# Context Orchestration: The Meta-Skill Driving AI Leverage in 2026

## Executive Summary

This week's developments reveal a critical shift in how high-velocity leaders create leverage with AI. The bottleneck isn't AI capability—it's humans' ability to orchestrate context effectively. From Google's distributed agent orchestrators to Claude Code's impact on knowledge work, the pattern is clear: those who excel at curating, sequencing, and surfacing information to AI systems are achieving breakthrough results. This brief examines how context orchestration is becoming the essential meta-skill for leaders in 2026.

## The November 2025 Inflection Point: Context Orchestration Emerges

The release of GPT-5.2 and Claude Opus 4.5 in November 2025 marked a significant capability threshold crossing that has transformed how leaders interact with AI systems [15]. These models didn't just get incrementally better—they crossed an invisible capability line that opened up entirely new categories of problems AI could solve [15]. This inflection point has shifted the focus from AI capabilities to how humans orchestrate the context these systems receive.

The real breakthrough isn't in coding agents themselves, but in the meta-skill they expose: context orchestration. As Liz Fong-Jones notes, "A language model changes you from a programmer who writes lines of code, to a programmer that manages the context the model has access to, prunes irrelevant things, adds useful material to context, and writes detailed specifications" [22]. This shift applies equally to non-technical leaders who need to make high-velocity decisions.

## Context Orchestration in Action: Three Key Patterns

### 1. Context Management as a Management Problem

The most successful AI implementations this week demonstrate that context orchestration is fundamentally a management problem. Ethan Mollick observed that "managing agents is really a management problem" with "teachable skills" [10]. This reframes AI interaction from a technical challenge to a leadership one.

Management experience transfers directly to effectively using AI systems. The same skills used to communicate clearly, set achievable goals, and provide relevant context to team members apply to AI interactions [10]. For leaders, this means your existing management capabilities are more valuable than technical expertise when driving AI systems.

Ben Werdmuller predicts a split in the tech industry between outcome-driven people (who embrace AI to test with users faster) and process-driven people (who derive meaning from the engineering process itself) [9]. Leaders who focus on outcomes rather than processes will likely extract more value from context orchestration.

### 2. Domain Context + AI Experience + IT Infrastructure

Will Larson, reflecting on enterprise AI adoption, identifies three critical components for success: "Real AI adoption on real problems is a complex blend of domain context on the problem, domain experience with AI tooling, and old-fashioned IT issues" [13]. This explains why smaller companies often implement AI more successfully—they can find all three elements in one or two people, while larger organizations require coordination across multiple departments [13].

This insight provides a framework for evaluating your organization's context orchestration readiness. Do you have:
1. Deep domain knowledge about the problems you're solving
2. Experience with AI tools and their capabilities
3. Infrastructure to support AI implementation

Jaana Dogan's experience at Google reinforces this pattern. Despite Google's resources, their distributed agent orchestrator project faced alignment challenges across teams [3]. Meanwhile, Dogan was able to recreate a year's worth of work in an hour using Claude Code with a simple three-paragraph prompt [3]. The difference wasn't technical capability but effective context orchestration.

### 3. From Labor to Leverage: The Jevons Paradox for Knowledge Work

Aaron Levie predicts that Jevons paradox is coming to knowledge work: "By making it far cheaper to take on any type of task that we can possibly imagine, we're ultimately going to be doing far more" [19]. This suggests that AI won't simply replace existing work but will enable entirely new categories of work that weren't previously possible [19].

Armin Ronacher frames this shift elegantly: "The puzzle is still there. What's gone is the labor... The thinking remains; the hitting of the keys and the frustrating is what's been removed" [4]. This distinction between value-creating thinking and mechanical labor is crucial for leaders orchestrating context. Your role isn't being automated—it's being amplified through better context management.

The result is that people who had stopped coding due to time constraints (like new parents or those in management roles) are returning to technical work because AI assistance allows them to get useful work done in short time periods [10]. The key insight: AI doesn't just make existing processes faster—it changes what's possible within your time constraints.

## Context Orchestration Tools: What Leaders Need to Know

### Vector Databases: Making Organizational Memory Searchable

Weaviate's 1.35 release introduces several features that enhance context orchestration capabilities [18]. The most significant for leaders is Object Time-to-Live (TTL), which enables automatic deletion of objects after a specified time period [18]. This addresses a critical context orchestration challenge: ensuring AI systems don't access outdated information.

