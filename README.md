# Systems Thinking Brief

An automated briefing system that aggregates and synthesizes long-form content from leading AI and systems thinkers into accessible monthly and quarterly essays for non-technical operators and founders.

## Overview

This system automatically collects, analyzes, and synthesizes new content from trusted sources (e.g., Simon Willison, Eugene Yan, Nathan Lambert, OpenAI, Anthropic, etc) into monthly and quarterly briefings that translate abstract AI concepts into concrete mental models and actionable insights.

**Status:** v1 (Python scripts, manual execution, 6 agents with 5 implemented)

## Target Audience

Non-technical founders, operators, RevOps leaders, and product managers who:
- Want to stay current on AI systems thinking
- Don't want raw research or hype
- Value clarity, examples, and tradeoffs
- Need citations they can trust and share

## Success Metrics

- **M1:** Monthly briefs generated with all 5 agents functioning
- **M2:** Each brief cites primary sources with APA-style citations
- **M3:** Conservative synthesis maintained (no speculation beyond sources)
- **M4:** Plain English accessible to semi-technical readers (non-developers)
- **M5:** Quarterly briefs connect insights across multiple months

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

The system uses six specialized agents, five of which are currently implemented:

#### 1. Ingest Agent
- **Trigger:** Manual or scheduled execution
- **Function:** Fetch blog posts from curated RSS feeds
- **Implementation:** Python script using `feedparser` library
- **Deduplication:** URL-based (checks existing documents before inserting)
- **Storage:** Raw content in `documents` table
- **Sources:** 7 Tier 1 sources (Simon Willison, Eugene Yan, Andrej Karpathy, Lilian Weng, Chip Huyen, Sebastian Raschka, Vicki Boykis)

#### 2. Extraction Agent
- **Input:** Raw HTML/markdown from documents table
- **Output:** Cleaned text stored in `extractions` table with metadata
- **Implementation:** BeautifulSoup-based HTML cleaning
- **Constraint:** No interpretation, pure text extraction
- **Processing:** Removes boilerplate, extracts article body, segments by section

#### 3. Embedding Agent
- **Input:** Cleaned text from extractions table
- **Output:** 1,536-dimensional embedding vectors
- **Implementation:** Calls OpenAI `text-embedding-3-small` API
- **Purpose:** Enable semantic similarity search, clustering, and deduplication detection
- **Batch Processing:** Processes up to 2,048 texts per API call for efficiency
- **Cost:** ~$0.02 per 1M tokens (very inexpensive)

#### 4. Analysis Agent
- **Input:** Cleaned text from extractions table
- **Output:** Structured JSON stored in `summaries` table containing:
  - `claims` — Factual assertions from the source
  - `metaphors` — Analogies and conceptual models used by author
  - `examples` — Concrete instances cited in article
  - `uncertainties` — Areas where author expressed doubt
  - `conflicts` — Claims that might conflict with other views
- **Implementation:** Calls Claude Sonnet 4 API with conservative analysis prompt
- **Principle:** No speculation beyond source material, surface uncertainties explicitly
- **Cost:** ~$0.038 per document (~$1.50/month for typical volume)

#### 5. Synthesis Agent
- **Input:** Structured JSON from multiple summaries (analysis outputs) OR completed monthly briefs for quarterly synthesis
- **Output:** Readable prose essays (monthly briefs or quarterly reports)
- **Implementation:** Calls Claude Sonnet 4 API with synthesis prompt
- **Two Modes:**
  - **Monthly Briefs:** Synthesize structured JSON from 40-100 analyzed documents covering one month
  - **Quarterly Reports:** Synthesize three completed monthly briefs to show evolution of themes over the quarter
- **Features:**
  - Context-aware timeframe detection (weekly vs monthly based on date range)
  - Plain English writing for semi-technical audiences
  - Mandatory jargon definitions on first use
  - Implications-first structure in executive summary
  - Sequential citation numbering (quarterly reports renumber citations [1], [2], [3]...)
