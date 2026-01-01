# Agent Workflow - Weekly Systems Thinking Brief

## Overview

This system uses four specialized agents that work sequentially to transform RSS feeds into structured insights. Each agent performs one specific task, passes its output to the next agent, and logs all activity.

```
RSS Feeds → [1] Ingest → [2] Extract → [3] Embed → [4] Analyze → Structured Data
```

---

## Agent 1: Ingest Agent

**What it does:** Fetches new articles from RSS feeds and saves them to the database.

**In simple terms:** Think of this as a newspaper delivery service. It checks your favorite blogs every week, grabs new articles, and stores the raw HTML in your filing cabinet (database).

**Input:**
- List of 7 RSS feed URLs (Simon Willison, Eugene Yan, etc.)
- Last 30 days of content (configurable)

**Process:**
1. Connects to each RSS feed
2. Checks which articles are new (not already in database)
3. Downloads the full HTML content
4. Calculates a unique fingerprint (hash) for deduplication
5. Stores in `documents` table

**Output:**
- New rows in `documents` table
- Each row contains: title, author, URL, raw HTML, publication date

**Resources created:**
- Database table: `documents`
- Example: 33 documents from 7 sources

**When it runs:** Weekly (or on-demand via command line)

**Script:** `scripts/ingest_agent.py`

---

## Agent 2: Extraction Agent

**What it does:** Cleans up messy HTML and extracts readable text.

**In simple terms:** Imagine taking a newspaper page covered in ads, navigation menus, and formatting—this agent strips all that away and gives you just the article text, clean and readable.

**Input:**
- Documents from `documents` table (raw HTML)

**Process:**
1. Loads HTML content
2. Uses BeautifulSoup to remove:
   - Navigation menus
   - Ads and sidebars
   - Scripts and styles
   - Footer/header elements
3. Extracts main article text
4. Counts words and estimates reading time
5. Stores cleaned text in `extractions` table

**Output:**
- New rows in `extractions` table
- Each row contains: cleaned text, word count, reading time estimate

**Resources created:**
- Database table: `extractions`
- Example: 33 extractions, 15,134 total words, 82 minutes total reading time

**When it runs:** After Ingest Agent completes

**Script:** `scripts/extraction_agent.py`

---

## Agent 3: Embedding Generator

**What it does:** Converts text into mathematical vectors for similarity search.

**In simple terms:** Think of this as creating a "fingerprint" of what each article is about—not based on keywords, but on meaning. Later, you can find articles about similar topics even if they use different words.

**Input:**
- Cleaned text from `extractions` table

**Process:**
1. Loads cleaned text
2. Sends to OpenAI's embedding API
3. Receives 1,536-dimensional vector (a list of numbers)
4. Stores vector in `extractions` table

**Output:**
- Updates `extractions` table with `embedding` column
- Each embedding is 1,536 numbers representing semantic meaning

**Resources created:**
- Embedding vectors in `extractions.embedding` column
- Example: 33 embeddings, ~$0.0004 total cost

**When it runs:** After Extraction Agent completes

**Script:** `scripts/generate_embeddings.py`

---

## Agent 4: Analysis Agent

**What it does:** Reads articles and extracts structured information using AI.

**In simple terms:** This is like having a research assistant read every article and create index cards with: key claims, metaphors used, concrete examples, things the author wasn't sure about, and ideas that might conflict with other views.

**Input:**
- Cleaned text from `extractions` table
- Article metadata (title, author, date)

**Process:**
1. Loads cleaned text
2. Sends to Claude 3.7 Sonnet API with conservative analysis prompt
3. Claude extracts 5 types of information:
   - **Claims:** Factual assertions made by author
   - **Metaphors:** Analogies or conceptual models used
   - **Examples:** Concrete instances or case studies
   - **Uncertainties:** Where author expressed doubt
   - **Conflicts:** Claims that might conflict with other views
4. Validates JSON structure
5. Stores in `summaries` table

**Output:**
- New rows in `summaries` table
- Each row contains: structured JSON with 5 fields, model used, prompt version

**Resources created:**
- Database table: `summaries`
- Example: 33 summaries, 247 claims, 34 metaphors, 75 examples, 30 uncertainties, 19 conflicts
- Total cost: ~$0.78 for all documents

**Conservative principles:**
- NO speculation beyond source material
- NO adding AI's own interpretations
- Uses "Unknown" or "Insufficient Evidence" when appropriate
- Does NOT resolve conflicts—surfaces them for human review
- Maintains strict fidelity to author's original words

**When it runs:** After Embedding Generator completes

**Script:** `scripts/analysis_agent.py`

---

## Complete Pipeline Flow

### Step-by-Step Journey of One Article

1. **Week 1, Monday:** Ingest Agent runs
   - Checks Simon Willison's RSS feed
   - Finds new article: "How Rob Pike got spammed with AI slop"
   - Downloads HTML (3,842 characters)
   - Stores in `documents` table with ID `abc123`

