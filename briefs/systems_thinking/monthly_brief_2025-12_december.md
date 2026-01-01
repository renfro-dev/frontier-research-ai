# Systems Thinking Brief: December 2025 - AI Ecosystem Evolution

## Executive Summary

The AI landscape is undergoing profound transformation as open models challenge closed systems, coding agents reshape software development practices, and enterprise AI adoption accelerates. This month's developments reveal how AI is becoming more deeply integrated into business operations, with significant implications for productivity, workforce skills, and competitive dynamics.

For decision-makers, these shifts matter because they're changing the economics of technology development and deployment. Organizations now face critical choices about which AI systems to adopt, how to integrate them into workflows, and how to balance the benefits of AI assistance against potential risks. The growing capabilities of open models are democratizing access to powerful AI, while coding agents are fundamentally changing how software gets built.

Key developments this month include the release of GPT-5.2 and GPT-5.2-Codex by OpenAI, significant advancements in open models from Chinese companies, new approaches to AI safety and evaluation, and the emergence of "vibe engineering" as a collaborative approach between humans and AI for software development.

## Key Developments

### Open Models Challenge Closed Systems

Open models—AI systems where the underlying architecture and weights are publicly available, unlike closed models where the internals are proprietary—have dramatically increased in capability during 2025, now rivaling closed models on most key benchmarks [16]. This shift has significant implications for who controls foundational AI infrastructure and where innovation happens.

Chinese companies have emerged as leaders in the open model space. DeepSeek R1, released in January 2025 under the MIT license, inspired many Chinese labs to release their models openly [16]. Qwen has overtaken Meta's Llama in terms of total downloads and as the most-used base model for fine-tuning [16]. This represents more than a technical milestone—it signals China's growing dominance in open AI development [16].

Despite benchmark parity, closed models still dominate in real-world usage [16]. The best closed models maintain advantages in robustness and richness that open models matching them on benchmarks don't always demonstrate [16]. This month, OpenAI released GPT-5.2, described as their "most advanced frontier model for everyday professional work" with improved reasoning, long-context understanding, coding, and vision capabilities [39]. They followed this with GPT-5.2-Codex, a version further optimized for coding tasks with enhanced cybersecurity capabilities [46, 47].

The open model ecosystem has become incredibly active, with approximately 1,000-2,000 models uploaded to HuggingFace each day [16]. This represents 30,000-60,000 models monthly, highlighting the scale and diversity of development efforts [16]. Models like Moondream have become leading players in the vision space, while others like Parakeet 3 for speech-to-text are faster than cloud-based platforms in terms of end-to-end latency [16].

Late December saw Meta acquire Manus, a Singapore-based AI agent startup with Chinese roots, for over $2 billion [95, 96]. The deal highlighted geopolitical tensions in AI development, with Meta explicitly stating that "there will be no continuing Chinese ownership interest in Manus AI following the transaction" [97]. Manus, which had been backed by Chinese investors including Tencent and ZhenFund, would wind down its operations in China following the acquisition [98].

### Coding Agents Transform Software Development

Coding agents—AI tools that can actively execute code they're working with to check functionality and iterate on problems—represent the most important trend in LLMs in 2025 [87]. These tools are fundamentally changing how software is developed, shifting programmers from writing lines of code to managing the context the model has access to, pruning irrelevant information, adding useful material, and writing detailed specifications [5].

The impact of these tools on productivity is substantial. Boris Cherny, creator of Claude Code, reported landing 259 pull requests and making 497 commits in thirty days using Claude Code with Opus 4.5 [60]. This represents a dramatic improvement from a year ago, when Claude struggled with basic tasks like generating bash commands without escaping issues [60].

Junior developers are using AI coding assistants effectively, not just accepting whatever the AI produces but using it to accelerate learning while maintaining quality [77]. These tools help by collapsing the search space—instead of spending hours figuring out which API to use, developers spend minutes evaluating options the AI surfaced [77]. This compression of the learning curve makes hiring junior developers a better bet for engineering managers [77].

However, there are concerns about how these tools are used. Some junior engineers empowered by LLM tools deposit large, untested pull requests and expect the code review process to handle the rest [87]. This approach is considered rude and a waste of other people's time [87]. The fundamental responsibility remains with the human developer: "Your job is to deliver code you have proven to work" [87]. A computer can never be held accountable; that's the human's job [87].

### Enterprise AI Adoption Accelerates

