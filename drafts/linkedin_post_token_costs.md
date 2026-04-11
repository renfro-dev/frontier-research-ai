# draft: linkedin post — token cost reduction

---

late last year i built an ai news engine to read and synthesize first-party sources — anthropic, openai, deepmind, the researchers themselves. no aggregators. no summaries of summaries.

i just reduced the ongoing token cost by 88%.

here's what happened.

the pipeline had been quietly failing for weeks. not crashing — just silently producing nothing. wrong date filters. a query that grew too long for the api to accept. credits that ran out mid-run and told no one. the workflow kept reporting "success."

when i finally dug in, i found three bugs and one bigger problem: i had no idea what anything cost.

i was running the analysis step — structured json extraction, literally just "find the claims and examples in this article" — on sonnet 4 when haiku handles that fine at 12× less cost. synthesis, the step that actually writes the essay, stayed on opus 4 where it belongs. but i was resending its 7,200-token system prompt fresh on every single api call instead of caching it. and i was hitting the api one article at a time instead of batching.

the fixes:
- swapped analysis to haiku 4 (12× cheaper for structured json extraction)
- turned on the batch api across the board (50% off, results in minutes)
- added prompt caching to the synthesis system prompt (90% off on repeat tokens)

weekly run cost: $2.45 → $0.30.

the honest lesson isn't really about which model to use or when to batch. it's this:

**subsidized token costs create lazy ai operators. i was one of them.**

one of the less-obvious advantages of leading enterprise ai work at cadre ai is that i get to see what happens when teams actually track compute — when the bill lands somewhere real. the discipline that comes from that is hard to replicate when you're running personal projects on a credit card you don't check.

if you're building with ai and you haven't looked at your token logs in a while: look.

you'll probably find the same thing i did.

---
*status: draft — do not publish*
