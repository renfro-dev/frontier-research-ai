-- Migration 001: Initial Schema
-- Creates all core tables for Weekly Systems Thinking Brief
-- Requires: pgvector extension enabled

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- Table: sources
-- Stores metadata about content sources (blogs, authors)
-- ============================================================================
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL,
    rss_feed_url TEXT,
    source_type TEXT NOT NULL CHECK (source_type IN ('rss', 'html_scrape', 'firecrawl')),
    is_active BOOLEAN NOT NULL DEFAULT true,
    fetch_frequency TEXT NOT NULL DEFAULT 'weekly',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE sources IS 'Content sources (blogs, authors) to scrape';
COMMENT ON COLUMN sources.source_type IS 'Method to fetch content: rss, html_scrape, or firecrawl';
COMMENT ON COLUMN sources.is_active IS 'Whether to actively fetch from this source';

-- ============================================================================
-- Table: documents
-- Stores raw fetched content indefinitely
-- ============================================================================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    author TEXT,
    published_at TIMESTAMPTZ,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    raw_content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE documents IS 'Raw fetched content, preserved indefinitely';
COMMENT ON COLUMN documents.content_hash IS 'Hash for deduplication detection';
COMMENT ON COLUMN documents.metadata IS 'Additional flexible metadata in JSON format';

-- ============================================================================
-- Table: extractions
-- Stores cleaned and processed text from documents
-- ============================================================================
CREATE TABLE extractions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    cleaned_text TEXT NOT NULL,
    sections JSONB DEFAULT '[]'::jsonb,
    word_count INTEGER NOT NULL,
    reading_time_minutes INTEGER NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE extractions IS 'Cleaned and processed text with vector embeddings';
COMMENT ON COLUMN extractions.sections IS 'Segmented sections of the document in JSON format';
COMMENT ON COLUMN extractions.embedding IS 'Vector embedding for semantic similarity search';

-- ============================================================================
-- Table: summaries
-- Stores structured LLM analysis outputs
-- ============================================================================
CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    extraction_id UUID NOT NULL REFERENCES extractions(id) ON DELETE CASCADE,
    analysis_json JSONB NOT NULL,
    model_used TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    analyzed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE summaries IS 'Structured LLM analysis outputs';
COMMENT ON COLUMN summaries.analysis_json IS 'Structured output: claims, metaphors, examples, uncertainties, conflicts';
COMMENT ON COLUMN summaries.model_used IS 'LLM model identifier (e.g., claude-sonnet-4)';
COMMENT ON COLUMN summaries.prompt_version IS 'Version identifier for tracking prompt changes';

-- ============================================================================
-- Table: weekly_briefs
-- Stores final published essays with citations
-- ============================================================================
CREATE TABLE weekly_briefs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    week_start_date DATE NOT NULL UNIQUE,
    title TEXT NOT NULL,
    essay_content TEXT NOT NULL,
    citations JSONB NOT NULL DEFAULT '[]'::jsonb,
    source_document_ids UUID[] NOT NULL DEFAULT ARRAY[]::UUID[],
    word_count INTEGER NOT NULL,
    reading_time_minutes INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'review', 'published')),
    reviewer_passed BOOLEAN,
    reviewer_notes TEXT,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE weekly_briefs IS 'Final published essays with citations and metadata';
COMMENT ON COLUMN weekly_briefs.week_start_date IS 'Start date of week this brief covers (unique)';
COMMENT ON COLUMN weekly_briefs.citations IS 'Array of citation objects in APA format';
COMMENT ON COLUMN weekly_briefs.source_document_ids IS 'Array of document UUIDs cited in this brief';
COMMENT ON COLUMN weekly_briefs.status IS 'Publication status: draft, review, or published';
COMMENT ON COLUMN weekly_briefs.reviewer_passed IS 'Whether the reviewer gate passed';

-- ============================================================================
-- Trigger: Update updated_at timestamp automatically
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_sources_updated_at
    BEFORE UPDATE ON sources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_weekly_briefs_updated_at
    BEFORE UPDATE ON weekly_briefs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Success Message
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'Migration 001_initial_schema.sql completed successfully';
    RAISE NOTICE 'Created tables: sources, documents, extractions, summaries, weekly_briefs';
END $$;
