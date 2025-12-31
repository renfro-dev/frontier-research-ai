# Weekly Systems Thinking Brief: October 16-30, 2025

## Executive Summary

This week's AI landscape is dominated by significant infrastructure investments, with OpenAI announcing partnerships to deploy 16 gigawatts of computing power through collaborations with AMD and Broadcom [33][40]. These massive infrastructure projects coincide with a shift in the open model ecosystem, where Chinese models like Qwen have gained dominance over Western counterparts like Meta's Llama [3][27]. Meanwhile, Google DeepMind achieved breakthrough performances in specialized domains, with Gemini models reaching gold-medal standards in both the International Mathematical Olympiad and the International Collegiate Programming Contest [2][18].

The week also saw numerous announcements of AI applications in specialized domains, from Google's AlphaEarth for planetary mapping [8] to Aeneas for ancient inscription analysis [21]. These specialized tools demonstrate how frontier AI capabilities are being adapted to solve complex problems across diverse fields. Simultaneously, both OpenAI and Google are expanding their global partnerships, with OpenAI announcing collaborations with the UK Ministry of Justice [6], Japan's Digital Agency [30], and potential projects in Argentina [41].

## Key Developments

### Massive Infrastructure Investments Signal AI Arms Race

The scale of infrastructure investment in AI continues to accelerate, with OpenAI announcing two major partnerships for computing power. The company revealed a multi-year partnership with AMD to deploy 6 gigawatts of AMD Instinct GPUs, beginning with 1 gigawatt in 2026 [33]. This was followed by an even larger announcement of a strategic collaboration with Broadcom to deploy 10 gigawatts of OpenAI-designed AI accelerators by 2029 [40]. These investments represent an unprecedented scale of computing infrastructure—6 gigawatts is enough electricity to power approximately 4.5 million homes.

OpenAI is also expanding its physical infrastructure through the "Stargate" initiative, announcing a new one-gigawatt campus in Michigan that aims to strengthen America's AI infrastructure while creating jobs and driving economic growth across the Midwest [60]. Similar projects are being explored internationally, including Argentina's first Stargate project—an AI and clean energy collaboration between OpenAI and Sur Energy that could position Argentina as a Latin American leader in AI and sustainable infrastructure [41].

The infrastructure race extends beyond hardware to include software frameworks for reinforcement learning (RL). Nathan Lambert notes that "scaling reinforcement learning is the next step in improving frontier models" [28], with companies developing specialized approaches to predict learning curves and optimize training. A paper called ScaleRL provides the "first definitive paper on scaling RL," establishing methods to extrapolate RL learning curves across compute scales [28]. These developments suggest that the ability to efficiently scale RL will be crucial for future AI advancements.

### Chinese Open Models Gain Dominance

A significant shift has occurred in the open model landscape, with Chinese models taking the lead [3]. According to Nathan Lambert, "DeepSeek kickstarted the Chinese open model norms" while "Qwen has achieved dominance in the open model landscape" [3]. This represents a major change from previous years when Western models like Meta's Llama were more prominent.

Download statistics confirm this shift, with Qwen 2.5 1.5B becoming "one of the most downloaded models of all time" [27]. The ATOM Project's analysis shows that "GPT-OSS's 20B and 120B models have 5.6M and 3.2M downloads in the last month" [27], but Chinese models continue to dominate the ecosystem. Lambert notes that "Chinese open models improve at an astonishing rate, being close to the best closed models" [27].

This dominance extends to model capabilities as well. GLM-4.6 is compared favorably to commercial models like "Sonnet/Haiku 4.5" though it "falls off harder at longer context than closed models" [27]. Qwen has released VL series updates with both small dense models and larger Mixture-of-Experts (MoE) models, and is exploring different architectures with hybrid attention [27]. Their Qwen3-Next model, "trained on over 15T tokens," could form "the groundwork for the next generation of Qwen models" [27].

### Specialized AI Models Achieve Breakthrough Performances

Google DeepMind announced several breakthrough performances in specialized domains. An advanced version of Gemini with Deep Think "officially achieves gold-medal standard at the International Mathematical Olympiad" [2], which is described as "the world's most prestigious competition for young mathematicians" that has been held annually since 1959 [2]. Similarly, Gemini 2.5 Deep Think achieved "gold-medal level at the International Collegiate Programming Contest World Finals" [18], demonstrating "a profound leap in abstract problem solving" [18].

