"""
Anthropic Claude API client for conservative text analysis
"""

import os
import json
import time
import logging
from typing import Dict, Any
from anthropic import Anthropic, APIError, RateLimitError, APITimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Prompt version for tracking
PROMPT_VERSION = "v1.0.0"

# Conservative analysis system prompt
SYSTEM_PROMPT = """You are a conservative analysis agent for a systems thinking research assistant.
Your role is to extract structured information from technical articles WITHOUT
adding interpretation or speculation.

Core principles:
1. ONLY extract what is explicitly stated in the source text
2. When evidence is insufficient, use "Unknown" or "Insufficient Evidence"
3. Do NOT resolve conflicts - surface them for human review
4. Do NOT add your own examples or metaphors - only extract author's
5. Maintain strict fidelity to source material

Return ONLY valid JSON with 5 fields: claims, metaphors, examples,
uncertainties, conflicts. No markdown, no explanations, no additional text."""

# User prompt template
USER_PROMPT_TEMPLATE = """Analyze the following article and extract structured information.

ARTICLE METADATA:
Title: {title}
Author: {author}
Published: {published_at}
Word Count: {word_count}

ARTICLE TEXT:
{cleaned_text}

INSTRUCTIONS:
1. Extract claims: Factual assertions made by the author. Include surrounding context for each claim.

2. Extract metaphors: Analogies, conceptual models, or explanatory frameworks used by the author. Explain what each metaphor represents.

3. Extract examples: Concrete instances, case studies, or demonstrations provided by the author. Include context about why each example was used.

4. Extract uncertainties: Topics where the author expressed uncertainty, acknowledged limitations, or indicated ongoing debate. Quote the author's statement if possible.

5. Extract conflicts: Claims that might conflict with commonly held views or other established perspectives. Note: You are NOT resolving these conflicts - just flagging them for human review.

CRITICAL CONSTRAINTS:
- DO NOT add your own interpretation
- DO NOT speculate beyond what is written
- If a category has no items, return an empty array []
- Use "Unknown" or "Insufficient Evidence" when appropriate
- Maintain author's voice in extracted text

Return your analysis as valid JSON matching this structure:
{{
  "claims": [
    {{
      "claim": "The specific assertion made",
      "context": "Surrounding context that clarifies the claim"
    }}
  ],
  "metaphors": [
    {{
      "metaphor": "The analogy or model used",
      "explanation": "What the metaphor represents or explains"
    }}
  ],
  "examples": [
    {{
      "example": "The concrete instance described",
      "context": "Why this example was used or what it demonstrates"
    }}
  ],
  "uncertainties": [
    {{
      "topic": "The subject of uncertainty",
      "nature_of_uncertainty": "What is uncertain or debated",
      "author_statement": "Direct quote if available (optional)"
    }}
  ],
  "conflicts": [
    {{
      "topic": "The subject of potential conflict",
      "description": "How this might conflict with other views"
    }}
  ]
}}"""


def get_anthropic_client() -> Anthropic:
    """
    Create and return Anthropic client

    Returns:
        Anthropic client

    Raises:
        ValueError: If API key not found in environment
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env")

    # Create client with just the API key
    # Note: We handle retries manually in analyze_text()
    return Anthropic(api_key=api_key)


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count
    Claude uses ~4 characters per token on average

    Args:
        text: Input text to estimate

    Returns:
        Estimated token count
    """
    return len(text) // 4


def extract_json_from_response(response_text: str) -> Dict[str, Any]:
    """
    Extract JSON from Claude's response, handling markdown code blocks

    Args:
        response_text: Raw response text from Claude

    Returns:
        Parsed JSON dict

    Raises:
        json.JSONDecodeError: If JSON cannot be extracted or parsed
    """
    logger = logging.getLogger(__name__)

    # Try parsing directly first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try extracting from markdown code block
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            if end > start:
                try:
                    return json.loads(response_text[start:end].strip())
                except json.JSONDecodeError:
                    pass

        # Try extracting from generic code block
        if "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            if end > start:
                try:
                    return json.loads(response_text[start:end].strip())
                except json.JSONDecodeError:
                    pass

        # If all else fails, log and raise
        logger.error(f"Could not extract valid JSON from response: {response_text[:500]}...")
        raise json.JSONDecodeError("No valid JSON found in response", response_text, 0)