- **Tone:** Neutral teacher, accessible to non-developers
- **Constraint:** Every claim must have citation, no new claims beyond source material
- **Cost:** ~$0.17-$0.44 per monthly brief, ~$0.50-$0.70 per quarterly report

#### 6. Reviewer Agent (Planned)
- **Status:** Not yet implemented
- **Function:** Quality control checkpoint before publication
- **Planned Checks:**
  - Citation coverage (every idea cited)
  - Hallucination detection
  - "Unknown" properly surfaced
  - Reading time within target
- **Outcome:** Pass/fail gate before publication

## Brief Output Format

Each monthly or quarterly brief includes:

1. **Executive Summary: Why This Matters**
   - Lead with implications and practical significance BEFORE summarizing events
   - Answer: "Why should a non-technical operator care about these developments?"
   - Connect technical changes to business, strategy, or decision-making impact
   - 2-3 paragraphs maximum

2. **Key Developments** (3-6 sections)
   - What actually happened this week (with citations)
   - Define ALL jargon on first use - assume reader is semi-technical but not a developer
   - Terms requiring definition: "open model", "closed model", "RL" (reinforcement learning), "MoE" (Mixture of Experts), "parameters", "fine-tuning", etc.
   - Example: "Open models—AI systems where the underlying code and model weights are publicly available, unlike closed models like GPT-5 where internals are proprietary—now rival their closed counterparts [3]."
   - Concrete metaphors and plain-language explanations
   - Tangible builder examples

3. **Tensions & Conflicts**
   - Where thinkers disagree or tradeoffs exist
   - Surface contradictions explicitly
   - Use first-party sources to show different perspectives

4. **Implications for Practitioners**
   - Concrete, actionable takeaways (optional - only if not fully covered in Executive Summary)
   - No prescriptions without evidence from sources

5. **Source Cards (APA)**
   - Numbered citations matching in-text references
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

### Writing Principles for Accessibility

**Contextualize with First-Party Sources**
- Use quotes from sources to provide critical context, not just report findings
- Surface authors' own observations about limitations, tradeoffs, and practical utility
- Example: If discussing a breakthrough, include author's own commentary on who benefits and what the constraints are

**Make Abstract Concepts Concrete**
- Translate technical scale into relatable comparisons
  - "6 gigawatts" → equivalence in city power consumption or data center capacity
  - "1M parameters" → explain what this means for speed/cost/capability
- **ALWAYS define jargon on first use** - this is mandatory, not optional
  - "Open model" → explain what it is, why it matters, how it differs from closed models
  - "RL" / "Reinforcement learning" → explain the concept before using the acronym
  - "MoE" / "Mixture of Experts" → provide plain-language explanation before using acronym
  - "Parameters" → explain what they are and why more/fewer matters
  - "Fine-tuning" → explain the process in plain language
- **Test**: Would a product manager or analyst with no coding background understand this without Googling?

**Surface Practical Implications**
- Distinguish specialized vs. general-purpose utility
  - When breakthroughs are in narrow domains (math competitions), note limitations for average users
  - Highlight "peaks and valleys" of specialization: great at X, still struggles with Y
- Connect technical developments to economic/geopolitical context when relevant
  - Chinese models surpassing US models → political/strategic implications
  - Government-private partnerships → explain shared incentives and power dynamics

**Explain Relationships and Dynamics**
- Clarify why multiple parties are aligned (or competing)
  - Infrastructure investments → explain what drives companies to invest in compute together
  - Open model competition → explain strategic reasons for open vs. closed approaches
- Note intersectionality between sectors (government, private companies, research institutions)

## Technology Stack

- **Database:** Supabase (Postgres + pgvector extension for embeddings)
- **LLM APIs:**
  - Claude Sonnet 4 (via Anthropic API) — Analysis and Synthesis agents
  - OpenAI text-embedding-3-small — Embedding generation
- **Libraries:**
  - `feedparser` — RSS feed parsing
  - `BeautifulSoup` — HTML cleaning
  - `anthropic` — Claude API client
  - `openai` — OpenAI API client
  - `supabase` — Database client
