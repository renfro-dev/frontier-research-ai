# AI Safety Tools & Agent Evolution

## key developments

### anthropic restricts claude mythos access for security research

anthropic chose not to release their latest model, claude mythos, through standard channels this week. instead, they made it available only to security researchers through project glasswing [14]. the model demonstrates cybersecurity research abilities strong enough that anthropic believes the software industry needs time to prepare [14].

the capability jump from previous models is significant. while claude opus 4.6 had a near-zero success rate at autonomous exploit development, mythos preview successfully developed working exploits 181 times out of several hundred attempts on firefox vulnerabilities [14]. the model has already found thousands of high-severity vulnerabilities, including some in every major operating system and web browser [14].

security researchers report dramatic improvements in their vulnerability discovery rates. nicholas carlini found more bugs in the last couple of weeks using the model than in the rest of his life combined [14]. the model discovered a bug in openbsd that had been present for 27 years, where sending specific data to any openbsd server could crash it [14]. greg kroah-hartman noted that a month ago the world switched from ai-generated security reports that were obviously wrong to real, good reports [14].

project glasswing includes $100 million in usage credits and $4 million in direct donations to open-source security organizations [14]. anthropic does not plan to make claude mythos preview generally available [14].

### meta launches muse spark as hosted model

meta announced muse spark this week, their first model release since llama 4 almost exactly a year ago [17]. unlike previous llama releases, muse spark is a hosted model rather than open weights, with api access currently limited to select users in private preview [17].

meta's benchmarks show muse spark competitive with opus 4.6, gemini 3.1 pro, and gpt 5.4 on selected benchmarks, though notably behind on terminal-bench 2.0 [17]. artificial analysis scored meta spark at 52, behind only gemini 3.1 pro, gpt-5.4, and claude opus 4.6 [17]. last year's llama 4 maverick and scout scored 18 and 13 respectively [17].

the model is available through meta.ai in two modes: "instant" and "thinking" [17]. meta promises a future "contemplating" mode that will offer much longer reasoning time, similar to gemini deep think or gpt-5.4 pro [17]. according to meta, they achieved these capabilities with over an order of magnitude less compute than their previous model, llama 4 maverick [17].

the meta.ai interface includes 16 different tools, including browser search, content search, image generation, python execution in a sandbox environment, and visual grounding capabilities that can identify and locate objects with pixel-level precision [17].

### langchain positions agent harnesses as critical infrastructure

langchain published multiple perspectives this week on the evolving role of agent harnesses—the orchestration layers that coordinate ai models with tools and memory systems. harrison chase argues that agent harnesses are becoming the dominant way to build agents and are not going anywhere [7].

the evolution of agentic systems has progressed from simple rag chains to complex flows to agent harnesses over the past three years [7]. when claude code's source code was leaked, it contained 512,000 lines of code, demonstrating that even the makers of the best models invest heavily in harnesses [7]. features like web search in openai and anthropic's apis are not part of the model itself but rather lightweight harnesses that orchestrate the model with external apis [7].

memory systems are tightly coupled to harnesses rather than being standalone services. chase argues that asking to plug memory into an agent harness is like asking to plug driving into a car [7]. the ownership of the harness determines control over the memory, with implications for data portability and vendor lock-in [7].

langchain also introduced better-harness, a method for using evaluations to iteratively improve agent harnesses [11]. they describe evaluations as "training data for agents," where each eval case contributes a signal about whether the agent took the right action or produced the right outcome [11]. testing with claude sonnet 4.6 and z.ai's glm-5 showed nearly full generalization to holdout sets after optimization [11].

### deep agents enables asynchronous delegation

langchain released deep agents v0.5 this week, adding support for asynchronous subagents that can delegate work to remote agents running in the background [15]. unlike inline subagents that block the supervisor's execution, async subagents return a task id immediately and execute independently on a remote server [15].

this addresses bottlenecks for work that takes minutes rather than seconds, such as deep research, large-scale code analysis, or multi-step data pipelines [15]. async subagents are stateful and maintain their own thread across interactions, allowing supervisors to send follow-up instructions or course-correct mid-task [15].

any remote agent that implements the agent protocol is a valid target for async subagents, including agents deployed with langsmith, custom fastapi services, or other implementations [15]. the release also extends multimodal support to pdfs, audio, video, and other file types using the same read_file tool with no api change required [15].

### openai responds to axios supply chain attack

openai published their response to the axios developer tool compromise this week [3]. the company rotated macos code signing certificates and updated apps in response to the supply chain attack [3]. openai confirmed that no user data was compromised [3].

### openai launches educational resources

openai released multiple educational resources through their academy this week. new guides cover getting started with chatgpt for writing, brainstorming, and problem-solving [1], using chatgpt to transform rough concepts into structured, actionable plans [2], and specific applications for managers including preparing for conversations, writing clear feedback, and improving team effectiveness [4]. they also introduced guidance on using projects in chatgpt to organize chats, files, and instructions for ongoing work and collaboration [5].

## tensions & conflicts

### open model sustainability challenges

nathan lambert argues that the inevitable need for an open model consortium emerged from recent instability in open model funding [9]. there has been significant turnover in open model labs in recent months, with high-profile departures at qwen and ai2 [9]. the cost of training relevant models is shifting from millions to billions of dollars [9].

