# Weekly Systems Thinking Brief: The Evolving AI Landscape

## Executive Summary

The AI industry is undergoing a significant transformation as companies race to build infrastructure, deploy models, and establish strategic partnerships that will shape the future of artificial intelligence. This week's developments highlight how the competition for AI dominance is intensifying across multiple fronts: massive compute infrastructure investments, open model ecosystems, specialized AI applications, and international partnerships.

The scale of infrastructure investment is staggering, with OpenAI announcing partnerships to deploy 6 gigawatts of AMD GPUs [33] and 10 gigawatts of custom-designed AI accelerators with Broadcom [40]—enough power to run multiple major cities. Meanwhile, Chinese companies have taken the lead in open models, with Qwen achieving dominance as Llama's influence fades [3]. These developments are occurring against a backdrop of increasing work intensity, with some AI researchers reportedly working 100-hour weeks in what some have compared to wartime conditions [29].

For business leaders and decision-makers, these developments signal both opportunity and challenge. The technical standard for relevance in AI is rising rapidly [29], creating pressure to invest in increasingly sophisticated AI capabilities while also raising questions about the sustainability of current development practices. At the same time, new specialized AI applications—from mathematical problem-solving to historical analysis—demonstrate how AI is expanding beyond general-purpose assistants into highly specialized domains.

## Key Developments

### Massive Infrastructure Investments Signal AI Arms Race

The scale of infrastructure investment in AI has reached unprecedented levels, reflecting the compute-intensive nature of advanced AI development. OpenAI announced a multi-year partnership with AMD to deploy 6 gigawatts of AMD Instinct GPUs, beginning with 1 gigawatt in 2026 [33]. For context, 1 gigawatt is enough electricity to power approximately 750,000 homes. OpenAI followed this with another announcement of a 10-gigawatt deployment of custom-designed AI accelerators in partnership with Broadcom, extending through 2029 [40].

These massive infrastructure investments are part of what some are calling a "new tech arms race" [29]. The pressure to remain competitive is driving extreme work conditions, with the Wall Street Journal reporting that some AI workers are putting in 100-hour workweeks [29]. Several top researchers have compared their circumstances to war, though this comparison has been criticized as out of touch given actual ongoing conflicts [29].

The infrastructure buildout extends beyond private companies to national initiatives. OpenAI announced the expansion of its Stargate project to Michigan with a new one-gigawatt campus that aims to strengthen America's AI infrastructure while creating jobs and driving economic growth across the Midwest [60]. Peter Wildeford predicts that "we will see fully operational 1GW data centers before mid-2026" as part of "45-60GW of total compute across Meta, Microsoft, Amazon/AWS/Anthropic, OpenAI/Oracle, Google/DeepMind, and xAI" [26].

### China Takes the Lead in Open Models as Ecosystem Evolves

The open model landscape has undergone a significant shift, with Chinese companies now taking the lead [3]. Qwen has achieved dominance in the open model ecosystem while Meta's Llama has faded in influence [3]. This represents more than just a technical milestone—it signals China's growing dominance in open AI development, which has implications for where innovation happens and who controls foundational AI infrastructure [27].

Qwen 2.5 1.5B has become one of the most downloaded models of all time, with extreme outliers on the order of 10M+ downloads that can heavily skew overall statistics [27]. The company continues to innovate, releasing VL series updates with small dense and larger Mixture-of-Experts (MoE) models—an architecture where only a subset of the model's parameters are activated for any given input, improving efficiency [27]. Qwen is also exploring different architectures with hybrid attention and has trained Qwen3-Next on over 15T tokens, potentially laying groundwork for their next generation of models [27].

OpenAI has entered the open model space with GPT-OSS, which initially faced implementation difficulties due to architecture choices and complex tool use [27]. Despite these challenges, OpenAI's 20B and 120B GPT-OSS models have seen strong adoption with 5.6M and 3.2M downloads in the last month, respectively [27]. OpenAI has also introduced gpt-oss-safeguard, which consists of open-weight reasoning models for safety classification that allow developers to apply and iterate on custom policies [56].

### Specialized AI Applications Demonstrate Expanding Capabilities

AI systems are increasingly demonstrating specialized capabilities across diverse domains. Google DeepMind announced that an advanced version of Gemini with Deep Think has officially achieved gold-medal standard at the International Mathematical Olympiad (IMO) [2], the world's most prestigious competition for young mathematicians that has been held annually since 1959 [2]. Similarly, Gemini 2.5 Deep Think achieved breakthrough performance at the International Collegiate Programming Contest World Finals, demonstrating "a profound leap in abstract problem solving" [18].

