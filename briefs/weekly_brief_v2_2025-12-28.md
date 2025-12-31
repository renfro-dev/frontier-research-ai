# Systems Thinking Weekly Brief: December 2025

## Executive Summary

December 2025 has been marked by significant developments in both open and closed AI models. OpenAI released GPT-5.2 and introduced new evaluation frameworks for biological research [1][2], while Google DeepMind expanded its safety partnerships and released new interpretability tools [6][7]. The open model ecosystem has experienced dramatic performance improvements throughout 2025, with models from DeepSeek, Qwen, and others now rivaling closed models on key benchmarks [9]. 

This month also saw innovations in web technology, with the release of textarea.my, a minimalist browser-based text editor that stores content in the URL hash [4]. Meanwhile, AI applications in biology advanced with AlphaFold being used to strengthen photosynthesis enzymes for heat-tolerant crops [5] and OpenAI developing frameworks to measure AI's capability to accelerate biological research [2].

The tension between open and closed models continues, with closed models still dominating real-world usage despite open models' benchmark parity [9]. This reflects broader questions about how we evaluate AI systems and the gap between benchmark performance and practical utility.

## Key Developments

### Evolution of AI Model Capabilities

OpenAI released GPT-5.2, the latest in the GPT-5 model family, maintaining the comprehensive safety mitigation approach used in previous GPT-5 versions [1]. The model was trained on diverse datasets including publicly available internet information, data from third-party partnerships, and information provided by users or human trainers and researchers [1].

Google DeepMind has been active in the interpretability space, releasing Gemma Scope 2, which provides open interpretability tools for all models in the Gemma 3 family [7]. This release aims to help the AI safety community better understand complex language model behavior [7].

The open model ecosystem has seen dramatic performance improvements in 2025, with models now rivaling closed alternatives on most key benchmarks [9]. DeepSeek and Qwen have become household names with their R1 and Qwen 3 releases respectively [9]. DeepSeek R1, released on January 20th, 2025 under the MIT license, inspired many Chinese labs to release their models openly and under open licenses [9]. Qwen has overtaken Llama in terms of total downloads and as the most-used base model for fine-tuning [9].

### AI Applications in Biology and Research

OpenAI introduced a real-world evaluation framework to measure how AI can accelerate biological research in wet labs [2]. Using GPT-5 to optimize a molecular cloning protocol, the work explores both the promise and risks of AI-assisted experimentation [2].

Google DeepMind reported that scientists are using AlphaFold to strengthen a photosynthesis enzyme with the goal of creating heat-tolerant crops [5]. This application demonstrates how AI tools can be applied to address challenges related to climate change and food security [5].

These developments highlight the growing role of AI in scientific research, particularly in biology, where models can help optimize experimental protocols and engineer more resilient organisms [2][5].

### Web Technology Innovations

A notable web technology innovation this month is textarea.my, a minimalist text editor built by Anton Medvedev that lives entirely in the browser and stores everything in the URL hash [4]. At just ~160 lines of HTML, CSS, and JavaScript, the editor demonstrates elegant simplicity while incorporating several advanced browser features [4].

The editor uses the "plaintext-only" value for the contenteditable attribute, which is supported across all modern browsers [4]. It also employs CompressionStream('deflate-raw') to compress the editor state so it can fit in a shorter fragment URL [4]. For saving files, it implements a custom save option triggered by keyboard shortcuts ((e.metaKey || e.ctrlKey) && e.key === 's'), using window.showSaveFilePicker() on supported browsers (mainly Chrome variants) or falling back to a direct download on others [4].

The implementation includes an elegant debounce function that ensures a function runs at most once every specified time period [4]. This approach is demonstrated with the example that "if you call the function five times in quick succession it will execute just once, 100ms after the last of that sequence of calls" [4].

### AI Safety and Security Partnerships

Google DeepMind and the UK AI Security Institute (AISI) have strengthened their collaboration on critical AI safety and security research [6]. This partnership reflects the growing emphasis on ensuring AI systems are developed responsibly and securely [6].

OpenAI is launching the OpenAI Academy for News Organizations, a learning hub built with the American Journalism Project and The Lenfest Institute [3]. The Academy offers training, practical use cases, and responsible-use guidance to support journalists, editors, and publishers as they adopt AI in reporting and operations [3].

These initiatives demonstrate how AI organizations are working with various stakeholders to address safety concerns and promote responsible AI adoption across different sectors [3][6].

### Open Model Development Approaches

