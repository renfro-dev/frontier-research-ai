PRD.md

Product Requirements Document

Project name: Weekly Systems Thinking Brief
Status: v1 (Cursor-first, single-author, public-ready later)

1. Goal

Create a single, trusted weekly briefing that aggregates and synthesizes new long-form content from leading AI / systems thinkers (e.g., Andrej Karpathy, Simon Willison, Eugene Yan), translates abstract ideas into concrete mental models and builder takeaways, and publishes a 1–2 page blog post with citations for non-technical founders, RevOps leaders, and product operators.

2. Primary User

Non-technical founder / operator / RevOps / product leader who:

Wants to stay current on AI systems thinking

Does not want raw research or hype

Values clarity, examples, and tradeoffs

Needs citations they can trust and share

3. Success Metrics (v1)

M1: Weekly brief published consistently (≥4 consecutive weeks)

M2: Each brief cites ≥3 primary sources (APA style)

M3: Zero hallucinated claims (Reviewer gate passes)

M4: Reading time ≤10 minutes for a full brief

4. Non-Goals (Explicitly Out of Scope for v1)

❌ Text search UI

❌ Email newsletter automation

❌ Social posting automation

❌ Multi-author submissions

❌ Tutorials or how-to guides

5. Content Scope
5.1 Sources (v1)

Only first-party, long-form content:

Personal blogs

Official research / engineering blogs

Examples:

Simon Willison’s Weblog

Anthropic Research & Engineering posts (Anthropic)

Eugene Yan’s essays

Excluded (v1):

Twitter/X

Podcasts

YouTube

Replies / commentary / reposts

6. Weekly Output Format

Single unified essay (1–2 pages) with:

Executive framing
What changed this week and why it matters

Key ideas (3–6 max)

Concrete metaphors

Plain-language explanations

Tangible builder examples

Conflicts & tensions

Where thinkers disagree

Tradeoffs surfaced explicitly

“What this means for builders”

Conservative, actionable implications

No prescriptions without evidence

Source cards (APA)

Paraphrased summaries

Direct links to originals

7. Analysis Principles (Hard Constraints)
7.1 Model Behavior

Conservative synthesis only

No speculation beyond source material

Readability > verbatim fidelity

Paraphrase by default

Cite everything

7.2 Guardrails (Required)

“Unknown / Insufficient Evidence” is a valid outcome

Structured intermediate outputs before prose

Conflicting views must be surfaced, not resolved

8. Architecture Overview
8.1 Why Supabase + Vector (Hybrid)

Decision: Hybrid storage
Rationale:

You want indefinite raw preservation (relational strength)

You also want theme clustering & repetition detection (semantic strength)

This avoids premature over-indexing while enabling future public search.

8.2 Storage Layers
A. Relational (Supabase Postgres)

Tables:

sources — author, canonical URL, domain

documents — raw HTML / markdown, fetched_at

extractions — cleaned text, sections

summaries — structured LLM outputs

weekly_briefs — final essays + citations

B. Vector Store (pgvector or external)

Embedded extractions

Used for:

Deduplication

Theme reinforcement

“Is this genuinely new?” checks

9. MCP + Agent Orchestration (Cursor-First)
9.1 Agent Roles

Ingest Agent

Weekly scheduled scrape (cron)

Fetch new blog posts only

Store raw content indefinitely

Extraction Agent

Clean HTML → text

Section segmentation

No interpretation

Analysis Agent

Produce structured JSON:

claims

metaphors

examples

uncertainties

conflicts

Synthesis Agent

Translate structure → readable prose

Neutral teacher tone

No new claims

Reviewer Agent (Gate)

Citation coverage

Hallucination check

“Unknown” surfaced where needed

10. Weekly Scheduling

Cron: Once per week (configurable)

Pipeline:

Fetch new content

Compare against prior weeks (vector similarity)

Reinforce or flag repetition

Generate draft brief

Reviewer approval required

Publish to blog (manual or scripted)

11. Acceptance Criteria

 Weekly job runs without manual intervention

 Raw source content preserved

 Structured intermediate JSON stored

 Final essay ≤2 pages

 APA citations included for every idea

 Reviewer gate passes with no unresolved risks

12. Risks & Mitigations
Risk	Mitigation
Abstract drift	Force concrete example field
Hallucination	Conservative synthesis + Reviewer
Repetition	Vector similarity check
Over-automation	Human publish step retained