Enterprise AI adoption is accelerating rapidly, with deeper integration and measurable productivity gains across industries in 2025 [31]. OpenAI reported that more than one million customers around the world now use their services to empower teams and unlock new opportunities [51].

Major financial institutions are implementing AI at scale. Commonwealth Bank of Australia is rolling out ChatGPT Enterprise to 50,000 employees to build AI fluency and improve customer service and fraud response [58]. BBVA is expanding its work with OpenAI through a multi-year AI transformation program, rolling out ChatGPT Enterprise to all 120,000 employees [49]. BNY is using OpenAI technology to expand AI adoption enterprise-wide, with over 20,000 employees building AI agents through their Eliza platform to enhance efficiency and improve client outcomes [42].

Beyond financial services, companies across sectors are integrating AI into their operations. Virgin Atlantic is using AI to speed up development, improve decision-making, and elevate customer experience [30]. Scout24 has created a GPT-5 powered conversational assistant that reimagines real-estate search, guiding users with clarifying questions, summaries, and tailored listing recommendations [35]. Podium implemented GPT-5 to build "Jerry," an AI teammate that drove 300% growth and transformed how small businesses serve customers [40].

OpenAI is forming strategic partnerships to accelerate enterprise AI adoption. They've taken an ownership stake in Thrive Holdings to embed frontier research and engineering into accounting and IT services [21], partnered with Accenture to help enterprises bring agentic AI capabilities into their business core [22], and collaborated with Deutsche Telekom to bring advanced, multilingual AI experiences to millions across Europe [32].

### "Vibe Engineering" Emerges as Collaborative Approach

A new approach to software development called "vibe engineering" has emerged, where expert programmers use coding agents professionally to produce high-quality results [74]. This differs from "vibe coding," which refers to uncritically accepting AI-generated code without proper review [74].

JustHTML, a Python library for parsing HTML released by Emil Stenström, exemplifies this approach [74]. Stenström used VS Code with Github Copilot in Agent mode along with several AI models including Claude Sonnet 3.7, Gemini 3 Pro, and Claude Opus to build the library [74]. He worked on it for a couple of months during off-hours, designing the core API himself while letting the AI handle implementation details [74].

This approach has inspired others to create similar libraries in different programming languages. Simon Willison ported JustHTML from Python to JavaScript using Codex CLI and GPT-5.2 in about 4.5 hours [76]. Anil Madhavapeddy created html5rw in OCaml [88], and Kyle Howells built a dependency-free HTML5 parser for Swift [88]. These projects all pass the comprehensive html5lib-tests conformance suite, demonstrating that AI-assisted development can produce high-quality, standards-compliant code [76, 88].

The division of labor between human and agent is key to this approach. The human acts as the lead architect, providing high-level direction and oversight, while the AI agent handles the implementation details [74]. This allows developers to focus on design decisions and quality control rather than typing code [74].

### New Approaches to AI Safety and Evaluation

As AI capabilities advance, new approaches to safety and evaluation are being developed. OpenAI introduced FrontierScience, a benchmark testing AI reasoning in physics, chemistry, and biology to measure progress toward real scientific research [20]. They also created a framework for evaluating "chain-of-thought monitorability," covering 13 evaluations across 24 environments [56]. This research found that monitoring a model's internal reasoning is far more effective than monitoring outputs alone [56].

For cybersecurity, OpenAI is investing in stronger safeguards and defensive capabilities as AI models become more powerful [36]. They're using automated red teaming trained with reinforcement learning to strengthen ChatGPT Atlas against prompt injection attacks [50]. This proactive discover-and-patch loop helps identify novel exploits early and harden the browser agent's defenses [50].

Researchers are also exploring new training methods to improve AI behavior. OpenAI is testing "confessions," a method that trains models to admit when they make mistakes or act undesirably, helping improve AI honesty, transparency, and trust [27]. Google DeepMind released Gemma Scope 2, making open interpretability tools available for all models in the Gemma 3 family [14].

For teen safety, OpenAI updated its Model Spec with new Under-18 Principles that define how ChatGPT should support teens with safe, age-appropriate guidance grounded in developmental science [48]. They also shared AI literacy resources to help teens and parents use ChatGPT thoughtfully, safely, and with confidence [57].

## Tensions & Conflicts

Several important tensions emerged across this month's developments:

