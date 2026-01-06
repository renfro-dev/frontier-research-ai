"""
LinkedIn Publisher
Posts content to LinkedIn company page via API
"""

import logging
import requests
from typing import Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import Config

logger = logging.getLogger(__name__)


class LinkedInPublisher:
    """Posts to LinkedIn company page"""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize LinkedIn publisher

        Args:
            config: LinkedIn configuration (optional, uses Config if not provided)
        """
        self.config = config or Config.get_linkedin_config()
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']
        self.access_token = self.config['access_token']
        self.refresh_token = self.config.get('refresh_token')
        self.company_urn = self.config['company_urn']
        self.base_url = self.config['base_url']

        if not all([self.client_id, self.client_secret, self.access_token, self.company_urn]):
            raise ValueError("Missing required LinkedIn credentials")

        logger.info(f"LinkedIn publisher initialized for company: {self.company_urn}")

    def create_post(self, text: str, add_hashtags: bool = True) -> Dict:
        """
        Post to LinkedIn company page

        Args:
            text: Post content (max 3000 chars)
            add_hashtags: If True, add default hashtags

        Returns:
            Dictionary with:
                - post_id: LinkedIn post ID
                - post_url: Public URL of the post
                - status: 'published'

        Raises:
            ValueError: If text exceeds character limit
            requests.HTTPError: If API call fails
        """
        # Add hashtags if requested
        if add_hashtags:
            text = self._add_hashtags(text)

        # Validate length
        if len(text) > Config.POST_MAX_CHARS:
            raise ValueError(
                f"Post text too long: {len(text)} chars (max {Config.POST_MAX_CHARS})"
            )

        logger.info(f"Creating LinkedIn post ({len(text)} chars)")

        # Build UGC post payload
        payload = {
            "author": self.company_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        # Make API call with retry logic
        result = self._create_post_with_retry(payload)
        logger.info(f"Successfully created LinkedIn post: {result['post_id']}")
        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
        reraise=True
    )
    def _create_post_with_retry(self, payload: Dict) -> Dict:
        """
        Create post with retry logic

        Args:
            payload: UGC post payload

        Returns:
            Dictionary with post ID and URL

        Raises:
            requests.HTTPError: If API call fails after retries
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        try:
            response = requests.post(
                f'{self.base_url}/ugcPosts',
                json=payload,
                headers=headers,
                timeout=30
            )

            # Handle specific error codes
            if response.status_code == 401:
                logger.error("LinkedIn access token expired")
                raise ValueError(
                    "LinkedIn access token expired. Please refresh your token and update the .env file."
                )
            elif response.status_code == 403:
                logger.error("LinkedIn API permission denied")
                raise ValueError(
                    "Insufficient LinkedIn API permissions. Ensure your app has 'w_organization_social' scope."
                )
            elif response.status_code == 429:
                logger.warning("LinkedIn rate limit hit - retrying with backoff")
                raise requests.exceptions.HTTPError("Rate limit exceeded", response=response)
            elif response.status_code >= 500:
                logger.warning(f"LinkedIn server error: {response.status_code}")
                raise requests.exceptions.HTTPError("Server error", response=response)

            # Raise for other HTTP errors
            response.raise_for_status()

            # Extract post ID from response headers
            post_id = response.headers.get('X-RestLi-Id')
            if not post_id:
                # Try to extract from response body
                post_id = response.json().get('id', 'unknown')

            # Build public URL
            post_url = self._build_post_url(post_id)

            return {
                'post_id': post_id,
                'post_url': post_url,
                'status': 'published'
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"LinkedIn API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response body: {e.response.text}")
            raise

    def _add_hashtags(self, text: str) -> str:
        """
        Add default hashtags to post text

        Args:
            text: Original post text

        Returns:
            Text with hashtags appended
        """
        # Use first 3 hashtags from config
        hashtags = Config.DEFAULT_HASHTAGS[:3]
        return f"{text}\n\n{' '.join(hashtags)}"

    def _build_post_url(self, post_id: str) -> str:
        """
        Build public URL for a LinkedIn post

        Args:
            post_id: LinkedIn post ID (UGC post ID)

        Returns:
            Public LinkedIn URL
        """
        # LinkedIn UGC post URLs follow this pattern:
        # https://www.linkedin.com/feed/update/urn:li:ugcPost:{id}
        #
        # Note: The exact URL format may need adjustment based on the actual post ID format
        if post_id.startswith('urn:li:'):
            return f"https://www.linkedin.com/feed/update/{post_id}"
        else:
            return f"https://www.linkedin.com/feed/update/urn:li:ugcPost:{post_id}"

    def refresh_access_token(self) -> str:
        """
        Refresh expired access token using refresh token

        Returns:
            New access token

        Raises:
            ValueError: If refresh token is not configured
            requests.HTTPError: If refresh fails
        """
        if not self.refresh_token:
            raise ValueError("No refresh token configured")

        logger.info("Refreshing LinkedIn access token")

        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()

            new_token = response.json()['access_token']
            self.access_token = new_token

            logger.info("Successfully refreshed LinkedIn access token")
            logger.warning(
                "IMPORTANT: Update your .env file with the new access token:\n"
                f"LINKEDIN_ACCESS_TOKEN={new_token}"
            )

            return new_token

        except Exception as e:
            logger.error(f"Failed to refresh access token: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test LinkedIn API connection and credentials

        Returns:
            True if connection successful, False otherwise
        """
        logger.info("Testing LinkedIn API connection")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        try:
            # Try to get organization info
            response = requests.get(
                f'{self.base_url}/organizations/{self.company_urn.split(":")[-1]}',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                logger.info("LinkedIn API connection successful")
                return True
            elif response.status_code == 401:
                logger.error("LinkedIn access token is invalid or expired")
                return False
            else:
                logger.error(f"LinkedIn API returned status {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"LinkedIn API connection test failed: {e}")
            return False


def publish_to_linkedin(post_text: str, add_hashtags: bool = True) -> Dict:
    """
    Convenience function to publish a post to LinkedIn

    Args:
        post_text: Post content
        add_hashtags: If True, add default hashtags

    Returns:
        Dictionary with post ID and URL

    Raises:
        Exception: If publishing fails
    """
    publisher = LinkedInPublisher()
    return publisher.create_post(post_text, add_hashtags=add_hashtags)