2. **Week 1, Monday:** Extraction Agent runs
   - Loads document `abc123`
   - Strips HTML tags, navigation, footer
   - Extracts 487 words of clean text
   - Estimates 2 minutes reading time
   - Stores in `extractions` table with ID `def456`

3. **Week 1, Monday:** Embedding Generator runs
   - Loads extraction `def456`
   - Sends to OpenAI API
   - Receives 1,536-number vector: [0.023, -0.145, 0.891, ...]
   - Updates `extractions` table

4. **Week 1, Monday:** Analysis Agent runs
   - Loads extraction `def456`
   - Sends to Claude API with prompt
   - Claude extracts:
     - 9 claims (e.g., "Rob Pike received AI-generated email...")
     - 1 metaphor ("AI slop")
     - 4 examples (Rob Pike email, Carpentries email, etc.)
     - 0 uncertainties
     - 2 conflicts (AI agency, attribution issues)
   - Stores in `summaries` table with ID `ghi789`

5. **Result:** One article transformed into:
   - Raw HTML (stored)
   - Clean text (stored)
   - Semantic vector (stored)
   - Structured insights (stored)

---

## Database Tables

### documents
- **Purpose:** Raw articles from RSS feeds
- **Created by:** Ingest Agent
- **Key fields:** title, author, url, raw_html, published_at

### extractions
- **Purpose:** Cleaned text and embeddings
- **Created by:** Extraction Agent, updated by Embedding Generator
- **Key fields:** document_id, cleaned_text, word_count, embedding

### summaries
- **Purpose:** Structured analysis
- **Created by:** Analysis Agent
- **Key fields:** extraction_id, analysis_json, model_used, prompt_version

### sources
- **Purpose:** RSS feed configuration
- **Created by:** Manual setup script
- **Key fields:** name, rss_feed_url, is_active

---

## Current System Status

**Agents Completed:** 4/4
- ✅ Ingest Agent: 33 documents from 7 sources
- ✅ Extraction Agent: 33 clean text extractions
- ✅ Embedding Generator: 33 semantic vectors
- ✅ Analysis Agent: 33 structured summaries

**Total Resources:**
- 7 active RSS sources
- 33 documents (raw HTML)
- 33 extractions (15,134 words)
- 33 embeddings (1,536 dimensions each)
- 33 summaries (247 claims, 34 metaphors, 75 examples)

**Next Phase:** Synthesis Agent (Phase 6)
- Transforms structured data → readable weekly brief
- Designed for non-technical operators
- Maintains conservative, citation-based approach

---

## Running the Pipeline

### Full pipeline (all agents):
```bash
# 1. Ingest new articles
python3 scripts/ingest_agent.py

# 2. Extract clean text
python3 scripts/extraction_agent.py

# 3. Generate embeddings
python3 scripts/generate_embeddings.py

# 4. Analyze with Claude
python3 scripts/analysis_agent.py
```

### Dry-run mode (test without changes):
```bash
python3 scripts/ingest_agent.py --dry-run
python3 scripts/extraction_agent.py --dry-run
python3 scripts/analysis_agent.py --dry-run
```

### Process specific sources:
```bash
python3 scripts/ingest_agent.py --source "Simon Willison"
```

### Reprocess existing data:
```bash
python3 scripts/extraction_agent.py --reprocess
python3 scripts/analysis_agent.py --reprocess
```

---

## Cost Breakdown

| Agent | API | Cost per Document | Total (33 docs) |
|-------|-----|-------------------|-----------------|
| Ingest Agent | None | $0 | $0 |
| Extraction Agent | None | $0 | $0 |
| Embedding Generator | OpenAI | ~$0.00001 | ~$0.0004 |
| Analysis Agent | Claude | ~$0.024 | ~$0.78 |
| **Total** | | **~$0.024** | **~$0.78** |

**Estimated monthly cost:** 40 documents/month × $0.024 = ~$0.96/month

---

## Logging & Monitoring

All agents log to `logs/` directory with timestamped filenames:
- `logs/ingest_YYYYMMDD_HHMMSS.log`
- `logs/extraction_YYYYMMDD_HHMMSS.log`
- `logs/embeddings_YYYYMMDD_HHMMSS.log`
- `logs/analysis_YYYYMMDD_HHMMSS.log`

Each log contains:
- Timestamp for every operation
- Success/failure status
- Token counts and costs (for API calls)
- Error messages with stack traces
- Summary statistics

---

## Design Principles

1. **One agent, one job:** Each agent has a single, clear responsibility
2. **Idempotent:** Can re-run safely without duplicating data
3. **Conservative:** Never speculate, never hallucinate
4. **Traceable:** Every operation logged with timestamps
5. **Cost-conscious:** Tracks API costs for every call
6. **Fail-safe:** One document failing doesn't stop others
7. **Human-in-the-loop:** Critical decisions require approval