In the humanities, Google DeepMind introduced Aeneas, described as the first model for contextualizing ancient inscriptions, designed to help historians better interpret, attribute, and restore fragmentary texts [21]. For environmental applications, Google's Perch model helps conservationists analyze audio faster to protect endangered species, from Hawaiian honeycreepers to coral reefs [19].

Medical applications are advancing with the announcement of new multimodal models in the MedGemma collection, described as "our most capable open models for health AI development" [24]. Google DeepMind is also launching a new 27 billion parameter foundation model for single-cell analysis built on the Gemma family of open models [9]. These specialized models demonstrate how AI is being tailored to specific domains requiring deep expertise.

Creative applications are expanding as well, with Google DeepMind's Genie 3 capable of generating dynamic worlds that users can navigate in real time at 24 frames per second, retaining consistency for a few minutes at a resolution of 720p [20]. Google also partnered with filmmaker Darren Aronofsky and a team of more than 200 people to create "ANCESTRA," combining Veo (an AI video generation technology) with live-action filmmaking [22].

### Strategic International Partnerships Reshape Global AI Landscape

Major AI companies are forming strategic partnerships with governments worldwide, potentially reshaping the global AI landscape. OpenAI announced a partnership with Japan's Digital Agency to advance generative AI in public services, support international AI governance, and promote safe, trustworthy AI adoption worldwide [30]. This was followed by the release of OpenAI's Japan Economic Blueprint, which outlines how Japan can harness AI to boost innovation, strengthen competitiveness, and enable sustainable and inclusive growth [44].

Similar initiatives are underway in South Korea, where OpenAI released a Korea Economic Blueprint outlining how South Korea can scale trusted AI through sovereign capabilities and strategic partnerships to drive growth [45]. In Korea, Wrtn has scaled AI applications to 6.5 million users with GPT-5 technology, creating what they call "Lifestyle AI" that blends productivity, creativity, and learning [31].

In the UK, OpenAI is expanding its existing partnership through a new agreement with the Ministry of Justice that will make ChatGPT available to civil servants [6]. OpenAI is also introducing UK data residency for ChatGPT Enterprise, ChatGPT Edu, and the API Platform to support trusted and secure AI adoption [6].

OpenAI and Sur Energy are exploring Argentina's first Stargate project—an AI and clean energy collaboration that could make Argentina a Latin American leader in artificial intelligence, sustainable infrastructure, and digital innovation [41]. In Europe, OpenAI and Allied for Startups released the Hacktivate AI report containing 20 actionable policy ideas to accelerate AI adoption, boost competitiveness, and empower innovators [32].

### New Tools and Frameworks for AI Development and Evaluation

Companies are releasing new tools and frameworks to help developers build, evaluate, and deploy AI systems more effectively. OpenAI released new tools to help developers go from prototype to production faster, including AgentKit, expanded evals capabilities, and reinforcement fine-tuning for agents [4]. Google DeepMind introduced Game Arena, a new, open-source platform for rigorous evaluation of AI models that allows for head-to-head comparison of frontier systems using environments with clear winning conditions [12].

For robotics applications, Google DeepMind announced Gemini Robotics 1.5, which is "powering an era of physical agents" by enabling robots to perceive, plan, think, use tools, and act to better solve complex, multi-step tasks [15]. OpenAI introduced Aardvark, an agentic security researcher that autonomously finds, validates, and helps fix software vulnerabilities at scale [59].

Scaling reinforcement learning (RL) has emerged as a key focus for improving frontier models [28]. The ScaleRL paper provides a method to extrapolate RL learning curves over compute scales and sets a baseline for the order of compute needed for top-end performance [28]. The approach involves taking base models, running some RL, and predicting endpoints through shape forecasting [28]. The paper endorses several recent algorithmic advancements as essential, including truncated importance sampling, Group Sequence Policy Optimization, and Clipped IS-weight Policy Optimization [28].

## Tensions & Conflicts

Several significant tensions and conflicts emerge from this week's developments:

**Work intensity vs. sustainability in AI development**: The extreme work conditions reported in AI development, with some researchers working 100-hour weeks [29], raise questions about sustainability. The author of one article argues that "mental acuity can drop off faster than physical peak performance when not rested" [29], suggesting these practices may be counterproductive. This conflicts with the industry's apparent embrace of such intense work schedules.