**Benchmark performance vs. real-world utility**: While open models now rival closed models on most key benchmarks, closed models still dominate in real-world usage [16]. This suggests a disconnect between benchmark performance and practical utility that organizations must consider when selecting AI systems.

**Human vs. AI roles in software development**: Different perspectives exist on how AI should be integrated into programming workflows. Some developers value the physical act of writing code and prefer tools like Copilot that enhance productivity while maintaining full control [62]. Others, particularly experienced developers, see their core value in judgment, tradeoffs, and intent, considering manual coding a waste of their time [62]. This reflects a broader tension about whether AI should augment or automate programming tasks.

**AI-generated content quality concerns**: The term "slop" was selected as Merriam-Webster's Word of the Year for 2025, defined as "digital content of low quality that is produced usually in quantity by means of artificial intelligence" [75]. This highlights concerns about AI systems generating low-quality content at scale. An incident where AI agents from the "AI Village" project sent unsolicited emails to prominent technologists like Rob Pike demonstrates the risks of allowing AI systems to interact with the world without human oversight [94].

**Copyright and ethical questions in AI-assisted development**: The rapid porting of software libraries using AI raises questions about copyright, ethics, and impact on the open source ecosystem [76]. When Simon Willison ported JustHTML from Python to JavaScript in 4.5 hours using AI, he questioned whether this represented a legal violation of copyright, whether it was ethical to build a library this way, whether it hurt the open source ecosystem, and whether he could assert copyright over code largely produced by an LLM [76].

## Implications

The developments this month demonstrate how AI is becoming more deeply integrated into business operations and software development practices. Organizations that effectively leverage these technologies can achieve significant productivity gains, but must also navigate complex questions about skill development, workflow integration, and responsible use.

The growing capabilities of open models are democratizing access to powerful AI, potentially shifting the balance of power in the AI ecosystem. Meanwhile, the emergence of "vibe engineering" as a collaborative approach between humans and AI suggests a future where the most successful organizations will be those that effectively combine human expertise with AI capabilities.

## Source Cards

[1] Simon Willison. (2025, December 28). actions-latest. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/28/actions-latest/

[2] Simon Willison. (2025, December 29). Quoting Aaron Levie. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/aaron-levie/

[3] Simon Willison. (2025, December 29). Quoting Jason Gorman. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/jason-gorman/

[4] Simon Willison. (2025, December 29). shot-scraper 1.9. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/shot-scraper/

[5] Simon Willison. (2025, December 30). Quoting Liz Fong-Jones. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/30/liz-fong-jones/

[6] Vicki Boykis. (2025, December 26). Favorite Books of 2025. Vicki Boykis. https://veekaybee.github.io/essays/2025-12-26-favorite-books/

[7] Simon Willison. (2025, December 29). Quoting D. Richard Hipp. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/29/d-richard-hipp/

[8] OpenAI Blog. (2025, December 11). Update to GPT-5 System Card: GPT-5.2. OpenAI Blog. https://openai.com/index/gpt-5-system-card-update-gpt-5-2

[9] OpenAI Blog. (2025, December 16). Measuring AI's capability to accelerate biological research. OpenAI Blog. https://openai.com/index/accelerating-biological-research-in-the-wet-lab

[10] OpenAI Blog. (2025, December 17). Introducing OpenAI Academy for News Organizations. OpenAI Blog. https://openai.com/index/openai-academy-for-news-organizations

[11] Simon Willison. (2025, December 27). textarea.my on GitHub. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/textarea-my/

[12] Google DeepMind Blog. (2025, December 4). Engineering more resilient crops for a warming climate. Google DeepMind Blog. https://deepmind.google/blog/engineering-more-resilient-crops-for-a-warming-climate/

[13] Google DeepMind Blog. (2025, December 11). Deepening our partnership with the UK AI Security Institute. Google DeepMind Blog. https://deepmind.google/blog/deepening-our-partnership-with-the-uk-ai-security-institute/

[14] Google DeepMind Blog. (2025, December 16). Gemma Scope 2: helping the AI safety community deepen understanding of complex language model behavior. Google DeepMind Blog. https://deepmind.google/blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/

[15] Nathan Lambert. (2025, December 10). New Talk: Building Olmo 3 Think. Interconnects. https://www.interconnects.ai/p/building-olmo-3-think

[16] Florian Brand. (2025, December 14). 2025 Open Models Year in Review. Interconnects. https://www.interconnects.ai/p/2025-open-models-year-in-review