Google is making some of these capabilities available to users, rolling out Deep Think in the Gemini app for Google AI Ultra subscribers, while "giving select mathematicians access to the full version of the Gemini 2.5 Deep Think model entered into the IMO competition" [13]. This suggests a tiered approach to deploying advanced reasoning capabilities.

Beyond mathematical reasoning, Google announced specialized models for various domains. AlphaEarth Foundations "integrates petabytes of Earth observation data" to create "a unified data representation" that "revolutionizes global mapping and monitoring" [8]. Gemma 3 270M, "a compact, 270-million parameter model," was added to the Gemma 3 toolkit [11], while a new "27 billion parameter foundation model for single-cell analysis" was built on the Gemma family of open models [9]. The Perch model helps "conservationists analyze audio faster to protect endangered species, from Hawaiian honeycreepers to coral reefs" [19].

Google also announced Genie 3, which "can generate dynamic worlds that you can navigate in real time at 24 frames per second, retaining consistency for a few minutes at a resolution of 720p" [20]. Aeneas, described as "the first model for contextualizing ancient inscriptions," is "designed to help historians better interpret, attribute and restore fragmentary texts" [21]. These specialized models demonstrate how AI capabilities are being adapted to solve complex problems across diverse fields.

### OpenAI Expands Global Partnerships and Sovereign AI

OpenAI announced several international partnerships this week. The company is "expanding its existing partnership in the UK through a new agreement with the Ministry of Justice" that will "make ChatGPT available to civil servants" [6]. OpenAI is also "introducing UK data residency for ChatGPT Enterprise, ChatGPT Edu, and the API Platform" to support "trusted and secure AI adoption" [6].

In Japan, OpenAI partnered with the Digital Agency to "advance generative AI in public services, support international AI governance, and promote safe, trustworthy AI adoption worldwide" [30]. The company also released a "Japan Economic Blueprint" outlining how Japan can "harness AI" to "boost innovation," "strengthen competitiveness," and "enable sustainable growth" [44]. A similar "Korea Economic Blueprint" outlines how South Korea can "scale trusted AI through sovereign capabilities and strategic partnerships to drive growth" [45].

These partnerships extend to the private sector as well. In Korea, Wrtn has "scaled AI apps to 6.5M users" with GPT-5, creating "Lifestyle AI" that "blends productivity, creativity, and learning" [31]. The company is now "expanding across East Asia" [31]. OpenAI and Allied for Startups released the "Hacktivate AI report" containing "20 actionable policy ideas to accelerate AI adoption in Europe" [32].

### New Tools for Developers and Enterprise Users

Both OpenAI and Google released new tools for developers and enterprise users this week. OpenAI introduced "a new generation of apps you can chat with, right inside ChatGPT" along with "the new Apps SDK, available in preview" [34]. The company also announced that Codex is "now generally available" with new features including "a Slack integration, Codex SDK, and admin tools" like "usage dashboards and workspace management" [35].

For enterprise users, OpenAI introduced "Company knowledge," which "brings context from your apps into ChatGPT" to provide "answers specific to your business" [57]. This feature includes "clear citations," "security, privacy, and admin controls," and is "available for Business, Enterprise, and Edu users" [57].

Google announced the Gemini 2.5 Computer Use model, which is "available in preview via the API" and "designed to power agents that can interact with user interfaces" [10]. The company also announced Gemini Robotics 1.5, which is "powering an era of physical agents" by "enabling robots to perceive, plan, think, use tools and act" to "better solve complex, multi-step tasks" [15].

OpenAI also introduced Aardvark, an "agentic security researcher" that "autonomously finds, validates, and helps fix software vulnerabilities at scale" [59]. The system is currently "in private beta" with opportunities for "people to sign up to join early testing" [59]. Similarly, Doppel uses "OpenAI's GPT-5 and reinforcement fine-tuning (RFT)" to "stop deepfake and impersonation attacks before they spread," "cutting analyst workloads by 80%" and "reducing threat response from hours to minutes" [54].

## Tensions & Conflicts

### Sustainability of AI Work Culture

The intense pace of AI development has led to concerns about burnout and work-life balance. According to Nathan Lambert, "AI workers are putting in extremely long hours, with some working 100-hour workweeks" [29]. The Wall Street Journal reported that "several top AI researchers have compared their circumstances to war" [29], though Lambert argues this comparison is inappropriate given actual ongoing conflicts.

