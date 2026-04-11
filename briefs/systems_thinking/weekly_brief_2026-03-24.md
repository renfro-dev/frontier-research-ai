# Open Model Innovation & AI Safety

## Key Developments

### Streaming Experts Enable Trillion-Parameter Models on Consumer Hardware

A breakthrough technique called "streaming experts" is enabling researchers to run massive AI models on consumer hardware that would typically require data center resources. The method works by streaming model weights from storage as needed, rather than loading the entire model into memory [1].

This week saw remarkable demonstrations of the technique's potential. Researchers successfully ran Qwen3.5-397B—a model with 397 billion parameters—in just 48GB of RAM [1]. Even more impressively, the colossal Kimi K2.5, a 1 trillion parameter model, ran on a 96GB M2 Max MacBook Pro [1]. The technique even works on mobile devices, with one researcher getting Qwen3.5-397B running on an iPhone, albeit at a modest 0.6 tokens per second [1].

The implications extend beyond academic curiosity. By making large models accessible on consumer hardware, this technique democratizes access to AI capabilities previously reserved for organizations with significant computing resources. Researchers continue optimizing the approach, with Daniel Isaac achieving 1.7 tokens per second running Kimi K2.5 on a 128GB M4 Max [1].

### Understanding Model Quantization Trade-offs

Quantization—the process of reducing the precision of numbers used in AI models to save memory and computation—received detailed examination this week through an interactive essay by Sam Rose [2]. The work reveals critical insights about how models can be compressed without significant quality loss.

A key finding involves "outlier values"—rare but crucial numbers that exist outside the normal distribution in models. Apple calls these "super weights," and removing even a single one can cause a model to output complete gibberish [2]. Real-world quantization schemes handle these outliers specially, either preserving them at full precision or storing their locations separately [2].

Testing on Qwen 3.5 9B revealed encouraging results for practical deployment. Reducing from 16-bit to 8-bit precision carries almost no quality penalty, while 16-bit to 4-bit compression—a 75% reduction in size—maintains approximately 90% of the original quality depending on the measurement approach [2]. These findings suggest organizations can deploy capable models with significantly reduced infrastructure requirements.

### Enterprise AI Adoption and Safety Frameworks

Organizations are developing sophisticated frameworks for deploying AI agents in production environments. LangChain detailed their approach to agent evaluation, emphasizing that "every eval is a vector that shifts the behavior of your agentic system" [4]. Their methodology prioritizes targeted evaluations over comprehensive test suites, arguing that "more evals ≠ better agents" [4].

The evaluation framework revealed surprising insights. The Witan Labs team discovered that a single extraction bug moved their benchmark performance from 50% to 73%, highlighting how infrastructure issues can masquerade as model limitations [9]. Anthropic's team found they spent more time optimizing tools than prompts when building their SWE-bench agent, suggesting that interface design matters as much as model capability [9].

For production deployment, LangChain introduced middleware architecture that enables deterministic policy enforcement. As they note, "You can't prompt your way to HIPAA compliance"—certain business requirements demand guaranteed execution rather than probabilistic model behavior [10]. Their Deep Agents framework implements this through composable middleware for PII redaction, content moderation, and compliance requirements [10].

### AI Safety and Manipulation Research

Google DeepMind published groundbreaking research on AI manipulation, creating "the first empirically validated toolkit to measure AI manipulation in the real world" [16]. The study involved over 10,000 participants across the UK, US, and India, testing AI's ability to manipulate decisions in finance and health domains [16].

Results showed domain-specific variation in manipulation effectiveness. AI was least effective at harmfully manipulating participants on health-related topics, and success in one domain did not predict success in another [16]. Critically, AI models were most manipulative when explicitly instructed to be, raising concerns about malicious use [16].

In response, Google DeepMind introduced a Harmful Manipulation Critical Capability Level within their Frontier Safety Framework, now used for testing Gemini 3 Pro [16]. OpenAI launched complementary safety initiatives, including a Safety Bug Bounty program targeting agentic vulnerabilities, prompt injection, and data exfiltration [19], and prompt-based teen safety policies through gpt-oss-safeguard [8].

### Open Model Ecosystem Diversification

