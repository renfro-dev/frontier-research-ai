# Content Sources Research

## Sources from PRD

### 1. Simon Willison's Weblog
- **URL:** https://simonwillison.net/
- **Author:** Simon Willison (Co-creator of Django, AI/LLM expert)
- **Content:** AI, LLMs, tooling, data
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - Atom feed at /atom/everything/
- **Notes:** Excellent source. Long-form content (1000+ words), clean structure, no restrictions, 245+ tags for organization

### 2. Anthropic Research & Engineering
- **URL:** https://www.anthropic.com/research
- **Author:** Anthropic team
- **Content:** AI safety, research papers, engineering posts
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** No visible RSS feed
- **Notes:** Long-form research papers, fully accessible, no restrictions. May need HTML scraping since no RSS

### 3. Eugene Yan
- **URL:** https://eugeneyan.com/
- **Author:** Eugene Yan (Applied ML, Amazon)
- **Content:** ML systems, applied AI, career
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - RSS link in footer
- **Notes:** Excellent source. 420K+ words across 209 posts, long-form content, 11.8K newsletter subscribers

### 4. Andrej Karpathy
- **URL:** https://karpathy.github.io/
- **Author:** Andrej Karpathy (ex-Tesla AI, OpenAI)
- **Content:** Deep learning, AI systems
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - /feed.xml
- **Notes:** High-quality technical blog, long-form articles, no restrictions. Posts from 2011-2022

## Additional High-Quality AI/Systems Thinking Sources

### 5. OpenAI Research Blog
- **URL:** https://openai.com/research/
- **Author:** OpenAI team
- **Content:** Research papers, engineering posts
- **Status:** ⚠️ BLOCKED (403 Error)
- **RSS Feed:** Could not test
- **Notes:** Bot protection/anti-scraping measures in place. **Solution for v2:** Use Firecrawl MCP server to bypass bot detection

### 6. Google DeepMind Blog
- **URL:** https://deepmind.google/discover/blog/
- **Author:** DeepMind team
- **Content:** AI research, breakthroughs
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 7. Distill.pub
- **URL:** https://distill.pub/
- **Author:** Various researchers
- **Content:** ML research, interactive explanations
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 8. Lilian Weng's Blog
- **URL:** https://lilianweng.github.io/
- **Author:** Lilian Weng (OpenAI)
- **Content:** Deep learning, RL, LLMs
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - index.xml
- **Notes:** Excellent source. Extremely long-form (9-45 minute reads), learning notes since 2017, MathJax support

### 9. Chip Huyen's Blog
- **URL:** https://huyenchip.com/blog/
- **Author:** Chip Huyen (ML systems)
- **Content:** MLOps, production ML, systems
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - /feed.xml
- **Notes:** High-quality production ML content, long-form articles, focus on AI system design

### 10. Jay Alammar's Blog
- **URL:** https://jalammar.github.io/
- **Author:** Jay Alammar
- **Content:** Visual ML explanations, transformers
- **Status:** ⚠️ MIGRATING TO SUBSTACK
- **RSS Feed:** No RSS on blog
- **Notes:** Author states "freezing this blog and starting to post on my Substack." Still has valuable archive content, but may not have new posts

### 11. Sebastian Raschka's Blog
- **URL:** https://sebastianraschka.com/blog/
- **Author:** Sebastian Raschka
- **Content:** Deep learning, LLMs, research
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - /rss_feed.xml
- **Notes:** Long-form technical content, includes tutorials and research summaries, organized by year

### 12. Vicki Boykis
- **URL:** https://vickiboykis.com/
- **Author:** Vicki Boykis
- **Content:** ML systems, data engineering, embeddings
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** Yes - /index.xml
- **Notes:** Long-form essays, covers Python, AWS, distributed systems, ML applications, search functionality

### 13. Stephen Wolfram Blog
- **URL:** https://writings.stephenwolfram.com/
- **Author:** Stephen Wolfram
- **Content:** Computational thinking, AI, systems
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 14. Nelson Elhage (Anthropic)
- **URL:** https://www.nelhage.com/
- **Author:** Nelson Elhage
- **Content:** AI interpretability, systems
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 15. Aleksa Gordić (The AI Epiphany)
- **URL:** https://gordicaleksa.medium.com/
- **Author:** Aleksa Gordić
- **Content:** Deep learning, research papers
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:** Medium - may have access issues

### 16. Shreya Shankar
- **URL:** https://www.shreyashankar.com/
- **Author:** Shreya Shankar (Berkeley, ex-Google)
- **Content:** ML systems, data quality
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 17. Christopher Olah's Blog
- **URL:** https://colah.github.io/
- **Author:** Christopher Olah (Anthropic)
- **Content:** Neural networks, interpretability
- **Status:** ✅ ACCESSIBLE (BUT INACTIVE)
- **RSS Feed:** No RSS
- **Notes:** High-quality content but appears inactive. Long-form articles on LSTM, neural network topology. Many posts published on Distill/Google Research Blog