releasing frontier models openly is now in active tension with focusing resources on ai products that generate meaningful revenue [9]. lambert predicts an ever-increasing number of companies releasing smaller, custom models but an ever-decreasing number willing to release fully open, near-frontier models [9]. he estimates a meaningful chance that anthropic, openai, and google will be the most valuable companies in the world in the 2030s by owning frontier intelligence [9].

### security capabilities versus open access

the release of claude mythos highlights tensions between advancing ai capabilities and managing security risks. lambert acknowledges that while he has written extensively about how open-weight models will fall behind closed models, cybersecurity may represent a legitimate red line [12]. he notes a 6-18 month delay from when capabilities are available in closed labs to being reproduced in the open [12].

current estimates put leading models like claude opus 4.6 or gpt 5.4 at around 3-5 trillion parameters, while the largest open-source models from chinese labs are around 1 trillion parameters [12]. running an 8 trillion parameter modern mixture-of-experts model requires approximately 100 h100 gpus, costing around $10,000 per day [12].

### voice mode capabilities lag behind text models

simon willison highlights that openai voice mode runs on a much older, much weaker model with a knowledge cutoff of april 2024, indicating it's a gpt-4o era model [8]. this contrasts with openai's highest-tier codex model that can coherently restructure entire code bases or find and exploit vulnerabilities for one hour [8]. domains with explicit reward functions that are verifiable, like unit tests, are more amenable to reinforcement learning training, while writing is much harder to explicitly judge [8]. b2b settings are more valuable, meaning the biggest fraction of teams focus on improving them [8].

## implications

the restriction of claude mythos to security researchers represents a significant shift in how frontier ai capabilities are released. the model's ability to find decades-old vulnerabilities and chain together complex exploits suggests we've crossed a threshold where general release could pose immediate risks to global software infrastructure.

the evolution of agent harnesses into critical infrastructure, combined with the trend toward hosted rather than open models, points to increasing centralization of ai capabilities. organizations deploying ai agents will need to carefully consider the tradeoffs between using proprietary harnesses with vendor lock-in versus building open alternatives that may lag in capabilities.

the growing gap between voice interfaces and text-based models, along with the increasing cost of frontier model training, suggests different ai modalities will continue to diverge in capabilities based on their economic value and technical constraints.

## sources

[1] [OpenAI Blog. (2026, April 10). Getting started with ChatGPT](https://openai.com/academy/getting-started)

[2] [OpenAI Blog. (2026, April 10). Brainstorming with ChatGPT](https://openai.com/academy/brainstorming)

[3] [OpenAI Blog. (2026, April 10). Our response to the Axios developer tool compromise](https://openai.com/index/axios-developer-tool-compromise)

[4] [OpenAI Blog. (2026, April 10). ChatGPT for managers](https://openai.com/academy/managers)

[5] [OpenAI Blog. (2026, April 10). Using projects in ChatGPT](https://openai.com/academy/projects)

[6] [Simon Willison's Weblog. (2026, April 10). Kākāpō parrots](https://simonwillison.net/2026/Apr/10/kakapo/#atom-everything)

[7] [Harrison Chase. (2026, April 11). Your harness, your memory](https://blog.langchain.com/your-harness-your-memory/)

[8] [Simon Willison's Weblog. (2026, April 10). ChatGPT voice mode is a weaker model](https://simonwillison.net/2026/Apr/10/voice-mode-is-weaker/#atom-everything)

[9] [Nathan Lambert. (2026, April 11). The inevitable need for an open model consortium](https://www.interconnects.ai/p/the-inevitable-need-for-an-open-model)

[10] [LangChain Accounts. (2026, April 7). Arcade.dev tools now in LangSmith Fleet](https://blog.langchain.com/arcade-dev-tools-now-in-langsmith-fleet/)

[11] [LangChain Accounts. (2026, April 8). Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://blog.langchain.com/better-harness-a-recipe-for-harness-hill-climbing-with-evals/)

[12] [Nathan Lambert. (2026, April 9). Claude Mythos and misguided open-weight fearmongering](https://www.interconnects.ai/p/claude-mythos-and-misguided-open)

[13] [Simon Willison's Weblog. (2026, April 9). GitHub Repo Size](https://simonwillison.net/2026/Apr/9/github-repo-size/#atom-everything)

[14] [Simon Willison's Weblog. (2026, April 7). Anthropic's Project Glasswing - restricting Claude Mythos to security researchers - sounds necessary to me](https://simonwillison.net/2026/Apr/7/project-glasswing/#atom-everything)

[15] [Chester Curme. (2026, April 7). Deep Agents v0.5](https://blog.langchain.com/deep-agents-v0-5/)

[16] [LangChain Accounts. (2026, April 9). Human judgment in the agent improvement loop](https://blog.langchain.com/human-judgment-in-the-agent-improvement-loop/)

[17] [Simon Willison's Weblog. (2026, April 8). Meta's new model is Muse Spark, and meta.ai chat has some interesting tools](https://simonwillison.net/2026/Apr/8/muse-spark/#atom-everything)