Lambert suggests that "the time window to be a player at the most cutting edge of LLM technology is actually a closing window" [29] and that "the quality bar for technical output in LLM development is constantly rising" [29]. This creates pressure to work longer hours, but Lambert warns that "mental acuity can drop off faster than physical peak performance when not rested" [29].

### Human vs. AI-Generated Code Quality

Despite advances in AI coding assistants, some experts argue that human-written code remains superior. Vicki Boykis claims that "quality software is written by people who care about software correctness, interfaces, and have worked towards mastery" [61]. She argues that "generative code models produce average quality code" that is "quite literally, mid, the compressed and weighted average of every excellent Stack Overflow answer" [61].

Boykis maintains that "humans are still better than AI at software reasoning, aesthetic judgment, and architecture" [61], suggesting that "intent matters in software engineering" [61]. This perspective conflicts with the industry's increasing embrace of AI coding assistants and automated code generation.

### Evaluation Methodologies for AI Models

Different organizations report significantly different download statistics for the same models. The ATOM Project's numbers "differ greatly from the numbers from CAISI and those differ even more from the ones by HuggingFace itself" [27]. This discrepancy arises from different methodologies for counting and filtering downloads.

Similarly, there are conflicts in how models are evaluated. The Center for AI Standards and Innovation (CAISI) released a report evaluating DeepSeek 3.1 against leading closed models, but "the evaluation scores they highlighted show some discrepancy with accepted results in the community" [27]. While some benchmarks like MMLU-Pro, GPQA, and HLE are "close to the self-reported scores from DeepSeek and within usual error bars," the SWE-bench Verified scores are "off by a wide margin due to a weak harness for the benchmark" [27]. This suggests that "the harness has as great an impact as the model itself for agentic benchmarks" [27].

## Implications

For builders and practitioners in the AI ecosystem, these developments highlight several key considerations. The massive infrastructure investments by major players suggest that compute will remain a critical differentiator, potentially widening the gap between well-funded organizations and smaller players. The rise of Chinese open models demonstrates that innovation can come from unexpected sources, and practitioners should monitor developments globally rather than focusing solely on Western companies.

The specialized AI models achieving breakthrough performances in specific domains indicate that tailoring models for particular use cases may yield better results than general-purpose approaches. Finally, the tensions around work culture, code quality, and evaluation methodologies underscore the importance of establishing sustainable practices and reliable benchmarks as the field continues to evolve rapidly.

## Source Cards

[1] Elhage, N. (2025, October 21). Solving Regex Crosswords with Z3. Nelson Elhage (Made of Bugs). https://blog.nelhage.com/post/regex-crosswords-z3/

[2] Google DeepMind Blog. (2025, October 24). Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the International Mathematical Olympiad. https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/

[3] Lambert, N. (2025, October 16). The State of Open Models. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/state-of-open-models-2025

[4] OpenAI Blog. (2025, October 6). Introducing AgentKit, new Evals, and RFT for agents. https://openai.com/index/introducing-agentkit

[5] OpenAI Blog. (2025, October 14). Expert Council on Well-Being and AI. https://openai.com/index/expert-council-on-well-being-and-ai

[6] OpenAI Blog. (2025, October 22). The next chapter for UK sovereign AI. https://openai.com/index/the-next-chapter-for-uk-sovereign-ai

[7] OpenAI Blog. (2025, October 29). Technical Report: Performance and baseline evaluations of gpt-oss-safeguard-120b and gpt-oss-safeguard-20b. https://openai.com/index/gpt-oss-safeguard-technical-report

[8] Google DeepMind Blog. (2025, October 24). AlphaEarth Foundations helps map our planet in unprecedented detail. https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/

[9] Google DeepMind Blog. (2025, October 23). How a Gemma model helped discover a new potential cancer therapy pathway. https://deepmind.google/blog/how-a-gemma-model-helped-discover-a-new-potential-cancer-therapy-pathway/

[10] Google DeepMind Blog. (2025, October 23). Introducing the Gemini 2.5 Computer Use model. https://deepmind.google/blog/introducing-the-gemini-25-computer-use-model/