[17] Nathan Lambert. (2025, December 18). 2025 Interconnects year in review. Interconnects. https://www.interconnects.ai/p/2025-interconnects-year-in-review

[18] Simon Willison. (2025, December 28). Substack Network error = security content they don't allow to be sent. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/28/substack-network-error/

[19] OpenAI Blog. (2025, December 18). Deepening our collaboration with the U.S. Department of Energy. OpenAI Blog. https://openai.com/index/us-department-of-energy-collaboration

[20] OpenAI Blog. (2025, December 16). Evaluating AI's ability to perform scientific research tasks. OpenAI Blog. https://openai.com/index/frontierscience

[21] OpenAI Blog. (2025, December 1). OpenAI takes an ownership stake in Thrive Holdings to accelerate enterprise AI adoption. OpenAI Blog. https://openai.com/index/thrive-holdings

[22] OpenAI Blog. (2025, December 1). Accenture and OpenAI accelerate enterprise AI success. OpenAI Blog. https://openai.com/index/accenture-partnership

[23] OpenAI Blog. (2025, December 1). OpenAI and NORAD team up to bring new magic to "NORAD Tracks Santa". OpenAI Blog. https://openai.com/index/norad-holiday-collaboration

[24] OpenAI Blog. (2025, December 1). Funding grants for new research into AI and mental health. OpenAI Blog. https://openai.com/index/ai-mental-health-research-grants

[25] OpenAI Blog. (2025, December 1). Inside Mirakl's agentic commerce vision. OpenAI Blog. https://openai.com/index/mirakl

[26] OpenAI Blog. (2025, December 3). Announcing the initial People-First AI Fund grantees. OpenAI Blog. https://openai.com/index/people-first-ai-fund-grantees

[27] OpenAI Blog. (2025, December 3). How confessions can keep language models honest. OpenAI Blog. https://openai.com/index/how-confessions-can-keep-language-models-honest

[28] OpenAI Blog. (2025, December 3). OpenAI to acquire Neptune. OpenAI Blog. https://openai.com/index/openai-to-acquire-neptune

[29] OpenAI Blog. (2025, December 4). Introducing OpenAI for Australia. OpenAI Blog. https://openai.com/global-affairs/openai-for-australia

[30] OpenAI Blog. (2025, December 8). How Virgin Atlantic uses AI to enhance every step of travel. OpenAI Blog. https://openai.com/index/virgin-atlantic-oliver-byers

[31] OpenAI Blog. (2025, December 8). The state of enterprise AI. OpenAI Blog. https://openai.com/index/the-state-of-enterprise-ai-2025-report

[32] OpenAI Blog. (2025, December 9). Bringing powerful AI to millions across Europe with Deutsche Telekom. OpenAI Blog. https://openai.com/index/deutsche-telekom-collaboration

[33] OpenAI Blog. (2025, December 8). Instacart and OpenAI partner on AI shopping experiences. OpenAI Blog. https://openai.com/index/instacart-partnership

[34] OpenAI Blog. (2025, December 9). OpenAI co-founds Agentic AI Foundation, donates AGENTS.md. OpenAI Blog. https://openai.com/index/agentic-ai-foundation

[35] OpenAI Blog. (2025, December 9). How Scout24 is building the next generation of real-estate search with AI. OpenAI Blog. https://openai.com/index/scout24

[36] OpenAI Blog. (2025, December 10). Strengthening cyber resilience as AI capabilities advance. OpenAI Blog. https://openai.com/index/strengthening-cyber-resilience

[37] OpenAI Blog. (2025, December 11). Ten years. OpenAI Blog. https://openai.com/index/ten-years

[38] OpenAI Blog. (2025, December 11). The Walt Disney Company and OpenAI reach landmark agreement to bring beloved characters to Sora. OpenAI Blog. https://openai.com/index/disney-sora-agreement

[39] OpenAI Blog. (2025, December 11). Introducing GPT-5.2. OpenAI Blog. https://openai.com/index/introducing-gpt-5-2

[40] OpenAI Blog. (2025, December 11). Increasing revenue 300% by bringing AI to SMBs. OpenAI Blog. https://openai.com/index/podium

[41] OpenAI Blog. (2025, December 11). Advancing science and math with GPT-5.2. OpenAI Blog. https://openai.com/index/gpt-5-2-for-science-and-math

