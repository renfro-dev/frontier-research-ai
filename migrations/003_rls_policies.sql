-- Migration 003: Row Level Security (RLS) Policies
-- Sets up security policies for Supabase
-- Depends on: 001_initial_schema.sql, 002_indexes_and_constraints.sql

-- ============================================================================
-- Enable RLS on all tables
-- ============================================================================
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE extractions ENABLE ROW LEVEL SECURITY;
ALTER TABLE summaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_briefs ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- RLS Policies for sources table
-- ============================================================================

-- Allow service role full access
CREATE POLICY "Service role has full access to sources"
    ON sources
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow anon/authenticated users to read active sources
CREATE POLICY "Public can read active sources"
    ON sources
    FOR SELECT
    TO anon, authenticated
    USING (is_active = true);

-- ============================================================================
-- RLS Policies for documents table
-- ============================================================================

-- Allow service role full access
CREATE POLICY "Service role has full access to documents"
    ON documents
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow anon/authenticated users to read documents
CREATE POLICY "Public can read documents"
    ON documents
    FOR SELECT
    TO anon, authenticated
    USING (true);

-- ============================================================================
-- RLS Policies for extractions table
-- ============================================================================

-- Allow service role full access
CREATE POLICY "Service role has full access to extractions"
    ON extractions
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow anon/authenticated users to read extractions
CREATE POLICY "Public can read extractions"
    ON extractions
    FOR SELECT
    TO anon, authenticated
    USING (true);

-- ============================================================================
-- RLS Policies for summaries table
-- ============================================================================

-- Allow service role full access
CREATE POLICY "Service role has full access to summaries"
    ON summaries
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow anon/authenticated users to read summaries
CREATE POLICY "Public can read summaries"
    ON summaries
    FOR SELECT
    TO anon, authenticated
    USING (true);

-- ============================================================================
-- RLS Policies for weekly_briefs table
-- ============================================================================

-- Allow service role full access
CREATE POLICY "Service role has full access to weekly_briefs"
    ON weekly_briefs
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Allow anon/authenticated users to read published briefs only
CREATE POLICY "Public can read published briefs"
    ON weekly_briefs
    FOR SELECT
    TO anon, authenticated
    USING (status = 'published');

-- ============================================================================
-- Success Message
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'Migration 003_rls_policies.sql completed successfully';
    RAISE NOTICE 'Enabled RLS and created security policies for all tables';
END $$;