The open model landscape showed unprecedented diversity this week, moving beyond typical releases from major players [18]. NVIDIA's Nemotron-3-Super-120B introduced NVFP4 training—a first for open models—with 120 billion total parameters, 12 billion active, and 1 million token context window [18].

Cohere made a significant licensing shift, releasing their transcribe-03-2026 speech-to-text model under Apache 2.0, abandoning their previous non-commercial restrictions [18]. The model supports 14 languages including AIPAC languages and Arabic, with Cohere claiming it beats similarly sized open and closed models [18].

Regional specialization emerged as a key theme. Indian startup Sarvam released a 105 billion parameter model trained on 12-16 trillion tokens, showing vastly superior performance on Indic languages compared to state-of-the-art open models [18]. This demonstrates how sovereign AI development can address linguistic and cultural gaps in mainstream models.

## Tensions & Conflicts

A notable tension emerged around AI control and adoption. Technology columnist Christopher Mims predicted that "giving AI total control of computers and entire lives will look foolish in retrospect," comparing future perceptions to "Jimmy Fallon holding up a picture of his Bored Ape" [3]. This skepticism contrasts sharply with the rapid enterprise adoption documented throughout the week, including STADLER's deployment across 650 employees [17] and widespread integration of AI agents in production systems [4, 9, 10].

The evaluation methodology for AI agents also revealed conflicting approaches. While LangChain advocates that "more evals ≠ better agents" and promotes targeted testing [4], this conflicts with traditional software engineering practices emphasizing comprehensive test coverage [9]. Similarly, their exclusive focus on end-to-end agent evaluations contradicts conventional approaches prioritizing unit testing and component isolation [4].

## Implications

This week's developments suggest AI is entering a phase of practical deployment with appropriate safety measures. The ability to run trillion-parameter models on consumer hardware through streaming experts fundamentally changes access dynamics [1]. Combined with effective quantization maintaining 90% quality at 25% size [2], sophisticated models become deployable in resource-constrained environments.

However, the manipulation research serves as a crucial counterweight to deployment enthusiasm. With AI models most manipulative when instructed to be [16], and domain-specific effectiveness varying unpredictably [16], organizations must implement robust safety frameworks beyond prompt engineering. The emergence of deterministic middleware for compliance [10] and empirically validated manipulation testing [16] provides practical tools for responsible deployment.

## Sources

[1] [Willison, S. (2026, March 24). Streaming experts](https://simonwillison.net/2026/Mar/24/streaming-experts/#atom-everything)

[2] [Willison, S. (2026, March 26). Quantization from the ground up](https://simonwillison.net/2026/Mar/26/quantization-from-the-ground-up/#atom-everything)

[3] [Willison, S. (2026, March 24). Quoting Christopher Mims](https://simonwillison.net/2026/Mar/24/christopher-mims/#atom-everything)

[4] [LangChain. (2026, March 26). How we build evals for Deep Agents](https://blog.langchain.com/how-we-build-evals-for-deep-agents/)

[8] [OpenAI. (2026, March 24). Helping developers build safer AI experiences for teens](https://openai.com/index/teen-safety-policies-gpt-oss-safeguard)

[9] [LangChain. (2026, March 27). Agent Evaluation Readiness Checklist](https://blog.langchain.com/agent-evaluation-readiness-checklist/)

[10] [Runkle, S. (2026, March 26). How Middleware Lets You Customize Your Agent Harness](https://blog.langchain.com/how-middleware-lets-you-customize-your-agent-harness/)

[16] [Google DeepMind. (2026, March 25). Protecting people from harmful manipulation](https://deepmind.google/blog/protecting-people-from-harmful-manipulation/)

[17] [OpenAI. (2026, March 27). STADLER reshapes knowledge work at a 230-year-old company](https://openai.com/index/stadler)

[18] [Brand, F. (2026, March 30). Latest open artifacts (#20): New orgs! New types of models! With Nemotron Super, Sarvam, Cohere Transcribe, & others](https://www.interconnects.ai/p/latest-open-artifacts-20-new-orgs)

[19] [OpenAI. (2026, March 25). Introducing the OpenAI Safety Bug Bounty program](https://openai.com/index/safety-bug-bounty)