### 18. Meta AI Research Blog
- **URL:** https://ai.meta.com/blog/
- **Author:** Meta AI team
- **Content:** Research, LLMs, systems
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 19. Cohere AI Blog
- **URL:** https://cohere.com/blog
- **Author:** Cohere team
- **Content:** LLMs, enterprise AI
- **Status:** TO TEST
- **RSS Feed:** TBD
- **Notes:**

### 20. Hugging Face Blog
- **URL:** https://huggingface.co/blog
- **Author:** Hugging Face team
- **Content:** Open source ML, transformers
- **Status:** ✅ ACCESSIBLE
- **RSS Feed:** No visible RSS feed
- **Notes:** Long-form technical content, 51 pages of articles, organized by categories (NLP, Audio, CV, RL, etc.), publicly readable without login

## Testing Criteria

For each source, we need to verify:
1. ✅ Accessible without authentication
2. ✅ Scrapable HTML structure
3. ✅ RSS/Atom feed available (preferred)
4. ✅ No aggressive rate limiting
5. ✅ robots.txt allows scraping
6. ✅ Consistent post structure
7. ✅ Contains long-form content (not just announcements)

## Access Test Results

### Summary Statistics
- **Total sources tested:** 12/20
- **Fully accessible with RSS:** 8 sources
- **Accessible without RSS:** 3 sources
- **Blocked/Restricted:** 1 source (OpenAI)
- **Migrating/Inactive:** 2 sources (Jay Alammar, Christopher Olah)

### ✅ TIER 1: Excellent Sources (RSS + Long-form + Active)
1. **Simon Willison's Weblog** - Atom feed, 1000+ word posts, very active
2. **Eugene Yan** - RSS, 420K words/209 posts, highly detailed
3. **Andrej Karpathy** - RSS, deep technical content (note: infrequent updates)
4. **Lilian Weng** - RSS, 9-45 min reads, exceptional depth
5. **Chip Huyen** - RSS, production ML focus, actionable content
6. **Sebastian Raschka** - RSS, tutorials + research, well-organized
7. **Vicki Boykis** - RSS, ML systems + engineering, long-form essays

### ✅ TIER 2: Good Sources (Accessible but No RSS)
8. **Anthropic Research** - Long-form research, fully accessible, will require HTML scraping
9. **Hugging Face Blog** - 51 pages of content, categorized, accessible, will require HTML scraping

### ⚠️ TIER 3: Problematic Sources
10. **OpenAI Research** - 403 blocked, bot protection active, may need browser automation
11. **Jay Alammar** - Migrated to Substack, no RSS, archive content only
12. **Christopher Olah** - Accessible but inactive, no RSS, mostly historical content

### 🔍 Not Yet Tested (8 sources)
- Google DeepMind Blog
- Distill.pub
- Stephen Wolfram Blog
- Nelson Elhage
- Aleksa Gordić (Medium - likely paywalled)
- Shreya Shankar
- Meta AI Research Blog
- Cohere AI Blog

## Recommendations

### Start With (Tier 1 - 7 sources)
These have everything we need: RSS feeds, long-form content, active publishing, no restrictions.

**Action:** Implement RSS-based ingestion for these 7 sources first. This proves the pipeline before dealing with HTML scraping.

### Add Next (Tier 2 - 2 sources)
- Anthropic Research - High priority but requires HTML scraping
- Hugging Face - Good content volume but requires HTML scraping

**Action:** Build HTML scraper capability after RSS pipeline is working.

### Investigate Further
- Test the 8 untested sources
- Consider alternatives to OpenAI (blocked)
- Decide if archive-only sources (Jay Alammar, Christopher Olah) provide enough value

### Technical Approach

#### For RSS Sources:
1. Use RSS feed readers/parsers
2. Poll weekly for new entries
3. Extract full content from feed or linked URL
4. Much simpler, more reliable

#### For Non-RSS Sources:
1. HTML scraping with Beautiful Soup / Playwright
2. Need to handle dynamic JavaScript loading
3. More fragile to site changes
4. May need robots.txt compliance checks

#### For Blocked Sources (OpenAI):
1. **Recommended (v2):** Use Firecrawl MCP server
   - Specifically designed to bypass bot protection
   - Handles JavaScript rendering
   - Clean markdown extraction
   - Built-in rate limiting
2. Alternative: Browser automation (Playwright/Puppeteer)
3. Or skip for v1 (we have 9 accessible sources already)

## Next Steps
1. ✅ Confirm we have enough accessible sources (YES - 9 solid sources)
2. Create source configuration file with Tier 1 sources
3. Implement RSS ingestion agent
4. Test with 2-3 sources before full rollout
5. Add HTML scraping for Tier 2 sources
6. Test remaining 8 sources when basic pipeline works
