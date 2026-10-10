# Frontier Research AI

An automated research pipeline that reads long-form writing from leading AI and systems thinkers and turns it into cited weekly briefs for non-technical operators and founders.

Briefs are published at [renfro.dev/research](https://renfro.dev/research), and every generated brief is committed to [`briefs/`](briefs/).

## What it produces

Two briefs each week, plus monthly roll-ups:

- **Systems Thinking:** translates the week's AI developments into concrete mental models and practical takeaways. See [`briefs/systems_thinking/`](briefs/systems_thinking/).
- **Context Orchestration:** executive-focused analysis of how AI changes work, centered on the skill of curating and orchestrating context. See [`briefs/context_orchestration/`](briefs/context_orchestration/).

Every brief follows the same shape: an executive summary that leads with why it matters, three to six key developments, tensions and disagreements between sources, implications for practitioners, and numbered APA source cards.

## Who it's for

Founders, operators, RevOps leaders, and product managers who want to stay current on AI without reading raw research or hype, and who need citations they can check.

## How it works

Six agents run in sequence. Five are implemented; the reviewer is planned.

| # | Agent | What it does | Built with |
|---|-------|--------------|------------|
| 1 | Ingest | Fetches new posts from curated RSS feeds, skipping URLs already stored | `feedparser` |
| 2 | Extraction | Strips boilerplate and segments the article body. No interpretation | BeautifulSoup |
| 3 | Embedding | Creates 1,536-dimension vectors for deduplication and theme clustering | OpenAI `text-embedding-3-small` |
| 4 | Analysis | Extracts claims, metaphors, examples, uncertainties, and conflicts as structured JSON | Claude Sonnet 4 |
| 5 | Synthesis | Writes the brief from the structured analysis, with a citation for every claim | Claude Sonnet 4 |
| 6 | Reviewer (planned) | Gate for citation coverage and hallucination checks before publishing | — |

A human still reads each brief before it is published.

Data lives in Supabase: Postgres tables for `sources`, `documents`, `extractions`, `summaries`, and `weekly_briefs`, with pgvector for the embeddings.

### Principles

- **Conservative synthesis.** Nothing beyond the source material. "Unknown" is a valid answer, and conflicting views are surfaced, not resolved.
- **Cite everything.** Every claim carries an APA citation and a link to the original.
- **Plain English.** Jargon is defined on first use. The test: would a product manager with no coding background understand it without searching?
- **First-party, long-form sources only.** Personal and official engineering blogs. No social posts, podcasts, or video.

## Automation

[`.github/workflows/weekly-brief.yml`](.github/workflows/weekly-brief.yml) runs the full pipeline every Monday at 03:00 UTC and commits both briefs to the repository. It can also be triggered manually with a custom date range.

Typical cost is about $0.40 to $0.60 per weekly run.

## Run it yourself

Requires Python 3.8+, a Supabase project, an OpenAI API key, and an Anthropic API key.

```bash
git clone https://github.com/renfro-dev/frontier-research-ai.git
cd frontier-research-ai
pip install -r requirements.txt
cp .env.example .env   # then add your keys
```

Apply the SQL files in [`migrations/`](migrations/) to your Supabase database in order, then load the sources and run the pipeline:

```bash
python scripts/utils/add_sources.py

python scripts/ingest_agent.py
python scripts/extraction_agent.py
python scripts/embedding_agent.py
python scripts/analysis_agent.py

python scripts/synthesis_agent.py --start-date 2025-12-29 --end-date 2026-01-04
python scripts/synthesis_agent_orchestration.py --start-date 2025-12-29 --end-date 2026-01-04
```

Briefs are written to `briefs/` and stored in the `weekly_briefs` table.

## Project structure

```
scripts/            One script per agent, plus utilities
scripts/linkedin/   Turns Context Orchestration briefs into LinkedIn post drafts
lib/                Shared clients and helpers (feeds, cleaning, embeddings, Claude, Supabase)
migrations/         Database schema
briefs/             Generated briefs
docs/               Setup guides, planning, and source research
```

## More docs

- [docs/setup/SETUP.md](docs/setup/SETUP.md): full setup walkthrough
- [docs/setup/AUTOMATION_SETUP.md](docs/setup/AUTOMATION_SETUP.md): GitHub Actions configuration
- [docs/LINKEDIN_SETUP.md](docs/LINKEDIN_SETUP.md): LinkedIn post automation
- [docs/planning/PRD.md](docs/planning/PRD.md): product requirements

## Status

Single-author project, v1. Not currently accepting contributions.