def analyze_text(
    text: str,
    metadata: Dict[str, Any],
    model: str = "claude-3-5-sonnet-20241022",  # Latest Claude Sonnet model
    max_tokens: int = 4096,
    temperature: float = 0.0,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Send text to Claude for conservative analysis

    Args:
        text: Cleaned article text to analyze
        metadata: Dict with title, author, published_at, word_count
        model: Claude model to use (default: claude-sonnet-4)
        max_tokens: Maximum tokens in response (default: 4096)
        temperature: Sampling temperature (default: 0.0 for determinism)
        max_retries: Maximum retry attempts for rate limits (default: 3)

    Returns:
        Dict with analysis_json, model_used, prompt_version, input_tokens, output_tokens, cost_usd

    Raises:
        APIError: If API call fails after retries
        json.JSONDecodeError: If response is not valid JSON
    """
    logger = logging.getLogger(__name__)
    client = get_anthropic_client()

    # Truncate text if too long (Claude can handle ~200k tokens but we'll be conservative)
    MAX_CHARS = 40000  # ~10,000 words, ~32,000 tokens
    if len(text) > MAX_CHARS:
        logger.warning(f"Text too long ({len(text)} chars), truncating to {MAX_CHARS}")
        text = text[:MAX_CHARS]

    # Format user prompt with metadata
    user_prompt = USER_PROMPT_TEMPLATE.format(
        title=metadata.get('title', 'Unknown'),
        author=metadata.get('author', 'Unknown'),
        published_at=metadata.get('published_at', 'Unknown'),
        word_count=metadata.get('word_count', 0),
        cleaned_text=text
    )

    # Estimate tokens for cost calculation
    estimated_input_tokens = estimate_tokens(SYSTEM_PROMPT + user_prompt)

    # Retry loop for rate limits
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Claude API (attempt {attempt + 1}/{max_retries})...")
            start_time = time.time()

            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            elapsed_time = time.time() - start_time

            # Extract response text
            response_text = response.content[0].text

            # Parse JSON from response
            analysis_json = extract_json_from_response(response_text)

            # Get actual token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # Calculate cost
            # Claude Sonnet 4 pricing (as of Jan 2025):
            # Input: $3.00 per 1M tokens
            # Output: $15.00 per 1M tokens
            input_cost = (input_tokens / 1_000_000) * 3.00
            output_cost = (output_tokens / 1_000_000) * 15.00
            total_cost = input_cost + output_cost

            logger.info(
                f"API call successful: {elapsed_time:.1f}s, "
                f"{input_tokens:,} input + {output_tokens:,} output tokens, "
                f"${total_cost:.4f}"
            )

            return {
                "analysis_json": analysis_json,
                "model_used": model,
                "prompt_version": PROMPT_VERSION,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": total_cost
            }

        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limit exceeded after {max_retries} attempts")
                raise

        except APITimeoutError as e:
            logger.error(f"API timeout (likely document too long): {str(e)}")
            raise

        except APIError as e:
            if attempt < max_retries - 1 and e.status_code in [500, 503]:
                wait_time = 2 ** attempt
                logger.warning(f"API error {e.status_code}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"API error: {str(e)}")
                raise

    # Should not reach here, but just in case
    raise APIError("Max retries exceeded")


def call_claude_api(
    system_prompt: str,
    user_prompt: str,
    model: str = "claude-sonnet-4",
    max_tokens: int = 4096,
    temperature: float = 0.0,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Generic Claude API call with custom prompts

    Args:
        system_prompt: System instructions for Claude
        user_prompt: User message/request
        model: Claude model to use (default: claude-sonnet-4)
        max_tokens: Maximum tokens in response (default: 4096)
        temperature: Sampling temperature (default: 0.0 for determinism)
        max_retries: Maximum retry attempts for rate limits (default: 3)

    Returns:
        Dict with content, input_tokens, output_tokens, cost

    Raises:
        APIError: If API call fails after retries
    """
    logger = logging.getLogger(__name__)
    client = get_anthropic_client()

    # Map friendly model name to actual model ID
    model_map = {
        "claude-sonnet-4": "claude-3-5-sonnet-20241022",
        "claude-3-7-sonnet": "claude-3-5-sonnet-20241022",
        "claude-opus-4": "claude-opus-4-20250514",
        "claude-haiku-4": "claude-3-5-haiku-20241022"
    }
    actual_model = model_map.get(model, model)

    # Retry loop for rate limits
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Claude API (attempt {attempt + 1}/{max_retries})...")
            start_time = time.time()

            response = client.messages.create(
                model=actual_model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            elapsed_time = time.time() - start_time

            # Extract response text
            content = response.content[0].text

            # Get actual token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # Calculate cost
            # Claude 3.7 Sonnet pricing (as of Jan 2025):
            # Input: $3.00 per 1M tokens
            # Output: $15.00 per 1M tokens
            input_cost = (input_tokens / 1_000_000) * 3.00
            output_cost = (output_tokens / 1_000_000) * 15.00
            total_cost = input_cost + output_cost

            logger.info(
                f"API call successful: {elapsed_time:.1f}s, "
                f"{input_tokens:,} input + {output_tokens:,} output tokens, "
                f"${total_cost:.4f}"
            )

            return {
                "content": content,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": total_cost,
                "model": actual_model,
                "elapsed_time": elapsed_time
            }

        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limit exceeded after {max_retries} attempts")
                raise

        except APITimeoutError as e:
            logger.error(f"API timeout: {str(e)}")
            raise

        except APIError as e:
            if attempt < max_retries - 1 and e.status_code in [500, 503]:
                wait_time = 2 ** attempt
                logger.warning(f"API error {e.status_code}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"API error: {str(e)}")
                raise

    # Should not reach here, but just in case
    raise APIError("Max retries exceeded")
