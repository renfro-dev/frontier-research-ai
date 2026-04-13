# context orchestration: the meta-skill hidden in this week's ai developments

## the harness is the context layer

this week's most significant insight came from harrison chase at langchain: "your harness, your memory" [7]. the claim sounds technical, but it reveals something fundamental about context orchestration. when claude code's source was leaked, it contained 512k lines of code [7]. that's not the model. that's the context orchestration layer.

think of it this way: the ai model is like a brilliant consultant who shows up with no context about your business. the harness is everything you build to give that consultant the right information at the right time. memory isn't a separate component you plug in [7]. it's integral to how you orchestrate context.

this matters because every leader using ai is building a harness, whether they realize it or not. when you paste context into chatgpt, you're manually orchestrating. when you use projects in chatgpt to organize chats and files [5], you're building a lightweight harness. when commonwealth bank deploys chatgpt to 50,000 employees, they're orchestrating context at enterprise scale.

## tools are context bridges

meta's new muse spark model demonstrates another context orchestration pattern: tools as context bridges [17]. the model itself doesn't generate images or search the web. instead, it orchestrates 16 different tools [17], each providing access to different context domains.

arcade.dev's integration with langsmith fleet extends this pattern [10]. they provide 7,500+ tools through a single gateway [10]. but here's the key insight: these aren't just api wrappers. arcade's tools are "narrowed to what agents actually need to do, not the full api surface" [10]. that's context curation in action.

the lesson for leaders: every tool you give your ai is a decision about what context to make accessible. too many tools create noise. too few limit capability. the meta-skill is knowing which context bridges to build.

## memory creates leverage through persistence

deep agents v0.5 introduced async subagents that maintain state across interactions [15]. this isn't just a technical feature. it's a fundamental shift in how context persists over time.

consider the practical impact: inline subagents block execution while they run [15]. for tasks taking minutes—deep research, large-scale analysis—the supervisor can't respond or make progress [15]. async subagents solve this by maintaining their own context thread [15].

this mirrors how high-performing teams work. you don't block waiting for every piece of information. you delegate context gathering, continue other work, and check back for results. the ai pattern follows the human pattern.

## human judgment shapes context

langchain's work with hundreds of organizations revealed a critical pattern: "ai agents work best when they reflect the knowledge and judgment your team has built over time" [16]. but most organizational knowledge is tacit—it "lives inside their employees' minds" [16].

teams discover this gap when building agents. the technical capability exists (llms are strong at generating sql [16]), but success requires encoding human judgment into the context layer. this happens through evaluation loops where humans calibrate automated evaluators [16] rather than manually reviewing outputs.

the meta-skill here: knowing which human judgments to encode into your context orchestration. not everything needs automation. but the judgments that shape how context flows to ai—those create leverage.

## security as context boundary

anthropic's project glasswing reveals context orchestration's sharp edge [14]. claude mythos found thousands of high-severity vulnerabilities [14], including bugs in every major operating system [14]. the model's exploit success rate jumped from near-zero to 181 out of several hundred attempts [14].

anthropic's response: restrict context access. they made mythos available only to security researchers [14] rather than general release. this isn't about the model—it's about what context the model can access and act upon.

nathan lambert frames the broader tension: "the best, frontier-level open weight models are going to fall behind the best closed models" [12]. but the real question isn't model capability. it's context access. a weaker model with rich context often outperforms a stronger model with poor context.

## practical applications

**for product teams**: openai's chatgpt academy shows how to package context orchestration for users. managers use chatgpt to "prepare for conversations" and "write clear feedback" [4] by providing the right context at the right time. projects help "organize chats, files, and instructions" [5]—that's context orchestration made visible.

**for engineering leaders**: the "better harness" approach from langchain demonstrates systematic context improvement [11]. evals become "training data for agents" [11], with each failure generating new context rules. one team discovered their agent kept asking for already-provided information, so they added: "do not ask for details the user already supplied" [11].

**for security teams**: mythos shows both opportunity and risk. greg kroah-hartman noted the world switched "from ai-generated security reports that were obviously wrong to real, good reports" [14]. the difference? better context orchestration around vulnerability data.

**for operations**: arcade's gateway pattern offers a solution to tool sprawl. instead of managing individual integrations, teams can use "a single gateway for the whole organization, or a tailored gateway per team" [10]. context orchestration becomes configurable infrastructure.

