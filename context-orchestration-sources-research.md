# Context Orchestration Sources Research
**Date:** 2026-01-01
**Purpose:** Identify high-value sources for deepening context orchestration brief content

## Executive Summary

✅ **Recommended: Add 4-5 sources immediately**
These sources will 10x the depth of context orchestration content:
- LangChain Blog (agent frameworks, RAG patterns)
- LlamaIndex Blog (RAG systems, document processing)
- Weaviate Blog (vector databases, context engineering)
- Model Context Protocol site (MCP documentation)

## Detailed Source Analysis

### Tier 1: Must-Have Sources (Immediate Add)

#### 1. **LangChain Blog**
- **URL:** https://blog.langchain.com/
- **RSS Feed:** ✅ https://blog.langchain.com/rss/
- **Posting Frequency:** Multiple times per week
- **Content Focus:**
  - Agent engineering and debugging
  - LangSmith tools (agent builder, fetch)
  - Production case studies (Fastweb, Vodafone, Jimdo)
  - Framework development (LangChain v1.0)
  - Sandbox execution and skills integration
- **Value Add:** PRIMARY source for agent frameworks and production patterns
- **Accessibility:** Fully accessible, RSS available
- **Scraping Method:** RSS feed

#### 2. **LlamaIndex Blog**
- **URL:** https://www.llamaindex.ai/blog/
- **RSS Feed:** ⚠️ Not explicitly found (likely exists at /rss or /feed)
- **Posting Frequency:** Regular (Dec 2025 posts: LlamaParse v2, Coding Agents Safety)
- **Content Focus:**
  - Document processing (LlamaParse, LlamaExtract, LlamaSplit)
  - AI agents building and deployment
  - RAG systems and optimization
  - Enterprise document workflows
  - Financial/healthcare/insurance use cases
- **Notable:** 150+ tags for filtering (LLM, AI, Agents, RAG, Document Intelligence)
- **Value Add:** Deepest RAG content, document intelligence patterns
- **Accessibility:** Fully accessible
- **Scraping Method:** Check for RSS at /rss or /feed, fallback to HTML scraping

#### 3. **Weaviate Blog**
- **URL:** https://weaviate.io/blog
- **RSS Feed:** ⚠️ Not explicitly found
- **Recent Posts:**
  - Weaviate 1.35 Release (Dec 29, 2025)
  - **"Context Engineering for AI Agents"** (Dec 9, 2025) - HIGHLY RELEVANT
  - AWS Partnership (Dec 3, 2025)
  - Java Client v6 (Dec 2, 2025)
- **Content Focus:**
  - Vector database optimization
  - Context engineering (selecting, organizing, managing LLM info)
  - Technical releases and integration guides
  - Agentic AI patterns
- **Value Add:** Vector DB specifics, context engineering techniques
- **Accessibility:** Fully accessible
- **Scraping Method:** Check for RSS, fallback to HTML scraping

#### 4. **Model Context Protocol (MCP)**
- **URL:** https://modelcontextprotocol.io/
- **Content Type:** Documentation site (not a blog)
- **RSS Feed:** ❌ Unlikely (docs site)
- **Content Focus:**
  - MCP standard and protocol
  - Connecting AI to external systems
  - Building MCP servers and clients
  - Architecture and core concepts
- **Value Add:** Authoritative MCP content, practical implementation
- **Accessibility:** Fully accessible
- **Scraping Method:** HTML scraping or periodic manual updates

### Tier 2: Strong Supporting Sources

#### 5. **Pinecone Blog**
- **URL:** https://www.pinecone.io/blog/
- **RSS Feed:** ⚠️ Not explicitly found (appears to be JavaScript-heavy site)
- **Recent Posts:** Dedicated Read Nodes (Dec 2025)
- **Content Focus:**
  - Vector database performance
  - Billion-vector workloads
  - High-QPS optimization
- **Value Add:** Vector DB at scale, performance optimization
- **Accessibility:** May require JavaScript rendering
- **Scraping Method:** Use MCP/Firecrawl for bot-protected site

#### 6. **Chroma Blog**
- **URL:** https://www.trychroma.com/blog
- **RSS Feed:** ❌ Not detected
- **Status:** JavaScript-heavy Next.js app
- **Content Focus:** Open-source vector DB for AI applications
- **Value Add:** Open-source vector DB patterns
- **Accessibility:** Requires JavaScript rendering
- **Scraping Method:** Use MCP/Firecrawl, or check /blog/feed endpoint