Different approaches to open model development were highlighted this month. Some organizations like Moonshot AI and Zhipu focus on one model line at a time, conducting experiments on smaller models that eventually feed back into their main model line for the next generation [9]. In contrast, Qwen3 covers multiple model types including general models, vision, coding, embedding, and reranker models [9].

The Allen Institute for AI (Ai2) continues its tradition of releasing models with all data, code, weights, logs, and methods available [9]. While the industry has shifted to Mixture of Experts (MoEs) for peak performance, Ai2's dense transformer models at 7B and 32B scales serve a crucial niche for accessibility of fine-tuning [9].

Architectural innovations are also emerging in the open model space. Nemotron 2 models are mamba2-transformer hybrids, which improves speed, especially at long contexts, compared to transformer-only models [9]. IBM's Granite 4 adapts the mamba-attention architecture and also releases MoEs [9].

## Tensions & Conflicts

A significant tension exists between benchmark performance and real-world utility of AI models. While open models now rival closed models on most key benchmarks, closed models still dominate in real-world usage [9]. This suggests a disconnect between the metrics we use to evaluate models and their practical value in applications.

There's also an apparent mismatch between quality and recognition for some models. The article on open models suggests that IBM's Granite models deserve more attention than they receive, implying that quality doesn't always correlate with community recognition [9]. Granite 3.2 debuted togglable thinking per prompt, yet the IBM team is "unable to get the attention they deserve" [9].

The ecosystem also shows tension between open and proprietary approaches. Meta's position is described as "weird to place" given reports that they may release proprietary models in the future, making the future of their open-source Llama model uncertain [9]. Similarly, Nathan Lambert expresses appreciation for proprietary models (ChatGPT, Claude, Gemini) while advocating strongly for open models, suggesting a complex relationship between these approaches [10].

## Implications

These developments have significant implications for AI practitioners and researchers. The dramatic improvement in open models means that developers now have more high-quality options for building AI applications without relying exclusively on closed APIs [9]. However, the persistent gap between benchmark performance and real-world utility suggests that practitioners should carefully evaluate models based on their specific use cases rather than benchmark scores alone [9].

The innovations in web technology demonstrate how clever engineering can create powerful tools with minimal code [4], while the advances in AI applications for biology show the growing potential for AI to accelerate scientific research [2][5]. For those working in AI safety, the new interpretability tools and security partnerships provide additional resources for understanding and mitigating risks [6][7].

As we move into 2026, the continued evolution of both open and closed models, along with their applications across various domains, will likely shape how AI is developed, deployed, and regulated.

## Source Cards

[1] OpenAI Blog. (2025, December 11). Update to GPT-5 System Card: GPT-5.2. OpenAI Blog. https://openai.com/index/gpt-5-system-card-update-gpt-5-2

[2] OpenAI Blog. (2025, December 16). Measuring AI's capability to accelerate biological research. OpenAI Blog. https://openai.com/index/accelerating-biological-research-in-the-wet-lab

[3] OpenAI Blog. (2025, December 17). Introducing OpenAI Academy for News Organizations. OpenAI Blog. https://openai.com/index/openai-academy-for-news-organizations

[4] Willison, S. (2025, December 27). textarea.my on GitHub. Simon Willison's Weblog. https://simonwillison.net/2025/Dec/27/textarea-my/#atom-everything

[5] Google DeepMind Blog. (2025, December 4). Engineering more resilient crops for a warming climate. Google DeepMind Blog. https://deepmind.google/blog/engineering-more-resilient-crops-for-a-warming-climate/

[6] Google DeepMind Blog. (2025, December 11). Deepening our partnership with the UK AI Security Institute. Google DeepMind Blog. https://deepmind.google/blog/deepening-our-partnership-with-the-uk-ai-security-institute/

[7] Google DeepMind Blog. (2025, December 16). Gemma Scope 2: helping the AI safety community deepen understanding of complex language model behavior. Google DeepMind Blog. https://deepmind.google/blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/

[8] Lambert, N. (2025, December 10). New Talk: Building Olmo 3 Think. Interconnects. https://www.interconnects.ai/p/building-olmo-3-think

[9] Brand, F. (2025, December 14). 2025 Open Models Year in Review. Interconnects. https://www.interconnects.ai/p/2025-open-models-year-in-review

[10] Lambert, N. (2025, December 18). 2025 Interconnects year in review. Interconnects. https://www.interconnects.ai/p/2025-interconnects-year-in-review