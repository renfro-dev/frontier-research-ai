# Context Orchestration: When AI Models Stream From Your SSD

This week saw steady progress in context orchestration tooling rather than fundamental shifts. The most notable development: streaming experts—a technique that lets you run trillion-parameter models on consumer hardware by orchestrating which model components to load when [1]. This same meta-skill of dynamic context management appears across agent evaluation frameworks, enterprise deployments, and new safety considerations.

## Streaming Experts: Context Orchestration at the Model Level

The breakthrough isn't just running massive models on limited hardware—it's the orchestration principle underneath. Dan Woods demonstrated Qwen3.5-397B-A17B running in 48GB of RAM [1]. The technique works by "streaming the necessary expert weights from SSD for each token that you process" [1]. Think of it as just-in-time context loading for the model itself.

This week's implementations pushed boundaries further. @seikixtc ran Kimi K2.5—a 1 trillion parameter model—in 96GB of RAM on an M2 Max MacBook Pro [1]. @anemll got Qwen3.5-397B-A17B working on an iPhone at 0.6 tokens/second [1]. Daniel Isaac achieved Kimi K2.5 on a 128GB M4 Max at ~1.7 tokens/second [1].

For leaders, streaming experts demonstrates a core context orchestration pattern: you don't need everything loaded at once. Just as you wouldn't give an AI assistant your entire company knowledge base for every query, these models only load the specific expert weights needed for each token. The same principle applies to RAG systems, vector databases, and agent memory—orchestrate what's needed when it's needed.

## Agent Evaluation: Teaching Context Through Testing

LangChain released two complementary frameworks this week that reveal how context orchestration shapes agent behavior [4][9]. Their core insight: "Every eval is a vector that shifts the behavior of your agentic system" [4]. When an evaluation for efficient file reading fails, developers "tweak the system prompt or the read_file tool description" [4]—they're orchestrating context to guide behavior.

The evaluation readiness checklist emphasizes starting simple: "A few end-to-end evals that test whether your agent completes its core tasks will give you a baseline immediately" [9]. Before building infrastructure, "spend 30 minutes reading through real agent traces" to learn failure patterns [9]. The Witan Labs team discovered that fixing a single extraction bug moved their benchmark from 50% to 73% [9].

For context orchestration, the key lesson is decomposition. Rather than one monolithic correctness evaluator, Witan Labs built "5 specialized evaluators (content accuracy, structure, visual formatting, formula scenarios, text quality)" [9]. Each evaluator focuses on a specific dimension—just as leaders should decompose their context into specialized domains rather than dumping everything into one prompt.

## Middleware: The Context Orchestration Layer

LangChain's middleware system, detailed this week, shows how to inject context management at every step of agent execution [10]. The architecture is simple: "an LLM, running in a loop, calling tools" with middleware hooks that "let you run custom logic before and after each step" [10].

Critical for leaders: some context management can't live in prompts. "You can't prompt your way to HIPAA compliance" [10]. PII redaction, content moderation, and compliance checks require deterministic enforcement through middleware [10]. LangChain's PIIMiddleware "has the ability to mask/redact/hash PII on model inputs, outputs, and tool outputs" [10].

The system includes pre-built middleware for common patterns [10]:
- **SummarizationMiddleware**: Prevents context overflow by summarizing message history when it exceeds token thresholds
- **LLMToolSelectorMiddleware**: Dynamically selects relevant tools from a registry based on the request
- **ModelRetryMiddleware**: Wraps API calls with retry logic for production reliability
- **ShellToolMiddleware**: Manages setup and teardown of resources around the agent loop

## Enterprise Context Management at Scale

Two enterprise case studies this week demonstrate context orchestration at organizational scale. Kensho built a multi-agent framework called Grounding that "serves as a core access layer for S&P Global data" [11]. The challenge: "Financial professionals often struggle with data retrieval across fragmented systems" [11]. Their solution uses LangGraph to route queries to specialized Data Retrieval Agents owned by different teams—equity research, fixed income, macroeconomics [11].

The key innovation is their DRA protocol, which "established a common data format for all returned data, including both structured and unstructured data" [11]. This standardization "accelerated collaboration and consistent data exchange across our entire multi-agent ecosystem" [11]. New agents get "immediate access to the full breadth of S&P Global data without rebuilding data pipelines" [11].