**Human vs. AI-generated code quality**: There's tension regarding the quality of AI-generated code compared to human-written code. One author argues that "generative code models produce average quality code" that is "quite literally, mid, the compressed and weighted average of every excellent Stack Overflow answer" [61]. They contend that "humans are still better than AI at software reasoning, aesthetic judgment, and architecture" [61], which conflicts with the industry's increasing embrace of AI coding assistants.

**Open vs. closed model approaches**: Different organizations report significantly different download numbers for the same models due to varying methodologies [27], creating confusion about the actual adoption of open models. There's also debate about whether hybrid reasoning (toggling thinking on/off) reduces peak performance in both modes, despite companies increasingly adopting this approach [27].

**Starting new AI labs vs. established players**: There's conflict over whether starting a new AI lab today provides advantages. Some argue that starting from scratch with a cleaner codebase is beneficial, but others dismiss this as "cope" [29]. The author of one article suggests that "SSI, Thinky, and Reflection1 are likely the last efforts that are capitalized enough to maybe catch up in the near term, but the odds are not on their side" [29], indicating a closing window for new entrants.

## Implications

The developments this week highlight how AI is becoming increasingly compute-intensive, specialized, and globally distributed. The massive infrastructure investments by major AI companies signal that compute will remain a critical competitive advantage. At the same time, the rise of Chinese open models demonstrates that innovation can come from unexpected sources and shift the balance of power in the AI ecosystem.

For organizations looking to leverage AI, these developments suggest the importance of both accessing cutting-edge models and finding specialized applications that deliver concrete value. The numerous examples of AI being applied to specific domains—from mathematics to conservation to healthcare—show how AI is moving beyond general-purpose assistants to tackle specialized problems that previously required deep human expertise.

The tensions around work intensity and sustainability raise important questions about the current pace of AI development. As one author notes, "AI progress is a long-haul now" [29], suggesting that organizations may need to find more sustainable approaches to innovation rather than treating AI development as a sprint.

## Source Cards

[1] Elhage, N. (2025, October 21). Solving Regex Crosswords with Z3. Nelson Elhage (Made of Bugs). https://blog.nelhage.com/post/regex-crosswords-z3/

[2] Google DeepMind Blog. (2025, October 24). Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the International Mathematical Olympiad. Google DeepMind Blog. https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/

[3] Lambert, N. (2025, October 16). The State of Open Models. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/state-of-open-models-2025

[4] OpenAI Blog. (2025, October 6). Introducing AgentKit, new Evals, and RFT for agents. OpenAI Blog. https://openai.com/index/introducing-agentkit

[5] OpenAI Blog. (2025, October 14). Expert Council on Well-Being and AI. OpenAI Blog. https://openai.com/index/expert-council-on-well-being-and-ai

[6] OpenAI Blog. (2025, October 22). The next chapter for UK sovereign AI. OpenAI Blog. https://openai.com/index/the-next-chapter-for-uk-sovereign-ai

[7] OpenAI Blog. (2025, October 29). Technical Report: Performance and baseline evaluations of gpt-oss-safeguard-120b and gpt-oss-safeguard-20b. OpenAI Blog. https://openai.com/index/gpt-oss-safeguard-technical-report

[8] Google DeepMind Blog. (2025, October 24). AlphaEarth Foundations helps map our planet in unprecedented detail. Google DeepMind Blog. https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/

[9] Google DeepMind Blog. (2025, October 23). How a Gemma model helped discover a new potential cancer therapy pathway. Google DeepMind Blog. https://deepmind.google/blog/how-a-gemma-model-helped-discover-a-new-potential-cancer-therapy-pathway/

[10] Google DeepMind Blog. (2025, October 23). Introducing the Gemini 2.5 Computer Use model. Google DeepMind Blog. https://deepmind.google/blog/introducing-the-gemini-25-computer-use-model/

[11] Google DeepMind Blog. (2025, October 23). Introducing Gemma 3 270M: The compact model for hyper-efficient AI. Google DeepMind Blog. https://deepmind.google/blog/introducing-gemma-3-270m-the-compact-model-for-hyper-efficient-ai/

[12] Google DeepMind Blog. (2025, October 23). Rethinking how we measure AI intelligence. Google DeepMind Blog. https://deepmind.google/blog/rethinking-how-we-measure-ai-intelligence/

[13] Google DeepMind Blog. (2025, October 23). Try Deep Think in the Gemini app. Google DeepMind Blog. https://deepmind.google/blog/try-deep-think-in-the-gemini-app/

[14] Google DeepMind Blog. (2025, October 23). Bringing AI to the next generation of fusion energy. Google DeepMind Blog. https://deepmind.google/blog/bringing-ai-to-the-next-generation-of-fusion-energy/