### Tier 3: Documentation/Reference (Not Blogs)

#### 7. **Anthropic Research**
- **URL:** https://www.anthropic.com/research
- **RSS Feed:** ❌ Not found
- **MCP Content:** Redirects to modelcontextprotocol.io (covered above)
- **Status:** Research papers, not blog format
- **Recommendation:** Already have Anthropic News in sources (row 14)

## Implementation Plan

### Phase 1: Add RSS-Based Sources (Immediate)
Add these 3 sources with RSS feeds:
1. **LangChain Blog** - https://blog.langchain.com/ (RSS: /rss/)
2. **LlamaIndex Blog** - https://www.llamaindex.ai/blog/ (test /rss or /feed)
3. **Weaviate Blog** - https://weaviate.io/blog (test /rss or /feed)

**Action:**
```bash
# Add to sources table with source_type='rss'
python scripts/add_sources.py --add langchain llamaindex weaviate
```

### Phase 2: Add MCP Docs (Manual/Periodic)
4. **Model Context Protocol** - https://modelcontextprotocol.io/

**Action:** Since this is a docs site, consider:
- Manual periodic updates (monthly)
- HTML scraping script for docs
- Or treat as reference material (link in briefs)

### Phase 3: Add JavaScript-Heavy Sites (MCP/Firecrawl)
5. **Pinecone Blog** - Requires JavaScript rendering
6. **Chroma Blog** - Requires JavaScript rendering

**Action:**
```bash
# Add to sources table with source_type='firecrawl' or 'html_scrape'
# Will require Firecrawl MCP server or Playwright/Puppeteer
```

## Expected Impact

### Before (Current State)
- **1 mention** of MCP
- **4 mentions** of RAG
- **0 specific** vector database content
- Generic AI news reframed as orchestration lessons

### After (With New Sources)
- **50-100+ mentions** of MCP, RAG, vector DBs
- **Concrete implementation patterns** from LangChain/LlamaIndex
- **Case studies** from production deployments
- **Technical depth** on context engineering (Weaviate article)
- **Authoritative MCP content** from official docs

## RSS Feed URLs (Confirmed/Likely)

| Source | RSS Feed URL | Status |
|--------|-------------|---------|
| LangChain | https://blog.langchain.com/rss/ | ✅ Confirmed |
| LlamaIndex | https://www.llamaindex.ai/blog/rss or /feed | ⚠️ Test |
| Weaviate | https://weaviate.io/blog/rss or /feed | ⚠️ Test |
| Pinecone | Unknown (JS-heavy) | ❌ Use MCP |
| Chroma | Unknown (JS-heavy) | ❌ Use MCP |

## Next Steps

1. **Test RSS feeds** for LlamaIndex and Weaviate:
   ```bash
   curl -I https://www.llamaindex.ai/blog/rss
   curl -I https://www.llamaindex.ai/blog/feed
   curl -I https://weaviate.io/blog/rss
   curl -I https://weaviate.io/blog/feed
   ```

2. **Add sources to database** using `add_sources.py` script

3. **Run ingest pipeline** for December content:
   ```bash
   python scripts/ingest_agent.py --sources langchain llamaindex weaviate
   ```

4. **Process new content** through full pipeline:
   ```bash
   python scripts/extraction_agent.py
   python scripts/embedding_agent.py
   python scripts/analysis_agent.py
   ```

5. **Re-generate context orchestration brief**:
   ```bash
   python scripts/synthesis_agent_orchestration.py --start-date 2025-12-01 --end-date 2025-12-31
   ```

6. **Compare depth** with original brief

## Tools Needed

- **For RSS sources:** Existing `feedparser` library (already in use)
- **For MCP docs:** BeautifulSoup HTML scraping (already in use)
- **For JS-heavy sites:** Firecrawl MCP server (install needed) or Playwright

## Estimated Timeline

- **Phase 1 (RSS sources):** 30 minutes to add + 2 hours for ingestion/processing
- **Phase 2 (MCP docs):** 1 hour for custom scraper or manual extraction
- **Phase 3 (JS sites):** 2-3 hours to set up Firecrawl MCP

**Total to meaningful improvement:** 3-4 hours of work for 10x content depth
