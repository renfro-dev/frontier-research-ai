# Weekly Systems Thinking Brief - TODO

## Project Status: Core Pipeline Operational ✅

### Completed ✅
- [x] Create PRD (Product Requirements Document)
- [x] Create .cursorrules for project constraints
- [x] Create README with architecture overview
- [x] Research and compile list of 20 potential content sources
- [x] Test access to 12 sources (RSS, scraping, restrictions)
- [x] Document RSS feeds and access patterns
- [x] Identify rate limits and access issues
- [x] **Phase 1: Infrastructure Setup** (Database, environment, 15 sources)
- [x] **Phase 2.1: Ingest Agent** (92 documents ingested)
- [x] **Phase 2.2: Extraction Agent** (33 documents extracted)
- [x] **Phase 2.3: Analysis Agent** (33 documents analyzed)
- [x] **Phase 3.1: Embedding Generation** (33 embeddings created)
- [x] **Documentation:** AGENT_WORKFLOW.md and AGENT_ACTIVITY_LOG.md

### Current Status 🔄
- **Documents:** 92 total (33 fully processed, 59 new awaiting extraction/embedding/analysis)
- **Sources:** 15 configured, 11 active
- **Cost:** ~$0.78 for analysis, ~$0.0004 for embeddings
- **Next:** Complete pipeline for 59 new documents, then build Synthesis Agent

---

## Phase 1: Infrastructure Setup ✅ COMPLETE

### 1.1 Database Setup ✅
- [x] Create Supabase account/project
- [x] Design database schema:
  - [x] `sources` table (author, URL, domain, RSS feed)
  - [x] `documents` table (raw HTML/markdown, fetched_at, source_id)
  - [x] `extractions` table (cleaned text, sections, document_id)
  - [x] `summaries` table (structured JSON outputs, extraction_id)
  - [x] `weekly_briefs` table (final essays, citations, published_at)
- [x] Enable pgvector extension
- [x] Create vector storage for embeddings
- [x] Set up indexes for performance

### 1.2 Environment Setup ✅
- [x] Set up Python/Node.js project structure
- [x] Install dependencies:
  - [x] RSS feed parser (feedparser)
  - [x] HTML scraper (BeautifulSoup4)
  - [x] Supabase client
  - [x] OpenAI/Anthropic SDK
  - [x] Vector embedding library
- [x] Configure environment variables:
  - [x] Supabase URL and keys
  - [x] Anthropic API key
  - [x] OpenAI API key

### 1.3 Source Configuration ✅
- [x] Sources stored directly in database (not config file)
- [x] Add original 7 Tier 1 sources
- [x] Add 9 additional high-quality sources (OpenAI, Matt Rickard, Interconnects, DeepMind, etc.)
- [x] Configure RSS feed URLs for each
- [x] **Total: 15 sources configured, 11 active**

---

## Phase 2: Core Agent Implementation 🤖