## tensions and tradeoffs

**context richness vs. privacy**: anthropic's mythos restrictions highlight this tension. more context enables more capability, but also more risk. leaders must decide which contexts to expose.

**curation cost vs. ai utility**: harrison chase notes that memory systems remain "in their infancy" [7]. the effort to curate and maintain context often exceeds the benefit. successful teams focus on high-leverage context first.

**open vs. closed orchestration**: when codex generates "an encrypted compaction summary that is not usable outside of the openai ecosystem" [7], it locks context to a platform. leaders face build-vs-buy decisions about context control.

**synchronous vs. asynchronous context**: deep agents shows the tradeoff between immediate context (blocking inline subagents) and eventual context (async subagents) [15]. different use cases require different context timing.

## your context orchestration stack

evaluate these components this quarter:

1. **memory systems**: where does context persist? harrison chase warns about losing agent memory—he accidentally deleted his email assistant and lost months of context [7].

2. **tool gateways**: how do you manage context bridges? arcade's approach—narrowing tools to what agents need [10]—offers a template.

3. **evaluation loops**: how does human judgment shape context flow? langchain's align evaluator [16] shows one approach to encoding expertise.

4. **access controls**: who can orchestrate which context? anthropic's glasswing [14] and arcade's per-user authorization [10] demonstrate different models.

5. **async patterns**: when should context gathering block vs. continue? deep agents' async subagents [15] provide a technical pattern with business implications.

the winners in ai won't be those with the best models. they'll be those who master context orchestration—the meta-skill of deciding what information to surface, when to surface it, and how to maintain it over time. this week's developments show the patterns emerging. the question is which ones you'll implement.

## sources

[1] [OpenAI Blog. (2026, April 10). Getting started with ChatGPT](https://openai.com/academy/getting-started)

[2] [OpenAI Blog. (2026, April 10). Brainstorming with ChatGPT](https://openai.com/academy/brainstorming)

[3] [OpenAI Blog. (2026, April 10). Our response to the Axios developer tool compromise](https://openai.com/index/axios-developer-tool-compromise)

[4] [OpenAI Blog. (2026, April 10). ChatGPT for managers](https://openai.com/academy/managers)

[5] [OpenAI Blog. (2026, April 10). Using projects in ChatGPT](https://openai.com/academy/projects)

[6] [Willison, S. (2026, April 10). Kākāpō parrots](https://simonwillison.net/2026/Apr/10/kakapo/#atom-everything)

[7] [Chase, H. (2026, April 11). Your harness, your memory](https://blog.langchain.com/your-harness-your-memory/)

[8] [Willison, S. (2026, April 10). ChatGPT voice mode is a weaker model](https://simonwillison.net/2026/Apr/10/voice-mode-is-weaker/#atom-everything)

[9] [Lambert, N. (2026, April 11). The inevitable need for an open model consortium](https://www.interconnects.ai/p/the-inevitable-need-for-an-open-model)

[10] [LangChain Accounts. (2026, April 7). Arcade.dev tools now in LangSmith Fleet](https://blog.langchain.com/arcade-dev-tools-now-in-langsmith-fleet/)

[11] [LangChain Accounts. (2026, April 8). Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://blog.langchain.com/better-harness-a-recipe-for-harness-hill-climbing-with-evals/)

[12] [Lambert, N. (2026, April 9). Claude Mythos and misguided open-weight fearmongering](https://www.interconnects.ai/p/claude-mythos-and-misguided-open)

[13] [Willison, S. (2026, April 9). GitHub Repo Size](https://simonwillison.net/2026/Apr/9/github-repo-size/#atom-everything)

[14] [Willison, S. (2026, April 7). Anthropic's Project Glasswing - restricting Claude Mythos to security researchers - sounds necessary to me](https://simonwillison.net/2026/Apr/7/project-glasswing/#atom-everything)

[15] [Curme, C. (2026, April 7). Deep Agents v0.5](https://blog.langchain.com/deep-agents-v0-5/)

[16] [LangChain Accounts. (2026, April 9). Human judgment in the agent improvement loop](https://blog.langchain.com/human-judgment-in-the-agent-improvement-loop/)

[17] [Willison, S. (2026, April 8). Meta's new model is Muse Spark, and meta.ai chat has some interesting tools](https://simonwillison.net/2026/Apr/8/muse-spark/#atom-everything)