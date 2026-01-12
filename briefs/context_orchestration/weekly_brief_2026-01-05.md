# Context Orchestration: Traces, Sandboxes, and Multi-Model Strategies

This week's developments highlight a critical shift in how leaders should think about AI context management. The focus is moving from simply providing information to AI systems toward orchestrating the entire context ecosystem - from traces that document AI decisions to sandboxes that safely contain AI actions to multi-model strategies that leverage specialized capabilities.

## The Rise of Trace-Based Orchestration

In traditional software, code is the source of truth. When something goes wrong, you read the code. But in AI agents, the code is just scaffolding - the actual decisions happen in the model at runtime [[1]](#ref-1). This represents a fundamental shift in how we understand and debug AI systems.

The source of truth in AI agents is shifting from code to traces - the sequence of steps an agent takes. These traces document the logic of your application: the reasoning at each step, which tools were called and why, the outcomes and timing [[1]](#ref-1). This means that operations you would traditionally perform on code (debugging, testing, profiling, monitoring) now happen on traces instead.

This shift has profound implications for context orchestration:

1. **Debugging becomes trace analysis**: When an AI agent fails, you don't look for bugs in the code - you examine the trace to find where the reasoning went wrong [[1]](#ref-1).

2. **Testing requires trace evaluation**: Since the logic exists in traces rather than code, you need to build pipelines to capture traces and evaluate them [[1]](#ref-1).

3. **Monitoring shifts to decision quality**: An agent can be technically "up" with zero errors but still perform terribly. You need to monitor the quality of decisions, not just system health [[1]](#ref-1).

4. **Collaboration centers on observability**: When the logic isn't in the code, collaboration must happen where the traces are. Teams need to share traces, add comments on specific decision points, and discuss why the agent chose certain paths [[1]](#ref-1).

For leaders, this means investing in good observability - structured tracing that you can search, filter, and compare. Without this, you're essentially working blind when building AI agents [[1]](#ref-1).

## Sandboxes: The Missing Link in Context Safety

One of the most significant developments this week is Fly.io's launch of Sprites.dev, addressing a critical gap in context orchestration: safely running AI agents with access to your systems [[14]](#ref-14).

Running coding agents in "dangerously-skip-permissions" mode (where the agent acts without constantly seeking approval) unlocks tremendous power but creates significant risk. A mistake or malicious prompt injection can damage your system and data [[14]](#ref-14). The safe approach is running these agents in robust sandboxes, where the worst outcome is needing to reset the sandbox [[14]](#ref-14).

Sprites.dev offers:

1. **Persistent environments**: Each Sprite gets a proper filesystem that persists between sessions, even while the Sprite itself shuts down after inactivity [[14]](#ref-14).

2. **Checkpoint capabilities**: You can trigger checkpoints that capture the entire disk state in around 300ms, allowing you to roll back to previous states [[14]](#ref-14).

3. **Network policy control**: You can configure network access policies using DNS-based allow/deny lists, controlling what resources your AI agents can access [[14]](#ref-14).

This development addresses what Simon Willison predicted earlier this week: "We're due a Challenger disaster with respect to coding agent security" [[14]](#ref-14). Using sandboxes for context orchestration isn't just about technical safety - it's about creating environments where AI can safely experiment with your systems.

Luis Cardoso's guide to sandboxing, highlighted by Willison, provides additional context by differentiating between containers (which share the host kernel), microVMs (with their own guest kernel behind hardware virtualization), gVisor userspace kernels, and WebAssembly/isolates that constrain everything within a runtime [[9]](#ref-9). Understanding these distinctions is crucial for leaders deciding how to safely deploy AI agents.

## Multi-Model Orchestration Strategies

Another key development in context orchestration is the growing recognition that no single AI model excels at everything. Nathan Lambert's analysis reveals how leaders can gain leverage by strategically orchestrating multiple models for different tasks [[3]](#ref-3).

Lambert describes using:
- GPT 5.2 Pro for research when accuracy is important
- Claude Opus 4.5 for processing raw data and editing
- Grok monthly for finding AI news from X
- Open models for cost-effective coding plans [[3]](#ref-3)

This multi-model approach isn't just about having options - it's about recognizing that AI capabilities are "jagged" (unevenly distributed across tasks) and orchestrating the right context for each situation [[3]](#ref-3). Lambert notes that using only one model would mean "taking a substantial haircut in capabilities" [[3]](#ref-3).

For leaders, this suggests a context orchestration strategy where different models are deployed based on task requirements:
- Frontier models (like GPT 5.2 Pro) for high-stakes research
- Specialized models for specific domains
- Cost-effective open models for routine tasks

As AI capabilities diffuse in 2026, Lambert predicts that speed will become more of a determining factor in model selection [[3]](#ref-3). This means leaders should consider not just what context to provide, but how quickly models can process that context.

## The Claude Code Phenomenon

Claude Code with Opus 4.5 has generated significant excitement this week, with Nathan Lambert noting a "meaningful jump in coding agent performance" [[2]](#ref-2). What makes this development particularly interesting from a context orchestration perspective is that the performance improvement seemed to come weeks after the model's integration with Opus, suggesting that product changes may have unlocked massive gains [[2]](#ref-2).

The key insight is that Claude Code isn't restricted to software development - it can control your entire computer, managing email, calendars, decision making, and other functions [[2]](#ref-2). This represents a shift from narrow context orchestration (giving AI access to code) to broad context orchestration (giving AI access to your entire digital environment).

Lambert predicts that software engineering will look very different by the end of 2026, with AI models able to replicate most-used software fairly easily [[2]](#ref-2). This transition will favor small organizations and startups with flexibility, potentially rebalancing the tech industry [[2]](#ref-2).

## Enterprise Context Orchestration

Several enterprise-focused developments this week highlight how organizations are orchestrating context at scale:

1. **OpenAI for Healthcare** enables secure, enterprise-grade AI that supports HIPAA compliance while reducing administrative burden and supporting clinical workflows [[6]](#ref-6). This represents a specialized context orchestration approach for the healthcare sector, where privacy and compliance are paramount.

2. **ChatGPT Health** securely connects health data and apps with privacy protections and physician-informed design [[4]](#ref-4). This shows how context orchestration in healthcare requires specialized knowledge and careful data handling.

3. **Netomi** is scaling enterprise AI agents using GPT-4.1 and GPT-5.2, combining concurrency, governance, and multi-step reasoning for reliable production workflows [[7]](#ref-7). This demonstrates how enterprise context orchestration requires additional layers of governance and reliability.

4. **Tolan** built a voice-first AI companion with GPT-5.1 that combines low-latency responses, real-time context reconstruction, and memory-driven personalities [[5]](#ref-5). This shows how context orchestration extends to voice interfaces, where maintaining conversational context is crucial.

5. **Datadog** is using Codex for system-level code review [[8]](#ref-8), though details of the implementation are limited in the available information.

## Open Model Ecosystem

The open model ecosystem continues to evolve rapidly, with several notable developments this week:

1. **NVIDIA** released an update to their Nemotron series with a Mamba2-Transformer architecture and MoE, and announced plans for two more model sizes in H1 2026: Super (~100B-A10B) and Ultra (~500B-A50B) [[15]](#ref-15).

2. **Arcee** released two models (Nano and Mini) and plans to release a larger model soon [[15]](#ref-15).

3. **GLM-4.7** by Zhipu performs well on broader tasks despite not being close to state-of-the-art on academic benchmarks [[15]](#ref-15).

4. **DeepSeek** released V3.2 and V3.2 Speciale, with the latter claiming to beat the 2025 IMO and IOI with gold-medal performance [[15]](#ref-15).

These developments suggest that open models are becoming increasingly capable, with GLM 4.7 and MiniMax M2.1 starting to be "good enough" in the Claude Code form factor [[15]](#ref-15). This provides leaders with more options for context orchestration, potentially at lower cost.

## Tensions & Tradeoffs in Context Orchestration

Several key tensions emerge from this week's developments:

1. **Code vs. Traces**: Traditional software engineering focuses on code as the source of truth, while AI agent development shifts focus to traces [[1]](#ref-1). Leaders must decide how to balance these approaches in hybrid systems.

2. **Security vs. Autonomy**: Running AI agents with full permissions increases productivity but creates security risks [[14]](#ref-14). Sandboxes provide a middle ground but require additional infrastructure.

3. **Single Model vs. Multi-Model**: Using a single model simplifies orchestration but sacrifices capabilities, while using multiple specialized models increases complexity but maximizes performance [[3]](#ref-3).

4. **Frontier Models vs. Open Models**: Frontier models from major labs offer cutting-edge capabilities at premium prices, while open models provide cost-effective alternatives with some performance tradeoffs [[3]](#ref-3) [[15]](#ref-15).

5. **Speed vs. Intelligence**: As AI capabilities diffuse, speed is becoming more important in model selection, creating a tradeoff between thorough reasoning and quick responses [[3]](#ref-3).

## Your Context Orchestration Stack

Based on this week's developments, leaders should evaluate:

1. **Trace Observability**: Do you have systems in place to capture, analyze, and learn from AI agent traces?

2. **Sandbox Strategy**: How are you safely running AI agents with system access? Are you using appropriate sandboxing technologies?

3. **Multi-Model Approach**: Have you identified which models excel at which tasks for your specific needs?

4. **Enterprise Governance**: If deploying AI at scale, do you have appropriate governance, concurrency, and reasoning frameworks?

5. **Open Model Integration**: Are you leveraging cost-effective open models where appropriate while maintaining frontier model access for critical tasks?

The context orchestration landscape is evolving rapidly, with traces replacing code as the source of truth, sandboxes enabling safe AI experimentation, and multi-model strategies maximizing capabilities while managing costs. Leaders who master these orchestration patterns will gain significant leverage in 2026.

## Sources

<a id="ref-1"></a>[1] [Chase, H. (2026, January 10). In software, the code documents the app. In AI, the traces do.](https://blog.langchain.com/in-software-the-code-documents-the-app-in-ai-the-traces-do/)

<a id="ref-2"></a>[2] [Lambert, N. (2026, January 9). Claude Code Hits Different](https://www.interconnects.ai/p/claude-code-hits-different)

<a id="ref-3"></a>[3] [Lambert, N. (2026, January 11). Use multiple models](https://www.interconnects.ai/p/use-multiple-models)

<a id="ref-4"></a>[4] [OpenAI Blog. (2026, January 7). Introducing ChatGPT Health](https://openai.com/index/introducing-chatgpt-health)

<a id="ref-5"></a>[5] [OpenAI Blog. (2026, January 7). How Tolan builds voice-first AI with GPT-5.1](https://openai.com/index/tolan)

<a id="ref-6"></a>[6] [OpenAI Blog. (2026, January 8). OpenAI for Healthcare](https://openai.com/index/openai-for-healthcare)

<a id="ref-7"></a>[7] [OpenAI Blog. (2026, January 8). Netomi's lessons for scaling agentic systems into the enterprise](https://openai.com/index/netomi)

<a id="ref-8"></a>[8] [OpenAI Blog. (2026, January 9). Datadog uses Codex for system-level code review](https://openai.com/index/datadog)

<a id="ref-9"></a>[9] [Willison, S. (2026, January 6). A field guide to sandboxes for AI](https://simonwillison.net/2026/Jan/6/a-field-guide-to-sandboxes-for-ai/#atom-everything)

<a id="ref-10"></a>[10] [Willison, S. (2026, January 7). Quoting Robin Sloan](https://simonwillison.net/2026/Jan/7/robin-sloan/#atom-everything)

<a id="ref-11"></a>[11] [Lambert, N. (2026, January 7). 8 plots that explain the state of open models](https://www.interconnects.ai/p/8-plots-that-explain-the-state-of)

<a id="ref-12"></a>[12] [Willison, S. (2026, January 8). How Google Got Its Groove Back and Edged Ahead of OpenAI](https://simonwillison.net/2026/Jan/8/how-google-got-its-groove-back/#atom-everything)

<a id="ref-13"></a>[13] [Willison, S. (2026, January 8). LLM predictions for 2026, shared with Oxide and Friends](https://simonwillison.net/2026/Jan/8/llm-predictions-for-2026/#atom-everything)

<a id="ref-14"></a>[14] [Willison, S. (2026, January 9). Fly's new Sprites.dev addresses both developer sandboxes and API sandboxes at the same time](https://simonwillison.net/2026/Jan/9/sprites-dev/#atom-everything)

<a id="ref-15"></a>[15] [Brand, F. (2026, January 5). Latest open artifacts (#17): NVIDIA, Arcee, Minimax, DeepSeek, Z.ai and others close an eventful year on a high note](https://www.interconnects.ai/p/latest-open-artifacts-17-nvidia-arcee)