The release also expands multimodal document embeddings support, making it easier to build powerful document retrieval applications [18]. For leaders, this means your organizational knowledge—including images, text, and other media—can be more effectively surfaced at decision time.

### Model Context Protocol (MCP): System Access Without Manual Copy-Paste

The Model Context Protocol (MCP) specification saw widespread adoption in early 2025, with OpenAI, Anthropic, and Mistral all rolling out API-level support within eight days of each other [16]. MCP allows AI systems to access your organization's systems without manual copy-paste, dramatically reducing context switching costs.

However, the meteoric rise of coding agents may make MCP "a one-year wonder" as the best possible tool for any situation appears to be giving AI agents access to run shell commands [16]. This represents a shift from structured context protocols to more flexible, agent-based approaches.

### Retrieval-Augmented Generation (RAG): Surfacing Relevant Knowledge at Decision Time

The Software Heritage archive demonstrates the power of effective knowledge retrieval systems. When a valuable open-source library disappeared from GitHub, Simon Willison was able to recover it from the Software Heritage archive [1]. This illustrates a key context orchestration principle: ensuring critical information remains accessible even when primary sources disappear.

Willison created a Software Heritage Repository Retriever tool to simplify this process [1], highlighting how leaders can build systems that make context retrieval more efficient. The lesson for leaders: your organization's knowledge is only valuable if it can be surfaced at the right moment.

## Tensions & Tradeoffs in Context Orchestration

### Security vs. Accessibility

Addy Osmani's insights from 14 years at Google highlight a fundamental tension in context orchestration: "With enough users, every observable behavior becomes a dependency—regardless of what you promised" [11]. This means that how you expose information to AI systems creates implicit dependencies that can be difficult to change later.

Leaders must carefully consider what context they make available to AI systems, as users will build workflows around whatever is accessible. As Osmani notes, "Someone is scraping your API, automating your quirks, caching your bugs" [11]. This requires thoughtful design of context access patterns from the beginning.

### Process vs. Outcomes

The tension between process-focused and outcome-focused approaches to AI adoption represents a fundamental challenge for leaders [9]. Those who derive meaning from the engineering process itself may resist AI tools that automate parts of that process, while those focused on outcomes may embrace them enthusiastically.

Leaders must navigate this cultural tension by emphasizing that context orchestration is about amplifying human capabilities, not replacing them. As Jason Gorman notes, "The hard part of programming has always been—and likely will continue to be for many years to come—knowing exactly what to ask for" [20]. This human skill of problem formulation remains essential.

### Compatibility vs. Innovation

D. Richard Hipp's comparison of SQLite and PostgreSQL approaches to software quality highlights different philosophies that apply to context orchestration [23]. SQLite's "aviation grade testing" allows them to "change code fearlessly" while maintaining quality, whereas PostgreSQL relies on "not messing with code that has worked for 10 years" [23].

Leaders must decide whether their context orchestration approach will prioritize stability (keeping context systems consistent) or innovation (continuously evolving how context is managed). Both approaches can work, but they require different organizational structures and testing methodologies.

## Your Context Orchestration Stack: What to Evaluate This Quarter

1. **Context Curation**: How are you deciding what information to give AI access to? Consider implementing Object TTL for automatic context pruning [18].

2. **Context Sequencing**: Are you providing information at the right time? Evaluate whether your current approach surfaces relevant knowledge at decision points.

3. **Tool Integration**: Does your AI have access to the right tools? Consider whether MCP or agent-based approaches better suit your needs [16].

4. **Memory Systems**: How are you preserving organizational knowledge? Ensure critical information is archived in retrievable formats [1].

5. **Management Practices**: Are you applying management skills to AI interactions? Train leaders to communicate clearly, set achievable goals, and provide relevant context [10].

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

[19] Simon Willison. (2025, December 29). Quoting Aaron Levie. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/aaron-levie/#atom-everything

[20] Simon Willison. (2025, December 29). Quoting Jason Gorman. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/jason-gorman/#atom-everything

[21] Simon Willison. (2025, December 29). shot-scraper 1.9. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/shot-scraper/#atom-everything

[22] Simon Willison. (2025, December 30). Quoting Liz Fong-Jones. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/30/liz-fong-jones/#atom-everything

[23] Simon Willison. (2025, December 29). Quoting D. Richard Hipp. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/d-richard-hipp/#atom-everything