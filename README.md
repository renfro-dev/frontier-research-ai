# Weekly Systems Thinking Brief

A trusted weekly briefing system that aggregates and synthesizes long-form content from leading AI and systems thinkers into accessible 1-2 page essays for non-technical operators and founders.

## Overview

This system automatically collects, analyzes, and synthesizes new content from trusted sources (e.g., Andrej Karpathy, Simon Willison, Eugene Yan) into weekly briefings that translate abstract AI concepts into concrete mental models and actionable insights.

**Status:** v1 (Cursor-first, single-author, public-ready later)

## Target Audience

Non-technical founders, operators, RevOps leaders, and product managers who:
- Want to stay current on AI systems thinking
- Don't want raw research or hype
- Value clarity, examples, and tradeoffs
- Need citations they can trust and share

## Success Metrics

- **M1:** Weekly brief published consistently (≥4 consecutive weeks)
- **M2:** Each brief cites ≥3 primary sources (APA style)
- **M3:** Zero hallucinated claims (Reviewer gate passes)
- **M4:** Reading time ≤10 minutes per brief

## Architecture

### Hybrid Storage Strategy

**Supabase Postgres (Relational)**
- `sources` — Author metadata, canonical URLs
- `documents` — Raw HTML/markdown, fetched timestamps
- `extractions` — Cleaned text, section segmentation
- `summaries` — Structured LLM outputs (JSON)
- `weekly_briefs` — Final essays with citations

**pgvector (Semantic)**
- Embedded extractions for:
  - Deduplication detection
  - Theme clustering
  - "Is this genuinely new?" checks

### Agent Pipeline

The system uses five specialized agents orchestrated via MCP:

#### 1. Ingest Agent
- **Trigger:** Weekly cron job
- **Function:** Fetch new blog posts from curated sources
- **Storage:** Raw content preserved indefinitely
- **Sources:** Personal blogs, official research/engineering blogs only

#### 2. Extraction Agent
- **Input:** Raw HTML/markdown
- **Output:** Cleaned text with section segmentation
- **Constraint:** No interpretation, pure extraction

#### 3. Analysis Agent
- **Input:** Cleaned extractions
- **Output:** Structured JSON containing:
  - `claims` — Factual assertions
  - `metaphors` — Analogies and models
  - `examples` — Concrete instances
  - `uncertainties` — Areas of doubt
  - `conflicts` — Points of disagreement
- **Principle:** Conservative synthesis only

#### 4. Synthesis Agent
- **Input:** Structured JSON from Analysis Agent
- **Output:** Readable prose (1-2 pages)
- **Tone:** Neutral teacher, plain language
- **Constraint:** No new claims beyond source material

#### 5. Reviewer Agent (Gate)
- **Function:** Quality control checkpoint
- **Checks:**
  - Citation coverage (every idea cited)
  - Hallucination detection
  - "Unknown" properly surfaced
  - Reading time ≤10 minutes
- **Outcome:** Pass/fail before publication

## Weekly Output Format

Each brief includes:

1. **Executive Framing**
   - What changed this week and why it matters

2. **Key Ideas** (3-6 max)
   - Concrete metaphors
   - Plain-language explanations
   - Tangible builder examples

3. **Conflicts & Tensions**
   - Where thinkers disagree
   - Tradeoffs surfaced explicitly

4. **What This Means for Builders**
   - Conservative, actionable implications
   - No prescriptions without evidence

5. **Source Cards (APA)**
   - Paraphrased summaries
   - Direct links to originals

## Content Scope

### Included (v1)
- Personal blogs (Simon Willison's Weblog, Eugene Yan)
- Official research/engineering blogs (Anthropic, etc.)
- First-party, long-form content only

### Excluded (v1)
- Twitter/X posts
- Podcasts
- YouTube videos
- Replies, commentary, reposts

## Core Principles

### Conservative Synthesis
- No speculation beyond source material
- "Unknown / Insufficient Evidence" is valid
- Conflicting views surfaced, not resolved

### Citation Requirements
- APA style for every claim
- Paraphrase by default
- Direct links to originals

### Quality Guardrails
- Structured intermediate outputs before prose
- Reviewer gate required
- Zero tolerance for hallucinated claims

## Technology Stack

- **Database:** Supabase (Postgres + pgvector)
- **Orchestration:** MCP + Agent framework
- **Scheduling:** Cron (weekly)
- **LLM:** Claude (via Anthropic API)
- **Development:** Cursor-first workflow
- **Content Ingestion (v1):** RSS feed parsers
- **Content Ingestion (v2):** Firecrawl MCP for bot-protected sites

## Explicitly Out of Scope (v1)

- Text search UI
- Email newsletter automation
- Social posting automation
- Multi-author submissions
- Tutorials or how-to guides

## Weekly Pipeline Flow

```
1. Cron trigger (weekly)
2. Ingest Agent → Fetch new content
3. Vector similarity check → Detect repetition
4. Extraction Agent → Clean content
5. Analysis Agent → Generate structured JSON
6. Synthesis Agent → Draft prose
7. Reviewer Agent → Quality gate
8. Manual publish step
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Abstract drift | Force concrete example field |
| Hallucination | Conservative synthesis + Reviewer |
| Repetition | Vector similarity check |
| Over-automation | Human publish step retained |

## Getting Started

1. Set up Supabase project with required tables
2. Enable pgvector extension
3. Configure source list (authors/blogs to track)
4. Set up MCP server connections
5. Configure Anthropic API credentials
6. Set weekly cron schedule
7. Run first ingestion cycle
8. Review and publish first brief

## Contributing

This is currently a single-author system. Multi-author support and public contributions are not in scope for v1.

## License

[To be determined]