STADLER, a 230-year-old company, deployed ChatGPT across 650 employees to "transform knowledge work" [17]. While details are limited, the scale suggests significant context orchestration decisions about which organizational knowledge to surface through AI.

## Skills: Portable Context Packages

LangSmith Fleet introduced shareable skills this week—essentially portable context packages [12]. The problem they solve: "Much of the knowledge that makes agents useful lives in people's heads. When someone figures out the right way to handle a task, that knowledge stays with them. When they leave, that knowledge leaves too" [12].

Skills work like "a persistent briefing doc that shapes how the agent behaves for a specific task or domain" [12]. Examples include "how to triage support tickets based on your team's SLA tiers" and "step-by-step workflows for processing refund requests" [12]. The system only loads skills "when it's relevant to what it's doing" [12], keeping agents focused.

The portability matters: "One command installs the skill and links it into your coding agent of choice - Claude Code, Cursor, Codex, or all of them at once" [12]. This solves a key context orchestration challenge—maintaining consistency across different AI tools without manual copying.

## Tensions & Tradeoffs

This week's developments surface several context orchestration tensions:

**Performance vs. Completeness**: Streaming experts trade speed for access—running a trillion-parameter model on an iPhone works but at 0.6 tokens/second [1]. Leaders face similar tradeoffs when deciding how much organizational context to load.

**Standardization vs. Flexibility**: Kensho's DRA protocol standardized data formats across teams [11], enabling integration but potentially constraining innovation. Every context orchestration system faces this balance.

**Automation vs. Control**: LangChain notes that "models are getting more capable, and that will change parts of the middleware stack" [10]. Some current middleware functions like "summarization, tool selection, output trimming—will eventually be absorbed into the model itself" [10]. Leaders must decide which context controls to keep explicit versus trusting to AI.

**Evaluation Overhead**: LangChain warns against the "illusion of 'improving your agent' by scoring well on an eval suite that may not accurately reflect behaviors you care about in production" [4]. More evals don't equal better agents [4]—but how do you know which context matters without testing?

## Your Context Orchestration Stack

Based on this week's developments, evaluate these components:

1. **Dynamic Loading**: Can your systems load context on-demand like streaming experts, or do they require everything upfront?

2. **Evaluation-Driven Context**: Are you using agent failures to identify missing context, as LangChain suggests with their trace review process [9]?

3. **Middleware Hooks**: Do you have deterministic context controls for compliance and safety that can't rely on prompts [10]?

4. **Portable Knowledge**: Can team knowledge be packaged and shared across tools like Fleet's skills [12]?

5. **Routing Intelligence**: For complex organizations, do you have Grounding-style routing to specialized context sources [11]?

The meta-lesson from this week: context orchestration isn't about having more information—it's about having the right information at the right time. Whether streaming model weights from SSD or routing financial queries to domain experts, the winners are those who master selective context loading.

## Sources

[1] [Willison, S. (2026, March 24). Streaming experts](https://simonwillison.net/2026/Mar/24/streaming-experts/#atom-everything)

[4] [LangChain Accounts. (2026, March 26). How we build evals for Deep Agents](https://blog.langchain.com/how-we-build-evals-for-deep-agents/)

[9] [LangChain Accounts. (2026, March 27). Agent Evaluation Readiness Checklist](https://blog.langchain.com/agent-evaluation-readiness-checklist/)

[10] [Runkle, S. (2026, March 26). How Middleware Lets You Customize Your Agent Harness](https://blog.langchain.com/how-middleware-lets-you-customize-your-agent-harness/)

[11] [LangChain Accounts. (2026, March 26). How Kensho built a multi-agent framework with LangGraph to solve trusted financial data retrieval](https://blog.langchain.com/customers-kensho/)

[12] [LangChain Accounts. (2026, March 25). Skills in LangSmith Fleet](https://blog.langchain.com/skills-in-langsmith-fleet/)

[17] [OpenAI Blog. (2026, March 27). STADLER reshapes knowledge work at a 230-year-old company](https://openai.com/index/stadler)