[11] Google DeepMind Blog. (2025, October 23). Introducing Gemma 3 270M: The compact model for hyper-efficient AI. https://deepmind.google/blog/introducing-gemma-3-270m-the-compact-model-for-hyper-efficient-ai/

[12] Google DeepMind Blog. (2025, October 23). Rethinking how we measure AI intelligence. https://deepmind.google/blog/rethinking-how-we-measure-ai-intelligence/

[13] Google DeepMind Blog. (2025, October 23). Try Deep Think in the Gemini app. https://deepmind.google/blog/try-deep-think-in-the-gemini-app/

[14] Google DeepMind Blog. (2025, October 23). Bringing AI to the next generation of fusion energy. https://deepmind.google/blog/bringing-ai-to-the-next-generation-of-fusion-energy/

[15] Google DeepMind Blog. (2025, October 23). Gemini Robotics 1.5 brings AI agents into the physical world. https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/

[16] Google DeepMind Blog. (2025, October 23). Strengthening our Frontier Safety Framework. https://deepmind.google/blog/strengthening-our-frontier-safety-framework/

[17] Google DeepMind Blog. (2025, October 24). Discovering new solutions to century-old problems in fluid dynamics. https://deepmind.google/blog/discovering-new-solutions-to-century-old-problems-in-fluid-dynamics/

[18] Google DeepMind Blog. (2025, October 24). Gemini achieves gold-medal level at the International Collegiate Programming Contest World Finals. https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/

[19] Google DeepMind Blog. (2025, October 24). How AI is helping advance the science of bioacoustics to save endangered species. https://deepmind.google/blog/how-ai-is-helping-advance-the-science-of-bioacoustics-to-save-endangered-species/

[20] Google DeepMind Blog. (2025, October 24). Genie 3: A new frontier for world models. https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/

[21] Google DeepMind Blog. (2025, October 24). Aeneas transforms how historians connect the past. https://deepmind.google/blog/aeneas-transforms-how-historians-connect-the-past/

[22] Google DeepMind Blog. (2025, October 25). Behind "ANCESTRA": combining Veo with live-action filmmaking. https://deepmind.google/blog/behind-ancestra-combining-veo-with-live-action-filmmaking/

[23] Google DeepMind Blog. (2025, October 25). Gemini 2.5 Flash-Lite is now ready for scaled production use. https://deepmind.google/blog/gemini-25-flash-lite-is-now-ready-for-scaled-production-use/

[24] Google DeepMind Blog. (2025, October 25). MedGemma: Our most capable open models for health AI development. https://deepmind.google/blog/medgemma-our-most-capable-open-models-for-health-ai-development/

[25] Google DeepMind Blog. (2025, October 29). Accelerating discovery with the AI for Math Initiative. https://deepmind.google/blog/accelerating-discovery-with-the-ai-for-math-initiative/

[26] Lambert, N. (2025, October 7). Thoughts on The Curve. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/thoughts-on-the-curve

