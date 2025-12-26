-- Migration 002: Indexes and Constraints
-- Adds performance indexes and additional constraints
-- Depends on: 001_initial_schema.sql

-- ============================================================================
-- Indexes for sources table
-- ============================================================================
CREATE INDEX idx_sources_domain ON sources(domain);
CREATE INDEX idx_sources_is_active ON sources(is_active);
CREATE INDEX idx_sources_source_type ON sources(source_type);

-- ============================================================================
-- Indexes for documents table
-- ============================================================================
CREATE INDEX idx_documents_source_id ON documents(source_id);
CREATE INDEX idx_documents_url ON documents(url);
CREATE INDEX idx_documents_content_hash ON documents(content_hash);
CREATE INDEX idx_documents_published_at ON documents(published_at DESC);
CREATE INDEX idx_documents_fetched_at ON documents(fetched_at DESC);

-- ============================================================================
-- Indexes for extractions table
-- ============================================================================
CREATE INDEX idx_extractions_document_id ON extractions(document_id);
CREATE INDEX idx_extractions_word_count ON extractions(word_count);

-- Vector similarity index for pgvector
-- Using HNSW (Hierarchical Navigable Small World) for fast approximate nearest neighbor search
CREATE INDEX idx_extractions_embedding ON extractions
    USING hnsw (embedding vector_cosine_ops);

-- ============================================================================
-- Indexes for summaries table
-- ============================================================================
CREATE INDEX idx_summaries_extraction_id ON summaries(extraction_id);
CREATE INDEX idx_summaries_model_used ON summaries(model_used);
CREATE INDEX idx_summaries_analyzed_at ON summaries(analyzed_at DESC);

-- GIN index for efficient JSON queries
CREATE INDEX idx_summaries_analysis_json ON summaries USING gin (analysis_json);

-- ============================================================================
-- Indexes for weekly_briefs table
-- ============================================================================
CREATE INDEX idx_weekly_briefs_week_start_date ON weekly_briefs(week_start_date DESC);
CREATE INDEX idx_weekly_briefs_status ON weekly_briefs(status);
CREATE INDEX idx_weekly_briefs_published_at ON weekly_briefs(published_at DESC);

-- GIN index for efficient JSON queries on citations
CREATE INDEX idx_weekly_briefs_citations ON weekly_briefs USING gin (citations);

-- GIN index for array searches on source_document_ids
CREATE INDEX idx_weekly_briefs_source_document_ids ON weekly_briefs USING gin (source_document_ids);

-- ============================================================================
-- Additional Constraints
-- ============================================================================

-- Ensure reading time is reasonable (between 1 and 60 minutes)
ALTER TABLE extractions ADD CONSTRAINT chk_extractions_reading_time
    CHECK (reading_time_minutes > 0 AND reading_time_minutes <= 60);

ALTER TABLE weekly_briefs ADD CONSTRAINT chk_weekly_briefs_reading_time
    CHECK (reading_time_minutes > 0 AND reading_time_minutes <= 60);

-- Ensure word count is positive
ALTER TABLE extractions ADD CONSTRAINT chk_extractions_word_count
    CHECK (word_count > 0);

ALTER TABLE weekly_briefs ADD CONSTRAINT chk_weekly_briefs_word_count
    CHECK (word_count > 0);

-- Ensure published briefs have a published_at timestamp
ALTER TABLE weekly_briefs ADD CONSTRAINT chk_weekly_briefs_published_at
    CHECK (
        (status = 'published' AND published_at IS NOT NULL) OR
        (status != 'published')
    );

-- ============================================================================
-- Success Message
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE 'Migration 002_indexes_and_constraints.sql completed successfully';
    RAISE NOTICE 'Created indexes for all tables and added data constraints';
END $$;
