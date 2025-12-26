# Setup Guide - Weekly Systems Thinking Brief

## Prerequisites
- [ ] Node.js 18+ or Python 3.9+ installed
- [ ] Git installed
- [ ] Text editor (VS Code, Cursor, etc.)

## Step 1: Supabase Setup

### 1.1 Create Supabase Account
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up for a free account
3. Create a new project:
   - **Name:** `weekly-systems-brief` (or your choice)
   - **Database Password:** (save this securely)
   - **Region:** Choose closest to you

### 1.2 Get Supabase Credentials
1. Once project is created, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** → This is your `SUPABASE_URL`
   - **anon/public key** → This is your `SUPABASE_ANON_KEY`
   - **service_role key** → This is your `SUPABASE_SERVICE_ROLE_KEY` (keep secret!)

### 1.3 Enable pgvector Extension
1. In Supabase dashboard, go to **Database** → **Extensions**
2. Search for "vector"
3. Enable the `vector` extension

## Step 2: Anthropic API Setup

### 2.1 Create Anthropic Account
1. Go to [https://console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Add payment method (Claude API requires billing)

### 2.2 Get API Key
1. Go to **Settings** → **API Keys**
2. Click **Create Key**
3. Name it: `weekly-systems-brief`
4. Copy the key → This is your `ANTHROPIC_API_KEY`
5. **Important:** Save this key immediately, you can't view it again!

## Step 3: Configure Environment Variables

### 3.1 Copy Template
The `.env` file already exists in your project. Open it and fill in the values:

```bash
# Open .env file in your editor
cursor .env
# or
code .env
# or
nano .env
```

### 3.2 Fill in Required Values
Replace the empty values with your actual credentials:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 3.3 Verify Configuration
- [ ] All required variables are filled
- [ ] No trailing spaces or quotes
- [ ] File is saved
- [ ] `.env` is listed in `.gitignore` (already done)

## Step 4: Database Schema Setup

Once you have Supabase credentials configured, we'll create the database tables. You have two options:

### Option A: Using Supabase SQL Editor (Recommended)
1. Go to Supabase dashboard → **SQL Editor**
2. We'll provide SQL scripts in the next phase

### Option B: Using Migration Scripts
1. We'll create migration files you can run via CLI

**Note:** We'll do this in the next step after environment is configured.

## Step 5: Install Dependencies

### If using Python:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies (we'll create requirements.txt next)
pip install -r requirements.txt
```

### If using Node.js:
```bash
# Install dependencies (we'll create package.json next)
npm install
```

## Step 6: Verify Setup

### Test Supabase Connection
We'll create a simple test script to verify your Supabase connection works.

### Test Anthropic API
We'll create a test script to verify your Claude API access.

**Coming in next phase:** Test scripts will be created after we set up the project structure.

## Optional Setup (v2)

### Firecrawl (for blocked sources like OpenAI)
1. Go to [https://firecrawl.dev](https://firecrawl.dev)
2. Sign up for account
3. Get API key from dashboard
4. Add to `.env`:
   ```env
   FIRECRAWL_API_KEY=fc-your-key-here
   ```

### OpenAI (if using for embeddings)
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] Never commit `.env` file to git
- [ ] Never share your service_role key publicly
- [ ] Keep API keys secure
- [ ] Use environment variables, not hardcoded keys

## Troubleshooting

### "Cannot connect to Supabase"
- Verify `SUPABASE_URL` is correct (should start with `https://`)
- Check if project is still active in Supabase dashboard
- Verify API keys are correct (no extra spaces)

### "Anthropic API authentication failed"
- Verify API key starts with `sk-ant-`
- Check if billing is set up in Anthropic console
- Verify key hasn't been revoked

### "pgvector extension not found"
- Go to Supabase → Database → Extensions
- Search for "vector" and enable it
- Restart your application

## Next Steps

Once your environment is configured:
1. ✅ Return to main setup flow
2. Create database schema (Phase 1.1 in TODO.md)
3. Set up project structure
4. Test connections

## Estimated Costs

**Free Tier Limits:**
- **Supabase:** 500MB database, 2GB bandwidth/month (plenty for v1)
- **Anthropic:** Pay-as-you-go, ~$0.003 per 1K tokens (Claude Sonnet)
- **Estimated monthly cost for v1:** $5-15 depending on usage

**Recommendations:**
- Start with Supabase free tier
- Use Claude Sonnet (balance of cost/quality)
- Monitor usage in first month
- Upgrade if needed
