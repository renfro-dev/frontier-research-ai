# Context Orchestration: The Meta-Skill That Unlocked AI Leverage in December 2025

## Executive Summary

This month marked a significant shift in how high-velocity leaders approach AI: the focus moved from model capabilities to **context orchestration** - the meta-skill of curating, sequencing, and surfacing information to AI systems for better decision-making. The bottleneck isn't AI capability—it's humans' ability to orchestrate context effectively. December's developments revealed that the most successful AI implementations weren't driven by better models, but by better context management strategies. From Claude Code generating in an hour what Google built in a year [3] to Boris Cherny shipping 259 PRs in 30 days [32], the pattern is clear: context orchestration creates leverage.

## The November 2025 Inflection Point: Context Matters More Than Models

While GPT-5.2 and Claude Opus 4.5 crossed an "invisible capability line" in November [15], December's developments revealed that the real breakthrough wasn't the models themselves but how leaders learned to manage their context. The most successful implementations came from those who mastered the meta-skill of context orchestration - deciding what information to give AI access to, what to hide, and when to surface it [16].

This month, we saw Jaana Dogan, Principal Engineer at Google, demonstrate this principle dramatically. She gave Claude Code a three-paragraph description of a distributed agent orchestration problem, and it generated in an hour what Google had been trying to build for a year [3]. The key wasn't the model's raw capability, but Dogan's ability to distill and sequence the right context.

Similarly, Boris Cherny, creator of Claude Code, landed 259 PRs and made 497 commits in just thirty days using Claude Code + Opus 4.5 [32]. This productivity explosion wasn't about typing faster—it was about learning to curate, prune, and sequence information effectively.

## Core Concepts: The Context Orchestration Toolkit

### 1. Context Management as a Management Problem

The most profound insight this month came from Ethan Mollick, who observed that "managing agents is really a management problem" [10]. This reframing is critical: the skills that make great managers—communicating clearly, setting achievable goals, providing relevant context—are precisely the skills needed for effective context orchestration [10].

Liz Fong-Jones reinforced this perspective, noting that language models transform you "from a programmer who writes lines of code, to a programmer that manages the context the model has access to, prunes irrelevant things, adds useful material to context, and writes detailed specifications" [23]. This is the essence of context orchestration.

For high-velocity leaders, this means your management experience transfers directly to AI effectiveness. The same skills you use to brief your team before a critical meeting apply to briefing AI systems before a complex task [10].

### 2. Vector Databases: Making Organizational Memory Searchable

Weaviate's December release highlighted how vector databases are evolving to support better context orchestration. Their v1.35 release introduced Object Time-to-Live (TTL), enabling automatic deletion of objects after a specified time period [18]. This feature addresses a critical context orchestration challenge: ensuring AI systems access fresh, relevant information while automatically pruning outdated context.

The release also expanded multimodal document embeddings support, making it easier to build powerful document retrieval applications [18]. For leaders, this means organizational knowledge—including images, documents, and text—can be made searchable and surfaced at decision time without manual context-switching.

### 3. Model Context Protocol (MCP): Giving AI Access to Your Systems

The Model Context Protocol (MCP) specification, widely adopted in early 2025, continues to transform how leaders integrate AI into workflows [16]. MCP allows AI systems to access your tools and data without manual copy-paste, creating significant leverage for decision-makers.

However, Simon Willison noted that MCP "may be a one-year wonder" as coding agents with shell access provide even more powerful context orchestration capabilities [16]. This suggests leaders should evaluate whether their context orchestration stack should evolve beyond MCP toward more agent-based approaches.

### 4. Retrieval-Augmented Generation (RAG): Surfacing Relevant Knowledge

Weaviate's support for multimodal document embeddings demonstrates how RAG systems are becoming more sophisticated in surfacing relevant knowledge at decision time [18]. The ability to search across text and images simultaneously means leaders can provide richer context to AI systems without manual curation.

This month also saw Simon Willison create a Software Heritage Repository Retriever tool to access archived Git repositories [1]. This tool demonstrates how RAG systems can now surface context from previously inaccessible sources, expanding the knowledge available for decision-making.

## Practical Applications: Context Orchestration in Action

### Cooking with Claude: A Microcosm of Context Orchestration

Simon Willison's experiment with "Cooking with Claude" provides a perfect case study in context orchestration for non-technical tasks. He took photos of two recipe cards, had Claude extract the details, then prompted it to build a custom application for cooking timing [37]. The result was a successful meal preparation that finished exactly on schedule.

The key insight: Willison didn't just ask for a recipe—he orchestrated context by:
1. Providing visual context (photos of recipe cards)
2. Requesting extraction of structured information
3. Defining the problem space (cooking two recipes simultaneously)
4. Setting constraints (mobile-friendly, persistent timing)

