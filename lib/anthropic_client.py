"""
Anthropic Claude API client for conservative text analysis.

Three cost-reduction strategies are applied:
  1. Haiku 4 for analysis  — 12× cheaper than Sonnet 4 for structured extraction
  2. Batch API             — 50% discount on all calls; results within 24 hrs
  3. Prompt caching        — 90% discount on repeat system-prompt tokens (≥1024 tok)
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Tuple, Optional
from anthropic import Anthropic, APIError, RateLimitError, APITimeoutError
from dotenv import load_dotenv

load_dotenv()

PROMPT_VERSION = "v1.0.0"

# ---------------------------------------------------------------------------
# Analysis system prompt (~400 tokens — below 1024 caching minimum, no cache)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Per-model pricing (USD per 1M tokens)
# ---------------------------------------------------------------------------
MODEL_PRICING = {
    "claude-haiku-4-20250514":  {"input": 0.25,  "output": 1.25},
    "claude-sonnet-4-20250514": {"input": 3.00,  "output": 15.00},
    "claude-opus-4-20250514":   {"input": 15.00, "output": 75.00},
}

MODEL_MAP = {
    "claude-haiku-4":    "claude-haiku-4-20250514",
    "claude-sonnet-4":   "claude-sonnet-4-20250514",
    "claude-3-7-sonnet": "claude-sonnet-4-20250514",
    "claude-opus-4":     "claude-opus-4-20250514",
}


def get_anthropic_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    return Anthropic(api_key=api_key)


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def _calculate_cost(actual_model: str, input_tokens: int, output_tokens: int,
                    cache_creation_tokens: int = 0, cache_read_tokens: int = 0,
                    batch: bool = False) -> float:
    pricing = MODEL_PRICING.get(actual_model, {"input": 3.00, "output": 15.00})
    base_in  = pricing["input"]  * (0.5 if batch else 1.0)
    base_out = pricing["output"] * (0.5 if batch else 1.0)

    regular_in = input_tokens - cache_creation_tokens - cache_read_tokens
    cost  = (regular_in           / 1_000_000) * base_in
    cost += (cache_creation_tokens / 1_000_000) * base_in * 1.25   # cache write: +25%
    cost += (cache_read_tokens     / 1_000_000) * base_in * 0.10   # cache read:  -90%
    cost += (output_tokens         / 1_000_000) * base_out
    return cost


def extract_json_from_response(response_text: str) -> Dict[str, Any]:
    logger = logging.getLogger(__name__)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        for marker in ("```json", "```"):
            if marker in response_text:
                start = response_text.find(marker) + len(marker)
                end   = response_text.find("```", start)
                if end > start:
                    try:
                        return json.loads(response_text[start:end].strip())
                    except json.JSONDecodeError:
                        pass
        logger.error(f"Could not extract JSON from response: {response_text[:500]}...")
        raise json.JSONDecodeError("No valid JSON found", response_text, 0)


# ---------------------------------------------------------------------------
# Single-call analysis (kept for dry-run / fallback — uses Haiku by default)
# ---------------------------------------------------------------------------
def analyze_text(
    text: str,
    metadata: Dict[str, Any],
    model: str = "claude-haiku-4-20250514",   # was Sonnet 4 — 12× cheaper
    max_tokens: int = 4096,
    temperature: float = 0.0,
    max_retries: int = 3,
) -> Dict[str, Any]:
    logger = logging.getLogger(__name__)
    client = get_anthropic_client()

    MAX_CHARS = 40_000
    if len(text) > MAX_CHARS:
        logger.warning(f"Text truncated from {len(text)} to {MAX_CHARS} chars")
        text = text[:MAX_CHARS]

    user_prompt = USER_PROMPT_TEMPLATE.format(
        title=metadata.get("title", "Unknown"),
        author=metadata.get("author", "Unknown"),
        published_at=metadata.get("published_at", "Unknown"),
        word_count=metadata.get("word_count", 0),
        cleaned_text=text,
    )

    for attempt in range(max_retries):
        try:
            t0 = time.time()
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
            elapsed = time.time() - t0
            analysis_json = extract_json_from_response(response.content[0].text)
            input_tokens  = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = _calculate_cost(model, input_tokens, output_tokens)
            logger.info(f"analyze_text OK {elapsed:.1f}s | {input_tokens}+{output_tokens} tok | ${cost:.4f}")
            return {
                "analysis_json":  analysis_json,
                "model_used":     model,
                "prompt_version": PROMPT_VERSION,
                "input_tokens":   input_tokens,
                "output_tokens":  output_tokens,
                "cost_usd":       cost,
            }
        except RateLimitError:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                logger.warning(f"Rate limited — retrying in {wait}s")
                time.sleep(wait)
            else:
                raise
        except APITimeoutError:
            logger.error("API timeout")
            raise
        except APIError as e:
            if attempt < max_retries - 1 and e.status_code in (500, 503):
                wait = 2 ** attempt
                logger.warning(f"API {e.status_code} — retrying in {wait}s")
                time.sleep(wait)
            else:
                raise
    raise APIError("Max retries exceeded")


# ---------------------------------------------------------------------------
# Batch analysis  — 50% discount, submits all articles in one API call
# items: list of (extraction_id, cleaned_text, metadata_dict)
# ---------------------------------------------------------------------------
def analyze_text_batch(
    items: List[Tuple[str, str, Dict[str, Any]]],
    model: str = "claude-haiku-4-20250514",
    max_tokens: int = 4096,
) -> Dict[str, Dict[str, Any]]:
    """
    Submit a batch of articles for analysis via the Anthropic Batch API.
    Returns a dict keyed by extraction_id.
    Each value has: success, analysis_json, input_tokens, output_tokens, cost_usd, error.
    """
    logger = logging.getLogger(__name__)
    client = get_anthropic_client()

    MAX_CHARS = 40_000
    requests = []
    for extraction_id, text, metadata in items:
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS]
        user_prompt = USER_PROMPT_TEMPLATE.format(
            title=metadata.get("title", "Unknown"),
            author=metadata.get("author", "Unknown"),
            published_at=metadata.get("published_at", "Unknown"),
            word_count=metadata.get("word_count", 0),
            cleaned_text=text,
        )
        requests.append({
            "custom_id": extraction_id,
            "params": {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": 0.0,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_prompt}],
            },
        })

    print(f"  📤 Submitting batch of {len(requests)} requests (Haiku 4, 50% batch discount)...")
    batch = client.messages.batches.create(requests=requests)
    logger.info(f"Batch created: {batch.id} | {len(requests)} requests")

    # Poll with increasing intervals
    poll_interval = 30
    while batch.processing_status == "in_progress":
        print(f"  ⏳ Batch {batch.id[:12]}… still processing — checking again in {poll_interval}s")
        time.sleep(poll_interval)
        batch = client.messages.batches.retrieve(batch.id)
        poll_interval = min(int(poll_interval * 1.5), 120)

    logger.info(f"Batch {batch.id} ended — request counts: {batch.request_counts}")

    # Collect results
    results: Dict[str, Dict[str, Any]] = {}
    for result in client.messages.batches.results(batch.id):
        eid = result.custom_id
        if result.result.type == "succeeded":
            msg = result.result.message
            cache_create = getattr(msg.usage, "cache_creation_input_tokens", 0) or 0
            cache_read   = getattr(msg.usage, "cache_read_input_tokens",     0) or 0
            try:
                analysis_json = extract_json_from_response(msg.content[0].text)
                results[eid] = {
                    "success":       True,
                    "analysis_json": analysis_json,
                    "input_tokens":  msg.usage.input_tokens,
                    "output_tokens": msg.usage.output_tokens,
                    "cost_usd":      _calculate_cost(
                        model, msg.usage.input_tokens, msg.usage.output_tokens,
                        cache_create, cache_read, batch=True
                    ),
                }
            except Exception as e:
                results[eid] = {"success": False, "error": f"JSON parse failed: {e}"}
        else:
            err = getattr(result.result, "error", result.result)
            results[eid] = {"success": False, "error": str(err)}

    return results


# ---------------------------------------------------------------------------
# Generic Claude call  — prompt caching on system prompt + optional batch
# Used by synthesis agents (Opus 4 with cached ~7200-token system prompt)
# ---------------------------------------------------------------------------
def call_claude_api(
    system_prompt: str,
    user_prompt: str,
    model: str = "claude-sonnet-4",
    max_tokens: int = 4096,
    temperature: float = 0.0,
    max_retries: int = 3,
    use_batch: bool = True,          # default ON — 50% discount
) -> Dict[str, Any]:
    logger = logging.getLogger(__name__)
    actual_model = MODEL_MAP.get(model, model)

    # Cache the system prompt when it's long enough (≥1024 tokens ≈ 4096 chars)
    system_content: Any
    if len(system_prompt) >= 4096:
        system_content = [{"type": "text", "text": system_prompt,
                           "cache_control": {"type": "ephemeral"}}]
    else:
        system_content = system_prompt

    if use_batch:
        return _call_claude_batch(actual_model, system_content, user_prompt, max_tokens, temperature)
    else:
        return _call_claude_direct(actual_model, system_content, user_prompt,
                                   max_tokens, temperature, max_retries)


def _call_claude_batch(actual_model, system_content, user_prompt, max_tokens, temperature):
    logger = logging.getLogger(__name__)
    client = get_anthropic_client()

    # Normalise system_content for the batch params dict
    if isinstance(system_content, list):
        sys_param = system_content
    else:
        sys_param = system_content

    batch = client.messages.batches.create(requests=[{
        "custom_id": "synthesis-call",
        "params": {
            "model":       actual_model,
            "max_tokens":  max_tokens,
            "temperature": temperature,
            "system":      sys_param,
            "messages":    [{"role": "user", "content": user_prompt}],
        },
    }])
    logger.info(f"Synthesis batch created: {batch.id}")

    poll_interval = 20
    while batch.processing_status == "in_progress":
        print(f"  ⏳ Synthesis batch {batch.id[:12]}… checking in {poll_interval}s")
        time.sleep(poll_interval)
        batch = client.messages.batches.retrieve(batch.id)
        poll_interval = min(int(poll_interval * 1.5), 90)

    for result in client.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            msg          = result.result.message
            content      = msg.content[0].text
            input_tokens = msg.usage.input_tokens
            output_tokens = msg.usage.output_tokens
            cache_create = getattr(msg.usage, "cache_creation_input_tokens", 0) or 0
            cache_read   = getattr(msg.usage, "cache_read_input_tokens",     0) or 0
            cost = _calculate_cost(actual_model, input_tokens, output_tokens,
                                   cache_create, cache_read, batch=True)
            logger.info(f"Synthesis batch OK | {input_tokens}+{output_tokens} tok "
                        f"(cache_write={cache_create}, cache_read={cache_read}) | ${cost:.4f}")
            return {
                "content":       content,
                "input_tokens":  input_tokens,
                "output_tokens": output_tokens,
                "cost":          cost,
                "model":         actual_model,
            }
        else:
            raise APIError(f"Batch synthesis failed: {result.result}")

    raise APIError("No result returned from synthesis batch")


def _call_claude_direct(actual_model, system_content, user_prompt, max_tokens, temperature, max_retries):
    logger = logging.getLogger(__name__)
    client = get_anthropic_client()

    for attempt in range(max_retries):
        try:
            t0 = time.time()
            response = client.messages.create(
                model=actual_model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_content,
                messages=[{"role": "user", "content": user_prompt}],
            )
            elapsed = time.time() - t0
            content       = response.content[0].text
            input_tokens  = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cache_create  = getattr(response.usage, "cache_creation_input_tokens", 0) or 0
            cache_read    = getattr(response.usage, "cache_read_input_tokens",     0) or 0
            cost = _calculate_cost(actual_model, input_tokens, output_tokens, cache_create, cache_read)
            logger.info(f"call_claude_api OK {elapsed:.1f}s | {input_tokens}+{output_tokens} tok | ${cost:.4f}")
            return {
                "content":       content,
                "input_tokens":  input_tokens,
                "output_tokens": output_tokens,
                "cost":          cost,
                "model":         actual_model,
                "elapsed_time":  elapsed,
            }
        except RateLimitError:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                logger.warning(f"Rate limited — retrying in {wait}s")
                time.sleep(wait)
            else:
                raise
        except APITimeoutError:
            logger.error("API timeout")
            raise
        except APIError as e:
            if attempt < max_retries - 1 and e.status_code in (500, 503):
                wait = 2 ** attempt
                logger.warning(f"API {e.status_code} — retrying in {wait}s")
                time.sleep(wait)
            else:
                raise
    raise APIError("Max retries exceeded")
