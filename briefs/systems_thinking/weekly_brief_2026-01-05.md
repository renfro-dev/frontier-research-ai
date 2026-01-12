# AI Development Shifts: Traces, Sandboxes, and Model Competition

## AI Development Paradigm Shifts

This week, Harrison Chase from LangChain published an influential analysis of how AI development fundamentally differs from traditional software engineering. In AI systems, particularly agents, "code is just scaffolding" that orchestrates LLM calls, while the actual decision logic happens in the model at runtime [[1]](#ref-1). This creates a profound shift in how developers must approach their work - the source of truth moves from code to "traces" (records of agent actions) [[1]](#ref-1). Unlike traditional software where the same inputs with the same code produce identical outputs, AI agents can generate different outputs each time, making debugging, testing, and monitoring fundamentally different processes [[1]](#ref-1).

This paradigm shift extends to how developers interact with their tools. Nathan Lambert notes that Claude Code with Opus 4.5 has seen a significant performance jump in recent weeks, creating new workflows where developers repeatedly engage with the AI assistant [[2]](#ref-2). Lambert predicts that "software engineering will look very different by the end of 2026" as AI models become increasingly capable of replicating most commonly-used software [[2]](#ref-2). This transition may favor smaller organizations and startups with greater flexibility to adapt to AI-driven development approaches [[2]](#ref-2).

The shift toward AI-assisted development is accelerating rapidly. Simon Willison predicts that "in 2026, it will become undeniable that LLMs write good code," noting that his own hand-written code has already dropped to a single-digit percentage of his overall output after the release of Claude Opus 4.5 and GPT-5.2 in late 2025 [[13]](#ref-13). Willison suggests that typing code by hand will eventually "go the way of punch cards," becoming an outdated practice as AI assistance becomes the norm [[13]](#ref-13).

## Secure Sandboxing Solutions

As AI coding agents become more powerful, the need for secure environments to run them safely has become critical. This week, Fly.io launched Sprites.dev, a new product that addresses both developer sandboxes and API sandboxes simultaneously [[14]](#ref-14). Sprites provides persistent virtual environments with approximately 8GB RAM and 8 CPU that come pre-installed with coding tools including Claude Code, Codex, Gemini CLI, Python 3.13, and Node.js 22.20 [[14]](#ref-14).

The timing is significant, as Simon Willison had just predicted that "we're due a Challenger disaster with respect to coding agent security" due to the common practice of running coding agents in "dangerously-skip-permissions mode" (also called "YOLO mode") [[14]](#ref-14). Sprites addresses this risk by providing a robust sandbox where "the worst thing that can happen is the sandbox gets messed up and you have to throw it away and get another one" [[14]](#ref-14).

A particularly innovative feature of Sprites is its checkpoint system, which captures the entire disk state in around 300ms, allowing users to roll back to previous states [[14]](#ref-14). This is especially valuable when running untrusted code, as users can checkpoint a clean environment, run potentially risky code, then roll back when finished [[14]](#ref-14). Sprites also offers a JSON API with client libraries in Go and TypeScript (with Python and Elixir coming soon), allowing programmatic control of sandboxed environments [[14]](#ref-14).

The importance of sandboxing technology extends beyond coding agents. Earlier this week, Simon Willison highlighted Luis Cardoso's comprehensive guide to the sandboxing landscape, which differentiates between containers (which share the host kernel), microVMs (with their own guest kernel behind hardware virtualization), gVisor userspace kernels, and WebAssembly/isolates that constrain everything within a runtime [[9]](#ref-9). Willison emphasized that "using the right sandboxes to safely run untrusted code is one of the most important problems to solve in 2026" [[9]](#ref-9).

## Open Model Competition Intensifies

The competition in open AI models continues to accelerate, with Chinese models maintaining their lead while new challengers emerge. Nathan Lambert's analysis shows that Qwen dominates adoption metrics among Chinese labs, with its December downloads outnumbering all other tracked organizations combined [[11]](#ref-11). Despite significant media attention to new open frontier model providers, their actual adoption "tends to look like a rounding error in adoption metrics" [[11]](#ref-11).

This week saw several significant model releases. NVIDIA updated their Nemotron series with a Mamba2-Transformer architecture and Mixture of Experts (MoE) approach, while announcing plans to release two more model sizes in the first half of 2026: Super (~100B-A10B) and Ultra (~500B-A50B) [[15]](#ref-15). Arcee released two models (Nano and Mini) with plans to release a larger 420B-A13B MoE model trained on 20T tokens "in the coming weeks" [[15]](#ref-15).

Chinese companies continue to make strong contributions to the open model ecosystem. Zhipu released GLM-4.7, which performs well on a broad suite of tasks despite not being close to state-of-the-art on academic benchmarks [[15]](#ref-15). In some areas, particularly UI generation for websites, Lambert found GLM-4.7's outputs superior to Claude Opus, though the model has limitations in speed and long-context performance [[15]](#ref-15). Xiaomi surprised the community by releasing MiMo-V2-Flash, a 309B-A15B MoE model, representing a significant leap from their previous 7B dense model [[15]](#ref-15).

DeepSeek released V3.2 and a "high compute" version called V3.2 Speciale, which claims to achieve gold-medal performance on the 2025 International Mathematical Olympiad (IMO) and International Olympiad in Informatics (IOI) [[15]](#ref-15). This continues the trend of specialized models achieving remarkable results in specific domains.

## Multi-Model Workflows Emerge

As the AI landscape becomes more diverse, power users are developing workflows that leverage multiple models for different tasks. Nathan Lambert describes using different models based on their specific strengths: GPT 5.2 Pro for research when accuracy is important, Claude Opus 4.5 for processing raw data and editing, and occasionally Grok for finding AI news from X (formerly Twitter) [[3]](#ref-3). Lambert notes that while open models haven't been "remotely close" to Claude 4.5 Opus or GPT 5.2 Thinking in his experience, they cost approximately 10 times less than frontier lab plans [[3]](#ref-3).

Lambert observes that as AI capabilities diffuse throughout 2026, speed will become a more important factor in model selection [[3]](#ref-3). Currently, Claude Opus 4.5 "isn't particularly fast compared to many models" but feels faster than GPT Thinking models and is sufficient for his work [[3]](#ref-3). He also notes that GPT 5.2 Thinking "took a big step in long-context capabilities," making it closer to Gemini 3 Pro in this aspect [[3]](#ref-3).

The concept of AI capabilities being "jagged" (unevenly distributed across different tasks) drives this multi-model approach [[3]](#ref-3). Lambert describes how problems with one AI model are often solved by passing the same query to a peer model, illustrating a workflow pattern that maximizes the strengths of different systems [[3]](#ref-3). This approach is particularly valuable for tasks at the "frontier of AI capabilities" where no single model excels at everything [[3]](#ref-3).

## Healthcare AI Expansion

OpenAI made several healthcare-focused announcements this week. They introduced ChatGPT Health, a dedicated experience that securely connects health data and apps with built-in privacy protections and physician-informed design [[4]](#ref-4). They also launched OpenAI for Healthcare, an enterprise-grade AI solution that supports HIPAA compliance while reducing administrative burden and supporting clinical workflows [[6]](#ref-6).

These healthcare initiatives represent part of a broader enterprise strategy from OpenAI. The company also highlighted how Netomi scales enterprise AI agents using GPT-4.1 and GPT-5.2, combining concurrency, governance, and multi-step reasoning for reliable production workflows [[7]](#ref-7). Additionally, they showcased Tolan's voice-first AI companion built with GPT-5.1, which combines low-latency responses, real-time context reconstruction, and memory-driven personalities to enable natural conversations [[5]](#ref-5).

## Tensions & Conflicts

Several significant tensions emerged across this week's developments. The fundamental shift from code to traces as the source of truth in AI systems conflicts with traditional software engineering perspectives where code is the primary artifact containing system logic [[1]](#ref-1). This creates tension in how developers approach testing, with AI systems requiring continuous evaluation in production due to non-determinism, conflicting with traditional approaches that emphasize pre-deployment verification [[1]](#ref-1).

There's also tension around the value proposition of frontier models versus open models. While Lambert claims that frontier models from companies like Anthropic and OpenAI are worth their high cost due to superior capabilities, this conflicts with the view that open models provide sufficient capabilities at much lower prices [[3]](#ref-3). The rapid improvement of open models, particularly from Chinese companies, creates further tension in this space [[11]](#ref-11).

A significant conflict exists around the future of software engineering careers. Willison describes the "Jevons paradox for software engineering," presenting two possible futures: either software engineering careers are devalued as code becomes cheaper to produce, or demand increases so much that these skills become more valuable [[13]](#ref-13). This uncertainty creates tension for professionals in the field.

In the sandboxing space, Fly's approach with persistent sandboxes in Sprites conflicts with the common industry practice of using ephemeral, disposable sandboxes for security [[14]](#ref-14). This represents a fundamental design philosophy difference that may influence how the industry approaches secure environments for AI coding agents.

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