This same pattern applies to business decisions. Leaders who master context orchestration can transform complex, multi-faceted problems into structured workflows with clear timing and dependencies [37].

### Navigating Complex Systems with Context Orchestration

Another practical example came from Willison using Claude in Chrome to navigate the Cloudflare dashboard—a system he found "really difficult to navigate" [36]. By providing Claude with the right context about what he was looking for (CORS headers for a specific directory), Claude found the information in under two minutes [36].

This demonstrates how context orchestration can help leaders navigate complex systems without becoming technical experts themselves. The meta-skill is knowing what context to provide, not understanding every technical detail [36].

## Tensions & Tradeoffs in Context Orchestration

### 1. Security vs. Context Richness

A significant tension emerged around browser agents like ChatGPT Atlas and Claude in Chrome. While these tools provide powerful context orchestration by accessing web interfaces directly, they also introduce security risks through potential prompt injection attacks [28][36].

OpenAI acknowledged this tension, announcing efforts to strengthen ChatGPT Atlas against prompt injection attacks using "automated red teaming trained with reinforcement learning" [28]. Leaders must balance the leverage gained from rich context access against the security risks of exposing sensitive systems to AI tools.

### 2. Enterprise Adoption: Context Access vs. Organizational Control

Will Larson highlighted that "real AI adoption on real problems is a complex blend of domain context on the problem, domain experience with AI tooling, and old-fashioned IT issues" [13]. This creates a tension in larger organizations, which need three different teams working together on AI adoption [13].

Earlier-stage companies have an advantage because they can often find all three necessary aspects (domain context, AI experience, IT knowledge) in a single person or across two people [13]. This explains why smaller organizations often move faster with AI adoption—they face fewer context orchestration barriers.

### 3. Process vs. Outcomes in Context Orchestration

Ben Werdmuller predicted a split in the tech industry between outcome-driven and process-driven people [9]. Those who are excited to test with users faster (outcome-driven) will embrace AI tools, while those who derive meaning from the engineering process itself (process-driven) may resist having that process automated [9].

This tension applies to all knowledge work. Leaders must decide whether their organization values the process of creating solutions or the outcomes those solutions deliver. Context orchestration optimizes for outcomes, potentially at the expense of process knowledge [9].

## Your Context Orchestration Stack: What to Evaluate This Quarter

Based on December's developments, high-velocity leaders should evaluate these context orchestration tools:

1. **Coding Agents as Context Management Training Grounds**: Tools like Claude Code and Codex (now called "Codex web" [8]) provide excellent practice for context orchestration skills. Even if you're not a developer, experimenting with these tools teaches valuable meta-skills that transfer to business contexts [10].

2. **Vector Databases with Lifecycle Management**: Solutions like Weaviate with Object TTL capabilities [18] ensure your AI systems access fresh, relevant information while automatically pruning outdated context.

3. **Browser Agents (with Security Guardrails)**: Tools like Claude in Chrome can navigate complex systems on your behalf [36], but require careful security considerations [28].

4. **Custom Context Orchestration Applications**: Following Willison's cooking example [37], consider building custom applications that structure complex workflows with clear timing and dependencies.

The key question isn't "which AI model should we use?" but "what context should we give it access to, and when?" [16] This is the essence of context orchestration—and the meta-skill that will create the most leverage for high-velocity leaders in 2026.

## Source Cards

[1] Simon Willison. (2025, December 30). TIL: Downloading archived Git repositories from archive.softwareheritage.org. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/30/software-heritage/#atom-everything

[2] Simon Willison. (2026, January 2). December 2025 sponsors-only newsletter. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/2/december/#atom-everything

[3] Simon Willison. (2026, January 4). Quoting Jaana Dogan. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/4/jaana-dogan/#atom-everything

[4] Simon Willison. (2025, December 30). Quoting Armin Ronacher. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/30/armin-ronacher/#atom-everything

[5] OpenAI Blog. (2026, January 2). Announcing OpenAI Grove Cohort 2. OpenAI Blog. https://openai.com/index/openai-grove

[6] Sebastian Raschka's Blog. (2025, December 30). LLM Research Papers: The 2025 List (July to December). Sebastian Raschka's Blog. https://sebastianraschka.com/blog/2025/llm-research-papers-2025-part2.html

[7] Sebastian Raschka's Blog. (2025, December 30). The State Of LLMs 2025: Progress, Problems, and Predictions. Sebastian Raschka's Blog. https://sebastianraschka.com/blog/2025/state-of-llms-2025.html

