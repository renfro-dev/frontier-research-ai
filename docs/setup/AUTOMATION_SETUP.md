# GitHub Actions Automation Setup

This guide will help you set up automated weekly brief generation using GitHub Actions.

## Prerequisites

- GitHub account
- This repository pushed to GitHub (public or private)
- API keys for Supabase, OpenAI, and Anthropic

## Setup Steps

### 1. Push Repository to GitHub

If you haven't already, create a new GitHub repository and push your code:

```bash
cd "/Users/JoshR/Desktop/fun/Frontier AI"

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: Weekly AI Brief system"

# Add remote and push (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Configure GitHub Secrets

Navigate to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

| Secret Name | Value | Where to Find |
|------------|-------|---------------|
| `SUPABASE_URL` | Your Supabase project URL | Supabase Dashboard → Project Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | Your service role key | Supabase Dashboard → Project Settings → API → service_role key |
| `OPENAI_API_KEY` | Your OpenAI API key | OpenAI Platform → API Keys |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Anthropic Console → API Keys |

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**

### 4. Verify Workflow

The workflow is located at `.github/workflows/weekly-brief.yml`

**Schedule:** Runs every Monday at 11:00 AM PST (7:00 PM UTC / 2:00 PM EST)

**What it does:**
1. Ingests new content from RSS feeds
2. Extracts and cleans text
3. Generates embeddings
4. Analyzes content with Claude
5. Synthesizes Systems Thinking weekly brief
6. Synthesizes Context Orchestration weekly brief
7. Commits both generated briefs to repository

## Manual Triggering

You can manually trigger the workflow at any time:

1. Go to **Actions** tab in your GitHub repository
2. Click **"Weekly Briefs Pipeline (Systems Thinking & Context Orchestration)"** in the left sidebar
3. Click **"Run workflow"** button
4. Optionally specify custom date range:
   - Start date: `YYYY-MM-DD` (e.g., `2025-12-29`)
   - End date: `YYYY-MM-DD` (e.g., `2026-01-04`)
5. Click **"Run workflow"**

## Monitoring

### View Workflow Runs

- Go to **Actions** tab to see all workflow runs
- Click on any run to see detailed logs for each step
- Green checkmark = success, Red X = failure

### Notifications

By default, GitHub will email you if a workflow fails. You can customize this:

1. Go to your GitHub profile → **Settings** → **Notifications**
2. Under **Actions**, configure your preferences

## Troubleshooting

### Workflow Fails

1. Check the **Actions** tab for error logs
2. Common issues:
   - **Missing secrets**: Verify all 4 secrets are configured correctly
   - **API rate limits**: OpenAI/Anthropic may have rate limits
   - **No new content**: If no articles published that week, synthesis may fail

### Date Calculation Issues

The workflow uses `date -d` command which works on Linux (GitHub Actions). If you need to adjust the date calculation logic, edit the "Calculate date range" step in `.github/workflows/weekly-brief.yml`.

### Cost Management

Each weekly run will incur API costs:
- OpenAI (embeddings): ~$0.02-0.05
- Anthropic (analysis + synthesis for both briefs): ~$0.35-0.55
- **Total per week**: ~$0.40-0.60

Monitor your API usage in the respective dashboards.

## Customization

### Change Schedule

Edit the cron expression in `.github/workflows/weekly-brief.yml`:

```yaml
schedule:
  - cron: '0 19 * * 1'  # Every Monday at 7 PM UTC (11 AM PST)
```

Cron format: `minute hour day-of-month month day-of-week`

Examples:
- `0 14 * * 1` - Every Monday at 2 PM UTC (6 AM PST)
- `0 9 * * 5` - Every Friday at 9 AM UTC (1 AM PST)
- `0 0 1 * *` - First day of every month at midnight UTC

### Disable Auto-Commit

If you don't want briefs automatically committed to the repo, remove or comment out the "Commit generated briefs" step in the workflow file.

## Next Steps

Once set up, both weekly briefs will be generated automatically every Monday. You can find them in the `briefs/` directory of your repository:
- Systems Thinking briefs: `briefs/systems_thinking/weekly_brief_YYYY-MM-DD.md`
- Context Orchestration briefs: `briefs/context_orchestration/weekly_brief_YYYY-MM-DD.md`
