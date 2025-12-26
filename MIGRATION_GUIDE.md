# Database Migration Guide

## Quick Start (Recommended Method)

The easiest way to run migrations is through the Supabase SQL Editor.

### Steps:

1. **Open Supabase SQL Editor**
   - Go to your Supabase dashboard
   - Navigate to: **SQL Editor** (left sidebar)
   - Click **New Query**

2. **Run Migration 001 (Initial Schema)**
   - Open: `migrations/001_initial_schema.sql`
   - Copy the entire file contents
   - Paste into SQL Editor
   - Click **Run** (or press Cmd/Ctrl + Enter)
   - Wait for success message: "Migration 001_initial_schema.sql completed successfully"

3. **Run Migration 002 (Indexes)**
   - Open: `migrations/002_indexes_and_constraints.sql`
   - Copy the entire file contents
   - Paste into SQL Editor
   - Click **Run**
   - Wait for success message

4. **Run Migration 003 (Security)**
   - Open: `migrations/003_rls_policies.sql`
   - Copy the entire file contents
   - Paste into SQL Editor
   - Click **Run**
   - Wait for success message

5. **Verify Schema**
   ```bash
   python3 verify_schema.py
   ```

## Alternative Methods

### Method 2: Direct PostgreSQL Connection

If you have psycopg2 installed:

```bash
# Install psycopg2
pip install psycopg2-binary

# Run migrations
python3 run_migrations_direct.py
```

This will prompt you for your database password and run all migrations automatically.

### Method 3: Manual psql CLI

If you have psql installed:

```bash
# Get your connection string from Supabase dashboard
# Settings → Database → Connection String

psql "your-connection-string" -f migrations/001_initial_schema.sql
psql "your-connection-string" -f migrations/002_indexes_and_constraints.sql
psql "your-connection-string" -f migrations/003_rls_policies.sql
```

## Troubleshooting

### "Extension vector not found"
- Go to Supabase Dashboard → Database → Extensions
- Search for "vector"
- Enable the pgvector extension
- Try migration again

### "Permission denied"
- Make sure you're using the service_role key (not anon key)
- Check that .env has SUPABASE_SERVICE_ROLE_KEY set

### "Table already exists"
- If you need to re-run migrations, first drop tables:
  ```sql
  DROP TABLE IF EXISTS weekly_briefs CASCADE;
  DROP TABLE IF EXISTS summaries CASCADE;
  DROP TABLE IF EXISTS extractions CASCADE;
  DROP TABLE IF EXISTS documents CASCADE;
  DROP TABLE IF EXISTS sources CASCADE;
  ```

## What Gets Created

### Tables (5)
- `sources` - Content source metadata
- `documents` - Raw fetched content
- `extractions` - Cleaned text with embeddings
- `summaries` - LLM analysis outputs
- `weekly_briefs` - Final published essays

### Indexes (20+)
- Performance indexes on all foreign keys
- Vector similarity index (HNSW) on embeddings
- GIN indexes for JSONB columns
- Indexes on commonly queried fields

### Security
- Row Level Security (RLS) enabled on all tables
- Service role has full access
- Public users can read published content only

## Next Steps

After migrations are complete:

1. **Verify schema**: `python3 verify_schema.py`
2. **Create source config**: Add Tier 1 sources to database
3. **Build Ingest Agent**: Start fetching content
