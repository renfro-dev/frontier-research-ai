"""
LinkedIn Post Generator
Uses Claude to extract and transform brief sections into LinkedIn posts
"""

import json
import logging
from typing import Dict, List, Optional
from anthropic import Anthropic

from .config import Config
from .prompts import (
    POST_SELECTION_SYSTEM_PROMPT,
    get_post_selection_prompt,
    WORD_COUNT_MIN,
    WORD_COUNT_MAX,
    CHAR_COUNT_MAX
)
from .db_helper import LinkedInPostsDB

logger = logging.getLogger(__name__)


class PostGenerator:
    """Generates LinkedIn posts from Context Orchestration briefs"""

    def __init__(self, dry_run: bool = False):
        """
        Initialize post generator

        Args:
            dry_run: If True, don't save to database (preview only)
        """
        self.dry_run = dry_run
        self.anthropic = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.db = LinkedInPostsDB() if not dry_run else None
        self.model = "claude-sonnet-4-20250514"

    def generate_posts_from_brief(
        self,
        brief_id: str,
        brief_content: str,
        brief_title: str,
        brief_date: str,
        num_posts: int = 2
    ) -> Dict:
        """
        Generate LinkedIn posts from a brief using Claude

        Args:
            brief_id: UUID of the source brief
            brief_content: Full markdown content of the brief
            brief_title: Title of the brief
            brief_date: Date range of the brief
            num_posts: Number of posts to generate (2 or 3)

        Returns:
            Dictionary with:
                - posts: List of generated post objects
                - cost: API call cost
                - tokens: Token usage statistics

        Raises:
            Exception: If API call fails or response is invalid
        """
        logger.info(f"Generating {num_posts} posts from brief: {brief_title}")

        # Build prompt
        user_prompt = get_post_selection_prompt(
            brief_content=brief_content,
            brief_title=brief_title,
            brief_date=brief_date,
            num_posts=num_posts
        )

        # Call Claude API
        try:
            response = self.anthropic.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                system=POST_SELECTION_SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract response text
            response_text = response.content[0].text

            # Parse JSON response
            posts_data = self._parse_claude_response(response_text)

            # Validate posts
            validated_posts = self._validate_posts(posts_data, brief_id)

            # Calculate cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = self._calculate_cost(input_tokens, output_tokens)

            logger.info(f"Generated {len(validated_posts)} posts. Cost: ${cost:.4f}")

            return {
                'posts': validated_posts,
                'cost': cost,
                'tokens': {
                    'input': input_tokens,
                    'output': output_tokens,
                    'total': input_tokens + output_tokens
                }
            }

        except Exception as e:
            logger.error(f"Failed to generate posts: {e}")
            raise

    def _parse_claude_response(self, response_text: str) -> Dict:
        """
        Parse Claude's JSON response

        Args:
            response_text: Raw response text from Claude

        Returns:
            Parsed JSON object

        Raises:
            ValueError: If response is not valid JSON
        """
        try:
            # Try to find JSON in response (handle cases where Claude adds extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)

            if 'posts' not in data:
                raise ValueError("Response missing 'posts' field")

            return data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"Invalid JSON response from Claude: {e}")

    def _validate_posts(self, posts_data: Dict, brief_id: str) -> List[Dict]:
        """
        Validate generated posts meet requirements

        Args:
            posts_data: Parsed JSON from Claude
            brief_id: UUID of source brief

        Returns:
            List of validated post dictionaries

        Raises:
            ValueError: If posts don't meet requirements
        """
        posts = posts_data.get('posts', [])

        if not posts:
            raise ValueError("No posts generated")

        validated = []
        for i, post in enumerate(posts, 1):
            # Check required fields
            required_fields = ['section_title', 'post_text', 'word_count']
            missing = [f for f in required_fields if f not in post]
            if missing:
                raise ValueError(f"Post {i} missing fields: {missing}")

            # Validate word count
            actual_word_count = len(post['post_text'].split())
            if actual_word_count < WORD_COUNT_MIN or actual_word_count > WORD_COUNT_MAX:
                logger.warning(
                    f"Post {i} word count {actual_word_count} outside range "
                    f"({WORD_COUNT_MIN}-{WORD_COUNT_MAX})"
                )

            # Validate character count
            char_count = len(post['post_text'])
            if char_count > CHAR_COUNT_MAX:
                raise ValueError(
                    f"Post {i} exceeds LinkedIn character limit: "
                    f"{char_count} > {CHAR_COUNT_MAX}"
                )

            # Build validated post object
            validated_post = {
                'brief_id': brief_id,
                'section_title': post['section_title'],
                'post_text': post['post_text'],
                'word_count': actual_word_count,  # Use actual count
                'character_count': char_count,
                'metadata': {
                    'selection_reason': post.get('selection_reason', ''),
                    'key_hook': post.get('key_hook', ''),
                    'claude_reported_word_count': post.get('word_count', 0)
                }
            }

            validated.append(validated_post)
            logger.info(
                f"Validated post {i}: '{post['section_title']}' "
                f"({actual_word_count} words, {char_count} chars)"
            )

        return validated

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate API call cost

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Total cost in USD
        """
        # Claude Sonnet 4 pricing (as of 2025-01-05)
        INPUT_COST_PER_1M = 3.00  # $3 per 1M input tokens
        OUTPUT_COST_PER_1M = 15.00  # $15 per 1M output tokens

        input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M
        output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M

        return input_cost + output_cost


def generate_linkedin_posts(
    brief_id: str,
    brief_content: str,
    num_posts: int = 2,
    dry_run: bool = False
) -> List[Dict]:
    """
    Main entry point for generating LinkedIn posts

    Args:
        brief_id: UUID of the source brief
        brief_content: Full markdown content of the brief
        num_posts: Number of posts to generate (2 or 3)
        dry_run: If True, don't save to database

    Returns:
        List of generated post dictionaries

    Raises:
        Exception: If generation fails
    """
    generator = PostGenerator(dry_run=dry_run)

    # Extract title and date from content
    lines = brief_content.split('\n')
    brief_title = lines[0].replace('#', '').strip() if lines else "Untitled Brief"

    # Try to extract date from title or content
    brief_date = "Unknown"
    for line in lines[:5]:
        if 'Executive Summary:' in line:
            brief_date = line.split('Executive Summary:')[-1].strip()
            break

    # Generate posts
    result = generator.generate_posts_from_brief(
        brief_id=brief_id,
        brief_content=brief_content,
        brief_title=brief_title,
        brief_date=brief_date,
        num_posts=num_posts
    )

    posts = result['posts']
    logger.info(f"Generated {len(posts)} posts for brief {brief_id}")

    return posts