[15] Google DeepMind Blog. (2025, October 23). Gemini Robotics 1.5 brings AI agents into the physical world. Google DeepMind Blog. https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/

[16] Google DeepMind Blog. (2025, October 23). Strengthening our Frontier Safety Framework. Google DeepMind Blog. https://deepmind.google/blog/strengthening-our-frontier-safety-framework/

[17] Google DeepMind Blog. (2025, October 24). Discovering new solutions to century-old problems in fluid dynamics. Google DeepMind Blog. https://deepmind.google/blog/discovering-new-solutions-to-century-old-problems-in-fluid-dynamics/

[18] Google DeepMind Blog. (2025, October 24). Gemini achieves gold-medal level at the International Collegiate Programming Contest World Finals. Google DeepMind Blog. https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/

[19] Google DeepMind Blog. (2025, October 24). How AI is helping advance the science of bioacoustics to save endangered species. Google DeepMind Blog. https://deepmind.google/blog/how-ai-is-helping-advance-the-science-of-bioacoustics-to-save-endangered-species/

[20] Google DeepMind Blog. (2025, October 24). Genie 3: A new frontier for world models. Google DeepMind Blog. https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/

[21] Google DeepMind Blog. (2025, October 24). Aeneas transforms how historians connect the past. Google DeepMind Blog. https://deepmind.google/blog/aeneas-transforms-how-historians-connect-the-past/

[22] Google DeepMind Blog. (2025, October 25). Behind "ANCESTRA": combining Veo with live-action filmmaking. Google DeepMind Blog. https://deepmind.google/blog/behind-ancestra-combining-veo-with-live-action-filmmaking/

[23] Google DeepMind Blog. (2025, October 25). Gemini 2.5 Flash-Lite is now ready for scaled production use. Google DeepMind Blog. https://deepmind.google/blog/gemini-25-flash-lite-is-now-ready-for-scaled-production-use/

[24] Google DeepMind Blog. (2025, October 25). MedGemma: Our most capable open models for health AI development. Google DeepMind Blog. https://deepmind.google/blog/medgemma-our-most-capable-open-models-for-health-ai-development/

[25] Google DeepMind Blog. (2025, October 29). Accelerating discovery with the AI for Math Initiative. Google DeepMind Blog. https://deepmind.google/blog/accelerating-discovery-with-the-ai-for-math-initiative/

[26] Lambert, N. (2025, October 7). Thoughts on The Curve. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/thoughts-on-the-curve