[27] Lambert, N. (2025, October 18). Latest open artifacts (#15): It's Qwen's world and we get to live in it, on CAISI's report, & GPT-OSS update. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/latest-open-models-15-its-qwens-world

[28] Lambert, N. (2025, October 20). How to scale RL. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/the-new-rl-scaling-laws

[29] Lambert, N. (2025, October 25). Burning out. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/burning-out

[30] OpenAI Blog. (2025, October 2). OpenAI announces strategic collaboration with Japan's Digital Agency. https://openai.com/global-affairs/strategic-collaboration-with-japan-digital-agency

[31] OpenAI Blog. (2025, October 2). With GPT-5, Wrtn builds lifestyle AI for millions in Korea. https://openai.com/index/wrtn

[32] OpenAI Blog. (2025, October 6). Accelerating AI adoption in Europe. https://openai.com/global-affairs/accelerating-ai-uptake-in-europe

[33] OpenAI Blog. (2025, October 6). AMD and OpenAI announce strategic partnership to deploy 6 gigawatts of AMD GPUs. https://openai.com/index/openai-amd-strategic-partnership

[34] OpenAI Blog. (2025, October 6). Introducing apps in ChatGPT and the new Apps SDK. https://openai.com/index/introducing-apps-in-chatgpt

[35] OpenAI Blog. (2025, October 6). Codex is now generally available. https://openai.com/index/codex-now-generally-available

[36] OpenAI Blog. (2025, October 7). Disrupting malicious uses of AI: October 2025. https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-october-2025

[37] OpenAI Blog. (2025, October 8). Growing impact and scale with ChatGPT. https://openai.com/index/hibob

[38] OpenAI Blog. (2025, October 9). Defining and evaluating political bias in LLMs. https://openai.com/index/defining-and-evaluating-political-bias-in-llms

[39] OpenAI Blog. (2025, October 10). HYGH powers next-gen digital ads with ChatGPT Business. https://openai.com/index/hygh

[40] OpenAI Blog. (2025, October 13). OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators. https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration

[41] OpenAI Blog. (2025, October 14). Argentina's AI opportunity. https://openai.com/global-affairs/argentinas-ai-opportunity

[42] OpenAI Blog. (2025, October 21). Introducing ChatGPT Atlas, the browser with ChatGPT built in. https://openai.com/index/introducing-chatgpt-atlas

[43] OpenAI Blog. (2025, October 21). Continue your ChatGPT experience beyond WhatsApp. https://openai.com/index/chatgpt-whatsapp-transition

[44] OpenAI Blog. (2025, October 22). AI in Japan—OpenAI's Japan Economic Blueprint. https://openai.com/index/japan-economic-blueprint

[45] OpenAI Blog. (2025, October 23). AI in South Korea—OpenAI's Economic Blueprint. https://openai.com/index/south-korea-economic-blueprint

[46] OpenAI Blog. (2025, October 23). Consensus accelerates research with GPT-5 and Responses API. https://openai.com/index/consensus

[47] OpenAI Blog. (2025, October 23). OpenAI acquires Software Applications Incorporated, maker of Sky. https://openai.com/index/openai-acquires-software-applications-incorporated

[48] OpenAI Blog. (2025, October 27). A law and tax firm redefines efficiency with ChatGPT Business. https://openai.com/index/steuerrecht

[49] OpenAI Blog. (2025, October 27). Strengthening ChatGPT's responses in sensitive conversations. https://openai.com/index/strengthening-chatgpt-responses-in-sensitive-conversations

[50] OpenAI Blog. (2025, October 27). Addendum to GPT-5 System Card: Sensitive conversations. https://openai.com/index/gpt-5-system-card-sensitive-conversations

[51] OpenAI Blog. (2025, October 27). Seizing the AI opportunity. https://openai.com/global-affairs/seizing-the-ai-opportunity

[52] OpenAI Blog. (2025, October 28). Built to benefit everyone. https://openai.com/index/built-to-benefit-everyone

[53] OpenAI Blog. (2025, October 28). The next chapter of the Microsoft–OpenAI partnership. https://openai.com/index/next-chapter-of-microsoft-openai-partnership

[54] OpenAI Blog. (2025, October 28). Doppel's AI defense system stops attacks before they spread. https://openai.com/index/doppel

[55] OpenAI Blog. (2025, October 28). Knowledge preservation powered by ChatGPT. https://openai.com/index/dai-nippon-printing

[56] OpenAI Blog. (2025, October 29). Introducing gpt-oss-safeguard. https://openai.com/index/introducing-gpt-oss-safeguard

[57] OpenAI Blog. (2025, October 23). Work smarter with your company knowledge in ChatGPT. https://openai.com/index/introducing-company-knowledge

[58] OpenAI Blog. (2025, October 30). How we built OWL, the new architecture behind our ChatGPT-based browser, Atlas. https://openai.com/index/building-chatgpt-atlas

[59] OpenAI Blog. (2025, October 30). Introducing Aardvark: OpenAI's agentic security researcher. https://openai.com/index/introducing-aardvark

[60] OpenAI Blog. (2025, October 30). Expanding Stargate to Michigan. https://openai.com/index/expanding-stargate-to-michigan

[61] Boykis, V. (2025, October 20). I want to see the claw. Vicki Boykis. https://veekaybee.github.io/2025/10/20/i-want-to-see-the-claw/

[62] Raschka, S. (2025, October 29). DGX Spark and Mac Mini for Local PyTorch Development. Sebastian Raschka's Blog. https://sebastianraschka.com/blog/2025/dgx-impressions.html

[63] OpenAI Blog. (2025, October 15). Plex Coffee delivers fast service and personal connections with ChatGPT Business. https://openai.com/index/plex-coffee