[42] OpenAI Blog. (2025, December 12). BNY builds "AI for everyone, everywhere" with OpenAI. OpenAI Blog. https://openai.com/index/bny

[43] OpenAI Blog. (2025, December 16). The new ChatGPT Images is here. OpenAI Blog. https://openai.com/index/new-chatgpt-images-is-here

[44] OpenAI Blog. (2025, December 17). Developers can now submit apps to ChatGPT. OpenAI Blog. https://openai.com/index/developers-can-now-submit-apps-to-chatgpt

[45] OpenAI Blog. (2025, December 18). Addendum to GPT-5.2 System Card: GPT-5.2-Codex. OpenAI Blog. https://openai.com/index/gpt-5-2-codex-system-card

[46] OpenAI Blog. (2025, December 18). Introducing GPT-5.2-Codex. OpenAI Blog. https://openai.com/index/gpt-5-2-codex

[47] OpenAI Blog. (2025, December 18). Introducing GPT-5.2-Codex. OpenAI Blog. https://openai.com/index/introducing-gpt-5-2-codex

[48] OpenAI Blog. (2025, December 18). Updating our Model Spec with teen protections. OpenAI Blog. https://openai.com/index/updating-model-spec-with-teen-protections

[49] OpenAI Blog. (2025, December 12). BBVA and OpenAI collaborate to transform global banking. OpenAI Blog. https://openai.com/index/bbva-collaboration-expansion

[50] OpenAI Blog. (2025, December 22). Continuously hardening ChatGPT Atlas against prompt injection. OpenAI Blog. https://openai.com/index/hardening-atlas-against-prompt-injection

[51] OpenAI Blog. (2025, December 22). One in a million: celebrating the customers shaping AI's future. OpenAI Blog. https://openai.com/index/one-in-a-million-customers

[52] Simon Willison. (2025, December 26). How uv got so fast. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/26/how-uv-got-so-fast/

[53] OpenAI Blog. (2025, December 9). Launching our first OpenAI Certifications courses. OpenAI Blog. https://openai.com/index/openai-certificate-courses

[54] Simon Willison. (2025, December 27). Pluribus training data. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/john-cena/

[55] OpenAI Blog. (2025, December 12). How We Used Codex to Ship Sora for Android in 28 Days. OpenAI Blog. https://openai.com/index/shipping-sora-for-android-with-codex

[56] OpenAI Blog. (2025, December 18). Evaluating chain-of-thought monitorability. OpenAI Blog. https://openai.com/index/evaluating-chain-of-thought-monitorability

[57] OpenAI Blog. (2025, December 18). AI literacy resources for teens and parents. OpenAI Blog. https://openai.com/index/ai-literacy-resources-for-teens-and-parents

[58] OpenAI Blog. (2025, December 9). Building AI fluency at scale with ChatGPT Enterprise. OpenAI Blog. https://openai.com/index/commonwealth-bank-of-australia

[59] OpenAI Blog. (2025, December 9). OpenAI appoints Denise Dresser as Chief Revenue Officer. OpenAI Blog. https://openai.com/index/openai-appoints-denise-dresser

[60] Simon Willison. (2025, December 27). Quoting Boris Cherny. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/boris-cherny/

[61] Nathan Lambert. (2025, December 18). Open models: Hot or Not with Nathan Lambert & Florian Brand. Interconnects. https://www.interconnects.ai/p/open-models-hot-or-not-with-nathan

[62] Simon Willison. (2025, December 13). Quoting Obie Fernandez. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/13/obie-fernandez/

[63] Simon Willison. (2025, December 16). The new ChatGPT Images is here. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/16/new-chatgpt-images/

[64] Simon Willison. (2025, December 18). Inside PostHog: How SSRF, a ClickHouse SQL Escaping 0day, and Default PostgreSQL Credentials Formed an RCE Chain. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/18/ssrf-clickhouse-postgresql/

[65] Simon Willison. (2025, December 17). AoAH Day 15: Porting a complete HTML5 parser and browser test suite. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/17/vibespiling/

[66] Simon Willison. (2025, December 23). Quoting Salvatore Sanfilippo. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/23/salvatore-sanfilippo/

[67] Sebastian Raschka. (2025, December 3). From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates. Sebastian Raschka's Blog. https://sebastianraschka.com/blog/2025/technical-deepseek.html