[8] Simon Willison. (2025, December 31). Codex cloud is now called Codex web. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/31/codex-cloud-is-now-called-codex-web/#atom-everything

[9] Simon Willison. (2026, January 2). Quoting Ben Werdmuller. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/2/ben-werdmuller/#atom-everything

[10] Simon Willison. (2026, January 4). Helping people write code again. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/4/coding-again/#atom-everything

[11] Simon Willison. (2026, January 4). Quoting Addy Osmani. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/4/addy-osmani/#atom-everything

[12] Simon Willison. (2026, January 2). The most popular blogs of Hacker News in 2025. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/2/most-popular-blogs-of-hacker-news/#atom-everything

[13] Simon Willison. (2026, January 2). Quoting Will Larson. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/2/will-larson/#atom-everything

[14] Simon Willison. (2026, January 3). Was Daft Punk Having a Laugh When They Chose the Tempo of Harder, Better, Faster, Stronger? Simon Willison's Weblog. https://simonwillison.net/2026/Jan/3/daft-punk/#atom-everything

[15] Simon Willison. (2026, January 4). The November 2025 inflection point. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/4/inflection/#atom-everything

[16] Simon Willison. (2025, December 31). 2025: The year in LLMs. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/31/the-year-in-llms/#atom-everything

[17] Simon Willison. (2026, January 1). Introducing gisthost.github.io. Simon Willison's Weblog. https://simonwillison.net/2026/Jan/1/gisthost/#atom-everything

[18] Weaviate Blog. (2025, December 29). Weaviate 1.35 Release. Weaviate Blog. https://weaviate.io/blog/weaviate-1-35-release

[19] Simon Willison. (2025, December 28). simonw/actions-latest. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/28/actions-latest/#atom-everything

[20] Simon Willison. (2025, December 29). Quoting Aaron Levie. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/aaron-levie/#atom-everything

[21] Simon Willison. (2025, December 29). Quoting Jason Gorman. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/jason-gorman/#atom-everything

[22] Simon Willison. (2025, December 29). shot-scraper 1.9. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/shot-scraper/#atom-everything

[23] Simon Willison. (2025, December 30). Quoting Liz Fong-Jones. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/30/liz-fong-jones/#atom-everything

[24] Vicki Boykis. (2025, December 26). Favorite Books of 2025. Vicki Boykis. https://veekaybee.github.io/essays/2025-12-26-favorite-books/

[25] Simon Willison. (2025, December 29). Quoting D. Richard Hipp. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/d-richard-hipp/#atom-everything

[26] Simon Willison. (2025, December 27). textarea.my on GitHub. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/textarea-my/#atom-everything

[27] Simon Willison. (2025, December 28). Substack Network error = security content they don't allow to be sent. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/28/substack-network-error/#atom-everything

[28] OpenAI Blog. (2025, December 22). Continuously hardening ChatGPT Atlas against prompt injection. OpenAI Blog. https://openai.com/index/hardening-atlas-against-prompt-injection

[29] OpenAI Blog. (2025, December 22). One in a million: celebrating the customers shaping AI's future. OpenAI Blog. https://openai.com/index/one-in-a-million-customers

[30] Simon Willison. (2025, December 26). How uv got so fast. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/26/how-uv-got-so-fast/#atom-everything

[31] Simon Willison. (2025, December 27). Pluribus training data. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/john-cena/#atom-everything

[32] Simon Willison. (2025, December 27). Quoting Boris Cherny. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/boris-cherny/#atom-everything

[33] Simon Willison. (2025, December 23). Quoting Salvatore Sanfilippo. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/23/salvatore-sanfilippo/#atom-everything

[34] Vicki Boykis. (2025, December 22). 2025 in review. Vicki Boykis. https://veekaybee.github.io/2025/12/22/2025-in-review/

[35] Simon Willison. (2025, December 24). uv-init-demos. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/24/uv-init-demos/#atom-everything

[36] Simon Willison. (2025, December 22). Using Claude in Chrome to navigate out the Cloudflare dashboard. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/22/claude-chrome-cloudflare/#atom-everything

[37] Simon Willison. (2025, December 23). Cooking with Claude. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/23/cooking-with-claude/#atom-everything

[38] Simon Willison. (2025, December 23). MicroQuickJS. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/23/microquickjs/#atom-everything

[39] Simon Willison. (2025, December 25). A new way to extract detailed transcripts from Claude Code. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/25/claude-code-transcripts/#atom-everything

[40] Simon Willison. (2025, December 26). How Rob Pike got spammed with an AI slop "act of kindness". Simon Willison's Weblog. https://simonwillison.net/2025/Dec/26/slop-acts-of-kindness/#atom-everything