### 2.1 Ingest Agent ✅ COMPLETE
- [x] Build RSS feed parser
- [x] Implement "fetch new posts only" logic
- [x] Store raw content in `documents` table
- [x] Add deduplication check (don't re-fetch existing URLs)
- [x] Handle feed parsing errors gracefully
- [x] Log ingestion metrics (posts fetched, errors)
- [x] Test with 2-3 sources before full rollout
- [x] **Stress tested with 15 sources, 92 documents ingested**

**Script:** `scripts/ingest_agent.py`

**Future Enhancement (v2):**
- [ ] Add Firecrawl MCP server integration for blocked sources
- [ ] Implement fallback logic: Try RSS first, then HTML scraping, then Firecrawl

### 2.2 Extraction Agent ✅ COMPLETE
- [x] Build HTML-to-text cleaner
- [x] Implement section segmentation logic
- [x] Extract metadata (title, author, date, URL)
- [x] Store cleaned content in `extractions` table
- [x] Preserve inline code/formatting where relevant
- [x] Test extraction quality on sample posts
- [x] **33 documents extracted, 15,134 words total**

**Script:** `scripts/extraction_agent.py`

**Status:** Need to run on 59 new documents

### 2.3 Analysis Agent ✅ COMPLETE
- [x] Design structured JSON schema (claims, metaphors, examples, uncertainties, conflicts)
- [x] Build LLM prompt for conservative analysis
- [x] Implement JSON validation
- [x] Store analysis in `summaries` table
- [x] Add "force concrete example" constraint
- [x] Test on various content types
- [x] **33 documents analyzed: 247 claims, 34 metaphors, 75 examples, 30 uncertainties, 19 conflicts**
- [x] **Model:** Claude 3.7 Sonnet (claude-3-7-sonnet-20250219)
- [x] **Cost:** ~$0.024 per document average

**Script:** `scripts/analysis_agent.py`

**Status:** Need to run on 59 new documents

### 2.4 Synthesis Agent
- [ ] Design prompt for JSON → prose conversion
- [ ] Implement neutral teacher tone
- [ ] Build essay structure:
  - [ ] Executive framing
  - [ ] Key ideas (3-6 max)
  - [ ] Conflicts & tensions
  - [ ] "What this means for builders"
  - [ ] Source cards
- [ ] Add reading time calculator (target: ≤10 min)
- [ ] Enforce 1-2 page constraint
- [ ] Test prose quality

### 2.5 Reviewer Agent (Quality Gate)
- [ ] Build citation coverage checker
- [ ] Implement hallucination detection:
  - [ ] Cross-reference claims with source material
  - [ ] Flag unsupported assertions
- [ ] Check for "Unknown" statements where needed
- [ ] Verify reading time ≤10 minutes
- [ ] Verify ≥3 sources cited
- [ ] Generate pass/fail report
- [ ] Test with intentionally flawed briefs

---

## Phase 3: System Integration 🔗

### 3.1 Vector Similarity ✅ PARTIALLY COMPLETE
- [x] Generate embeddings for extractions
- [x] Store embeddings in pgvector
- [x] **33 embeddings created with OpenAI text-embedding-3-small**
- [x] **Cost:** ~$0.0004 total
- [ ] Build similarity comparison function
- [ ] Implement "is this genuinely new?" check
- [ ] Detect theme repetition across weeks
- [ ] Test with duplicate/similar content

**Script:** `scripts/generate_embeddings.py`

**Status:** Need to run on 59 new documents

### 3.2 APA Citation Formatter
- [ ] Build APA citation generator:
  - [ ] Author name formatting
  - [ ] Publication date
  - [ ] Article title
  - [ ] URL
- [ ] Create "Source Cards" template
- [ ] Test with various source formats

### 3.3 Brief Output Formatter
- [ ] Design Markdown template for briefs
- [ ] Implement reading time calculator
- [ ] Add citation inline markers [1], [2]
- [ ] Build bibliography section
- [ ] Test output formatting

### 3.4 MCP Orchestration Pipeline
- [ ] Design agent coordination flow:
  ```
  Ingest → Extraction → Vector Check → Analysis → Synthesis → Review → Publish
  ```
- [ ] Build pipeline orchestrator
- [ ] Implement error handling between agents
- [ ] Add logging at each stage
- [ ] Store intermediate outputs for debugging
- [ ] Test full pipeline end-to-end

### 3.5 Weekly Cron Scheduling
- [ ] Set up cron job (or equivalent):
  - [ ] Trigger: Once per week (e.g., Sunday 6am)
  - [ ] Run: Full ingestion + analysis pipeline
  - [ ] Output: Draft brief ready for review
- [ ] Add manual trigger option for testing
- [ ] Configure notifications (email/Slack) on completion
- [ ] Test scheduling logic

---

## Phase 4: Testing & Validation 🧪

### 4.1 Integration Testing
- [ ] Test with single source (Simon Willison)
- [ ] Validate data flow through all agents
- [ ] Check database records at each stage
- [ ] Review generated brief quality
- [ ] Test Reviewer gate with flawed input

### 4.2 Multi-Source Testing
- [ ] Run pipeline with all 7 Tier 1 sources
- [ ] Verify citation coverage across sources
- [ ] Check for conflicts/tensions surfaced
- [ ] Validate reading time constraint
- [ ] Review synthesis quality

### 4.3 Edge Case Testing
- [ ] Test with very long posts (>10k words)
- [ ] Test with very short posts (<500 words)
- [ ] Test with posts containing code/tables
- [ ] Test with duplicate content
- [ ] Test with no new content in a week

### 4.4 Success Metrics Validation
- [ ] M1: Can brief be published weekly? (test 4 weeks)
- [ ] M2: Does each brief cite ≥3 sources?
- [ ] M3: Reviewer gate passes (zero hallucinations)?
- [ ] M4: Reading time ≤10 minutes?

---

## Phase 5: First Production Run 🚀

### 5.1 Week 1
- [ ] Run full pipeline
- [ ] Human review of draft brief
- [ ] Manual edits if needed (document what/why)
- [ ] Publish to blog (manual)
- [ ] Collect feedback

### 5.2 Week 2-4
- [ ] Repeat weekly pipeline
- [ ] Track consistency
- [ ] Document any issues
- [ ] Refine prompts/agents as needed
- [ ] Validate M1 (≥4 consecutive weeks)

### 5.3 Post-Launch Review
- [ ] Review all 4 briefs
- [ ] Analyze what worked/what didn't
- [ ] Document lessons learned
- [ ] Plan v2 improvements

---

## Future Enhancements (v2+) 🔮

Not in scope for v1, but consider later:

### Content Expansion
- [ ] **Add Firecrawl MCP integration** for blocked sources (OpenAI Research)
- [ ] Add Tier 2 sources (HTML scraping for Anthropic, Hugging Face)
- [ ] Test remaining 8 untested sources
- [ ] Implement intelligent fallback: RSS → HTML scraping → Firecrawl

### Features
- [ ] Build text search UI for archive
- [ ] Email newsletter automation
- [ ] Social media posting automation
- [ ] Multi-author submissions
- [ ] Tutorial/how-to content
- [ ] Public API for brief access
- [ ] Analytics dashboard

---

## Current Blockers ❌

None! Core pipeline operational.

## Next Immediate Actions

### Short-term (Complete current batch)
1. **Run extraction agent on 59 new documents** → `python3 scripts/extraction_agent.py`
2. **Run embedding generator on new extractions** → `python3 scripts/generate_embeddings.py`
3. **Run analysis agent on new extractions** → `python3 scripts/analysis_agent.py`
4. **Regenerate activity log** → `python3 scripts/generate_activity_log.py`
5. **Verify quality** → Spot-check samples from new sources

### Medium-term (Phase 2.4)
6. **Build Synthesis Agent** → Transform structured JSON into readable weekly brief
7. **Build Reviewer Agent** → Quality gate for hallucination detection
8. **Test end-to-end** → Generate first complete weekly brief draft

### Long-term (Phase 3+)
9. **Automate pipeline** → Weekly cron job
10. **Build similarity detection** → "Is this genuinely new?" check
11. **Create output formatter** → APA citations, source cards