[68] Sebastian Raschka. (2025, December 8). From Random Forests to RLVR: A Short History of ML/AI Hello Worlds. Sebastian Raschka's Blog. https://sebastianraschka.com/blog/2025/hello-world-ai.html

[69] Vicki Boykis. (2025, December 22). 2025 in review. Vicki Boykis. https://veekaybee.github.io/2025/12/22/2025-in-review/

[70] Simon Willison. (2025, December 13). Quoting OpenAI Codex CLI. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/13/openai-codex-cli/

[71] Simon Willison. (2025, December 16). Quoting Gemini thinking trace. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/16/gemini-thinking-trace/

[72] Simon Willison. (2025, December 24). uv-init-demos. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/24/uv-init-demos/

[73] Simon Willison. (2025, December 14). Copywriters reveal how AI has decimated their industry. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/14/copywriters-reveal-how-ai-has-decimated-their-industry/

[74] Simon Willison. (2025, December 14). JustHTML is a fascinating example of vibe engineering in action. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/14/justhtml/

[75] Simon Willison. (2025, December 15). 2025 Word of the Year: Slop. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/15/2025-word-of-the-year-slop/

[76] Simon Willison. (2025, December 15). I ported JustHTML from Python to JavaScript with Codex CLI and GPT-5.2 in 4.5 hours. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/15/porting-justhtml/

[77] Simon Willison. (2025, December 16). Quoting Kent Beck. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/16/kent-beck/

[78] Simon Willison. (2025, December 16). Poe the Poet. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/16/poe-the-poet/

[79] Simon Willison. (2025, December 16). ty: An extremely fast Python type checker and LSP. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/16/ty/

[80] Simon Willison. (2025, December 16). s3-credentials 0.17. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/16/s3-credentials/

[81] Simon Willison. (2025, December 17). firefox parser/html/java/README.txt. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/17/firefox-parser/

[82] Simon Willison. (2025, December 19). Agent Skills. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/19/agent-skills/

[83] Simon Willison. (2025, December 19). Introducing GPT-5.2-Codex. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/19/introducing-gpt-52-codex/

[84] Simon Willison. (2025, December 19). Sam Rose explains how LLMs work with a visual essay. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/19/sam-rose-llms/

[85] Simon Willison. (2025, December 19). Quoting Andrej Karpathy. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/19/andrej-karpathy/

[86] Simon Willison. (2025, December 17). Gemini 3 Flash. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/17/gemini-3-flash/

[87] Simon Willison. (2025, December 18). Your job is to deliver code you have proven to work. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/18/code-proven-to-work/

[88] Simon Willison. (2025, December 18). swift-justhtml. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/18/swift-justhtml/

[89] Simon Willison. (2025, December 21). Quoting Shriram Krishnamurthi. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/21/shriram-krishnamurthi/

[90] Simon Willison. (2025, December 22). Using Claude in Chrome to navigate out the Cloudflare dashboard. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/22/claude-chrome-cloudflare/

[91] Simon Willison. (2025, December 23). Cooking with Claude. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/23/cooking-with-claude/

[92] Simon Willison. (2025, December 23). MicroQuickJS. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/23/microquickjs/

[93] Simon Willison. (2025, December 25). A new way to extract detailed transcripts from Claude Code. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/25/claude-code-transcripts/

[94] Simon Willison. (2025, December 26). How Rob Pike got spammed with an AI slop "act of kindness". Simon Willison's Weblog. https://simonwillison.net/2025/Dec/26/slop-acts-of-kindness/

[95] TechCrunch. (2025, December 29). Meta just bought Manus, an AI startup everyone has been talking about. https://techcrunch.com/2025/12/29/meta-just-bought-manus-an-ai-startup-everyone-has-been-talking-about/

[96] CNBC. (2025, December 30). Meta acquires intelligent agent firm Manus, capping year of aggressive AI moves. https://www.cnbc.com/2025/12/30/meta-acquires-singapore-ai-agent-firm-manus-china-butterfly-effect-monicai.html

[97] CBC News. (2025, December 30). Meta acquires Chinese-founded AI startup Manus for $2B. https://www.cbc.ca/news/business/meta-manus-acquisition-two-billion-explained-9.7030180

[98] Al Jazeera. (2025, December 30). Tech giant Meta buys Chinese-founded AI firm Manus. https://www.aljazeera.com/economy/2025/12/30/tech-giant-meta-buys-chinese-founded-ai-firm-manus