[27] Lambert, N. (2025, October 18). Latest open artifacts (#15): It's Qwen's world and we get to live in it, on CAISI's report, & GPT-OSS update. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/latest-open-models-15-its-qwens-world

[28] Lambert, N. (2025, October 20). How to scale RL. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/the-new-rl-scaling-laws

[29] Lambert, N. (2025, October 25). Burning out. Interconnects (Nathan Lambert). https://www.interconnects.ai/p/burning-out

[30] OpenAI Blog. (2025, October 2). OpenAI announces strategic collaboration with Japan's Digital Agency. OpenAI Blog. https://openai.com/global-affairs/strategic-collaboration-with-japan-digital-agency

[31] OpenAI Blog. (2025, October 2). With GPT-5, Wrtn builds lifestyle AI for millions in Korea. OpenAI Blog. https://openai.com/index/wrtn

[32] OpenAI Blog. (2025, October 6). Accelerating AI adoption in Europe. OpenAI Blog. https://openai.com/global-affairs/accelerating-ai-uptake-in-europe

[33] OpenAI Blog. (2025, October 6). AMD and OpenAI announce strategic partnership to deploy 6 gigawatts of AMD GPUs. OpenAI Blog. https://openai.com/index/openai-amd-strategic-partnership

[34] OpenAI Blog. (2025, October 6). Introducing apps in ChatGPT and the new Apps SDK. OpenAI Blog. https://openai.com/index/introducing-apps-in-chatgpt

[35] OpenAI Blog. (2025, October 6). Codex is now generally available. OpenAI Blog. https://openai.com/index/codex-now-generally-available

[36] OpenAI Blog. (2025, October 7). Disrupting malicious uses of AI: October 2025. OpenAI Blog. https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-october-2025

[37] OpenAI Blog. (2025, October 8). Growing impact and scale with ChatGPT. OpenAI Blog. https://openai.com/index/hibob

[38] OpenAI Blog. (2025, October 9). Defining and evaluating political bias in LLMs. OpenAI Blog. https://openai.com/index/defining-and-evaluating-political-bias-in-llms

[39] OpenAI Blog. (2025, October 10). HYGH powers next-gen digital ads with ChatGPT Business. OpenAI Blog. https://openai.com/index/hygh

[40] OpenAI Blog. (2025, October 13). OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators. OpenAI Blog. https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration

[41] OpenAI Blog. (2025, October 14). Argentina's AI opportunity. OpenAI Blog. https://openai.com/global-affairs/argentinas-ai-opportunity

[42] OpenAI Blog. (2025, October 21). Introducing ChatGPT Atlas, the browser with ChatGPT built in. OpenAI Blog. https://openai.com/index/introducing-chatgpt-atlas

[43] OpenAI Blog. (2025, October 21). Continue your ChatGPT experience beyond WhatsApp. OpenAI Blog. https://openai.com/index/chatgpt-whatsapp-transition

[44] OpenAI Blog. (2025, October 22). AI in Japan—OpenAI's Japan Economic Blueprint. OpenAI Blog. https://openai.com/index/japan-economic-blueprint

[45] OpenAI Blog. (2025, October 23). AI in South Korea—OpenAI's Economic Blueprint. OpenAI Blog. https://openai.com/index/south-korea-economic-blueprint

[46] OpenAI Blog. (2025, October 23). Consensus accelerates research with GPT-5 and Responses API. OpenAI Blog. https://openai.com/index/consensus

[47] OpenAI Blog. (2025, October 23). OpenAI acquires Software Applications Incorporated, maker of Sky. OpenAI Blog. https://openai.com/index/openai-acquires-software-applications-incorporated

[48] OpenAI Blog. (2025, October 27). A law and tax firm redefines efficiency with ChatGPT Business. OpenAI Blog. https://openai.com/index/steuerrecht

[49] OpenAI Blog. (2025, October 27). Strengthening ChatGPT's responses in sensitive conversations. OpenAI Blog. https://openai.com/index/strengthening-chatgpt-responses-in-sensitive-conversations

[50] OpenAI Blog. (2025, October 27). Addendum to GPT-5 System Card: Sensitive conversations. OpenAI Blog. https://openai.com/index/gpt-5-system-card-sensitive-conversations

[51] OpenAI Blog. (2025, October 27). Seizing the AI opportunity. OpenAI Blog. https://openai.com/global-affairs/seizing-the-ai-opportunity

[52] OpenAI Blog. (2025, October 28). Built to benefit everyone. OpenAI Blog. https://openai.com/index/built-to-benefit-everyone

[53] OpenAI Blog. (2025, October 28). The next chapter of the Microsoft–OpenAI partnership. OpenAI Blog. https://openai.com/index/next-chapter-of-microsoft-openai-partnership

[54] OpenAI Blog. (2025, October 28). Doppel's AI defense system stops attacks before they spread. OpenAI Blog. https://openai.com/index/doppel

[55] OpenAI Blog. (2025, October 28). Knowledge preservation powered by ChatGPT. OpenAI Blog. https://openai.com/index/dai-nippon-printing

[56] OpenAI Blog. (2025, October 29). Introducing gpt-oss-safeguard. OpenAI Blog. https://openai.com/index/introducing-gpt-oss-safeguard

[57] OpenAI Blog. (2025, October 23). Work smarter with your company knowledge in ChatGPT. OpenAI Blog. https://openai.com/index/introducing-company-knowledge

[58] OpenAI Blog. (2025, October 30). How we built OWL, the new architecture behind our ChatGPT-based browser, Atlas. OpenAI Blog. https://openai.com/index/building-chatgpt-atlas

[59] OpenAI Blog. (2025, October 30). Introducing Aardvark: OpenAI's agentic security researcher. OpenAI Blog. https://openai.com/index/introducing-aardvark

[60] OpenAI Blog. (2025, October 30). Expanding Stargate to Michigan. OpenAI Blog. https://openai.com/index/expanding-stargate-to-michigan

[61] Boykis, V. (2025, October 20). I want to see the claw. Vicki Boykis. https://veekaybee.github.io/2025/10/20/i-want-to-see-the-claw/

[62] Raschka, S. (2025, October 29). DGX Spark and Mac Mini for Local PyTorch Development. Sebastian Raschka's Blog. https://sebastianraschka.com/blog/2025/dgx-impressions.html

[63] OpenAI Blog. (2025, October 15). Plex Coffee delivers fast service and personal connections with ChatGPT Business. OpenAI Blog. https://openai.com/index/plex-coffee
