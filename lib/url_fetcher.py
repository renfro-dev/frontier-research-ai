"""
URL Fetcher - Fetch full article HTML from URLs with retry logic and fallback
"""

import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result
)
from urllib.parse import urlparse
import time


@dataclass
class FetchResult:
    """Result of fetching a URL"""
    success: bool
    html: str  # Full HTML content or fallback content
    error: Optional[str] = None
    status_code: Optional[int] = None
    final_url: Optional[str] = None
    content_type: Optional[str] = None
    fetch_duration_ms: int = 0


class ArticleFetcher:
    """Fetch full article HTML from URLs with retry logic and rate limiting"""

    def __init__(self, timeout: int = 15, max_retries: int = 3, rate_limit_delay: float = 1.0):
        """
        Initialize the ArticleFetcher

        Args:
            timeout: HTTP request timeout in seconds
            max_retries: Maximum number of retry attempts
            rate_limit_delay: Delay between requests to same domain (seconds)
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        self.logger = logging.getLogger(__name__)

        # Track last request time per domain for rate limiting
        self.domain_last_request: Dict[str, datetime] = {}

        # User-Agent header
        self.user_agent = 'Weekly-AI-Brief/1.0 (Educational; +https://github.com)'

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc or parsed.path.split('/')[0]
        except Exception:
            return "unknown"

    def _apply_rate_limit(self, url: str) -> None:
        """Apply per-domain rate limiting"""
        domain = self._get_domain(url)

        if domain in self.domain_last_request:
            last_request = self.domain_last_request[domain]
            elapsed = (datetime.now() - last_request).total_seconds()

            if elapsed < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - elapsed
                self.logger.debug(f"Rate limiting {domain}: sleeping {sleep_time:.2f}s")
                time.sleep(sleep_time)

        self.domain_last_request[domain] = datetime.now()

    def _is_retryable_exception(self, exception: Exception) -> bool:
        """Determine if an exception is retryable"""
        retryable_types = (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ChunkedEncodingError
        )
        return isinstance(exception, retryable_types)

    def _is_retryable_status(self, status_code: int) -> bool:
        """Determine if a status code is retryable"""
        # Retry on: 429 (rate limit), 500, 502, 503, 504 (server errors)
        return status_code in (429, 500, 502, 503, 504)

    def _is_valid_content_type(self, content_type: Optional[str]) -> bool:
        """Check if content type is valid for article extraction"""
        if not content_type:
            return True  # Assume valid if no content-type header

        # Accept HTML and XHTML
        valid_types = ('text/html', 'application/xhtml+xml', 'application/xml', 'text/xml')
        return any(content_type.startswith(vt) for vt in valid_types)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type((
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ChunkedEncodingError
        )),
        reraise=True
    )
    def _fetch_with_retry(self, url: str) -> requests.Response:
        """
        Fetch URL with retry logic for network errors

        Args:
            url: URL to fetch

        Returns:
            requests.Response object

        Raises:
            requests.exceptions.RequestException: On final failure
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=self.timeout,
            allow_redirects=True
        )

        # Handle HTTP errors - some are retryable
        if self._is_retryable_status(response.status_code):
            response.raise_for_status()  # Raises HTTPError

        # Non-retryable HTTP errors (4xx except 429) - return as-is
        # We'll handle them in fetch_url()

        return response

    def fetch_url(self, url: str, fallback_content: str = "") -> FetchResult:
        """
        Fetch full article HTML from URL with retry logic and fallback

        Args:
            url: URL to fetch
            fallback_content: Content to return if fetch fails

        Returns:
            FetchResult with HTML content (or fallback) and metadata
        """
        start_time = datetime.now()

        try:
            # Apply rate limiting
            self._apply_rate_limit(url)

            # Fetch with retry logic
            response = self._fetch_with_retry(url)

            # Check status code
            if response.status_code >= 400:
                # Non-retryable client errors (404, 403, etc.)
                error_msg = f"HTTP {response.status_code}"
                self.logger.warning(f"Failed to fetch {url}: {error_msg}")

                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                return FetchResult(
                    success=False,
                    html=fallback_content,
                    error=error_msg,
                    status_code=response.status_code,
                    final_url=response.url,
                    fetch_duration_ms=duration_ms
                )

            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if not self._is_valid_content_type(content_type):
                error_msg = f"Invalid content-type: {content_type}"
                self.logger.warning(f"Failed to fetch {url}: {error_msg}")

                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                return FetchResult(
                    success=False,
                    html=fallback_content,
                    error=error_msg,
                    status_code=response.status_code,
                    final_url=response.url,
                    content_type=content_type,
                    fetch_duration_ms=duration_ms
                )

            # Check if content is too small (likely error page)
            if len(response.text) < 100:
                error_msg = "Content too small (likely error page)"
                self.logger.warning(f"Failed to fetch {url}: {error_msg}")

                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                return FetchResult(
                    success=False,
                    html=fallback_content,
                    error=error_msg,
                    status_code=response.status_code,
                    final_url=response.url,
                    content_type=content_type,
                    fetch_duration_ms=duration_ms
                )

            # Success!
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            self.logger.debug(f"Successfully fetched {url} ({len(response.text)} bytes in {duration_ms}ms)")

            return FetchResult(
                success=True,
                html=response.text,
                status_code=response.status_code,
                final_url=response.url,
                content_type=content_type,
                fetch_duration_ms=duration_ms
            )

        except requests.exceptions.Timeout as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            error_msg = f"Request timeout after {self.timeout}s"
            self.logger.warning(f"Failed to fetch {url}: {error_msg}")

            return FetchResult(
                success=False,
                html=fallback_content,
                error=error_msg,
                fetch_duration_ms=duration_ms
            )

        except requests.exceptions.ConnectionError as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            error_msg = f"Connection error: {str(e)[:100]}"
            self.logger.warning(f"Failed to fetch {url}: {error_msg}")

            return FetchResult(
                success=False,
                html=fallback_content,
                error=error_msg,
                fetch_duration_ms=duration_ms
            )

        except requests.exceptions.RequestException as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            error_msg = f"Request error: {str(e)[:100]}"
            self.logger.warning(f"Failed to fetch {url}: {error_msg}")

            return FetchResult(
                success=False,
                html=fallback_content,
                error=error_msg,
                fetch_duration_ms=duration_ms
            )

        except Exception as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            error_msg = f"Unexpected error: {str(e)[:100]}"
            self.logger.error(f"Failed to fetch {url}: {error_msg}")

            return FetchResult(
                success=False,
                html=fallback_content,
                error=error_msg,
                fetch_duration_ms=duration_ms
            )