- **Development:** Python scripts, manual execution
- **Content Ingestion:** RSS feed parsers (v1)
- **Future:** Firecrawl MCP for bot-protected sites (v2)

## Explicitly Out of Scope (v1)

- Text search UI
- Email newsletter automation
- Social posting automation
- Multi-author submissions
- Tutorials or how-to guides

## Pipeline Flow (Current Implementation)

### Phase 1: Content Collection
```
1. Ingest Agent (manual execution)
   → Fetches RSS feeds from 7 sources
   → Stores raw HTML/markdown in documents table
   → URL-based deduplication (skips existing documents)
```

### Phase 2: Content Processing
```
2. Extraction Agent (manual execution)
   → Reads raw content from documents table
   → Cleans HTML, removes boilerplate
   → Stores cleaned text in extractions table

3. Embedding Agent (manual execution)
   → Reads cleaned text from extractions table
   → Calls OpenAI API to generate 1,536-dim vectors
   → Stores embeddings in extractions table
   → Enables semantic similarity search
```

### Phase 3: Analysis & Synthesis
```
4. Analysis Agent (manual execution)
   → Reads cleaned text from extractions table
   → Calls Claude Sonnet 4 API for structured analysis
   → Extracts claims, metaphors, examples, uncertainties, conflicts
   → Stores JSON in summaries table

5. Synthesis Agent (manual execution with date range)
   → Monthly Mode: Reads structured JSON from summaries table
   → Quarterly Mode: Reads three completed monthly briefs
   → Calls Claude Sonnet 4 API to generate prose
   → Creates monthly briefs (40-100 docs) or quarterly reports (synthesizes 3 months)
   → Renumbers citations sequentially for quarterly reports
   → Stores essays in weekly_briefs table
   → Exports markdown files to briefs/ directory
```

### Phase 4: Quality Control & Publishing
```
6. Manual Review
   → Human reads generated brief
   → Spot-checks citations and accuracy
   → Verifies accessibility for semi-technical readers

7. Manual Publish
   → (Future: automation via email/web)
```

**Note:** All agents run as standalone Python scripts. No automated scheduling currently implemented.

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Abstract drift | Force concrete example field |
| Hallucination | Conservative synthesis + Reviewer |
| Repetition | Vector similarity check |
| Over-automation | Human publish step retained |

## Getting Started

### Prerequisites
- Python 3.8+
- Supabase account
- OpenAI API key
- Anthropic API key

### Setup Steps

1. **Database Setup**
   ```bash
   # Run schema migration
   psql -h your-supabase-host -d postgres -f migrations/001_initial_schema.sql
   ```

2. **Environment Configuration**
   ```bash
   # Create .env file
   cp .env.example .env

   # Add API keys
   SUPABASE_URL=your-supabase-url
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   OPENAI_API_KEY=your-openai-key
   ANTHROPIC_API_KEY=your-anthropic-key
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Sources**
   ```bash
   # Populate sources table with 7 Tier 1 sources
   python scripts/add_sources.py
   ```

5. **Run Pipeline (Manual Execution)**
   ```bash
   # Step 1: Ingest new content
   python scripts/ingest_agent.py

   # Step 2: Extract clean text
   python scripts/extraction_agent.py

   # Step 3: Generate embeddings
   python scripts/embedding_agent.py

   # Step 4: Analyze content
   python scripts/analysis_agent.py

   # Step 5a: Generate monthly brief
   python scripts/synthesis_agent.py --start-date 2025-11-01 --end-date 2025-11-30

   # Step 5b: Generate quarterly report (after all monthly briefs are complete)
   python scripts/synthesis_agent.py --start-date 2025-10-01 --end-date 2025-12-31
   ```

6. **Review Output**
   - Generated briefs saved to `briefs/` directory
   - Also stored in Supabase `weekly_briefs` table
   - Monthly briefs: `monthly_brief_2025-11_november.md`
   - Quarterly reports: `quarterly_brief_2025-Q4.md`

## Contributing

This is currently a single-author system. Multi-author support and public contributions are not in scope for v1.

## License

[To be determined]
