# Weekly Systems Thinking Brief - TODO

## Project Status: Planning Complete ✅

### Completed ✅
- [x] Create PRD (Product Requirements Document)
- [x] Create .cursorrules for project constraints
- [x] Create README with architecture overview
- [x] Research and compile list of 20 potential content sources
- [x] Test access to 12 sources (RSS, scraping, restrictions)
- [x] Document RSS feeds and access patterns
- [x] Identify rate limits and access issues

**Key Finding:** We have **7 excellent Tier 1 sources** with RSS feeds and long-form content that are immediately accessible. This is sufficient to build and validate the system.

---

## Phase 1: Infrastructure Setup 🏗️

### 1.1 Database Setup
- [ ] Create Supabase account/project
- [ ] Design database schema:
  - [ ] `sources` table (author, URL, domain, RSS feed)
  - [ ] `documents` table (raw HTML/markdown, fetched_at, source_id)
  - [ ] `extractions` table (cleaned text, sections, document_id)
  - [ ] `summaries` table (structured JSON outputs, extraction_id)
  - [ ] `weekly_briefs` table (final essays, citations, published_at)
- [ ] Enable pgvector extension
- [ ] Create vector storage for embeddings
- [ ] Set up indexes for performance

### 1.2 Environment Setup
- [ ] Set up Python/Node.js project structure
- [ ] Install dependencies:
  - [ ] RSS feed parser (feedparser)
  - [ ] HTML scraper (BeautifulSoup4, Playwright)
  - [ ] Supabase client
  - [ ] OpenAI/Anthropic SDK
  - [ ] Vector embedding library
- [ ] Configure environment variables:
  - [ ] Supabase URL and keys
  - [ ] Anthropic API key
  - [ ] Other service credentials

### 1.3 Source Configuration
- [ ] Create `sources.json` or `sources.yaml` config file
- [ ] Add Tier 1 sources (7 RSS-enabled sources):
  - [ ] Simon Willison's Weblog
  - [ ] Eugene Yan
  - [ ] Andrej Karpathy
  - [ ] Lilian Weng
  - [ ] Chip Huyen
  - [ ] Sebastian Raschka
  - [ ] Vicki Boykis
- [ ] Configure RSS feed URLs for each
- [ ] Set update frequency (weekly)

---

## Phase 2: Core Agent Implementation 🤖

### 2.1 Ingest Agent
- [ ] Build RSS feed parser
- [ ] Implement "fetch new posts only" logic
- [ ] Store raw content in `documents` table
- [ ] Add deduplication check (don't re-fetch existing URLs)
- [ ] Handle feed parsing errors gracefully
- [ ] Log ingestion metrics (posts fetched, errors)
- [ ] Test with 2-3 sources before full rollout

**Future Enhancement (v2):**
- [ ] Add Firecrawl MCP server integration for blocked sources (OpenAI Research)
- [ ] Implement fallback logic: Try RSS first, then HTML scraping, then Firecrawl
- [ ] Configure Firecrawl API key and rate limits
- [ ] Test with OpenAI Research blog (currently returns 403)

### 2.2 Extraction Agent
- [ ] Build HTML-to-text cleaner
- [ ] Implement section segmentation logic
- [ ] Extract metadata (title, author, date, URL)
- [ ] Store cleaned content in `extractions` table
- [ ] Preserve inline code/formatting where relevant
- [ ] Test extraction quality on sample posts

### 2.3 Analysis Agent
- [ ] Design structured JSON schema:
  ```json
  {
    "claims": [],
    "metaphors": [],
    "examples": [],
    "uncertainties": [],
    "conflicts": []
  }
  ```
- [ ] Build LLM prompt for conservative analysis
- [ ] Implement JSON validation
- [ ] Store analysis in `summaries` table
- [ ] Add "force concrete example" constraint
- [ ] Test on various content types

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

### 3.1 Vector Similarity
- [ ] Generate embeddings for extractions
- [ ] Store embeddings in pgvector
- [ ] Build similarity comparison function
- [ ] Implement "is this genuinely new?" check
- [ ] Detect theme repetition across weeks
- [ ] Test with duplicate/similar content

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

None! All Phase 1 research complete.

## Next Immediate Actions

1. **Set up Supabase project** (Phase 1.1)
2. **Design database schema** (Phase 1.1)
3. **Create source configuration file** (Phase 1.3)
4. **Build Ingest Agent** (Phase 2.1)

Start with these foundational pieces, then proceed sequentially through the phases.
