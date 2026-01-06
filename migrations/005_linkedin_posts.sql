-- Migration 005: LinkedIn Posts Tracking Table
-- Tracks LinkedIn posts generated from Context Orchestration briefs
-- Author: Claude Code
-- Date: 2026-01-05

-- Create linkedin_posts table
CREATE TABLE IF NOT EXISTS linkedin_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Source brief reference
    brief_id UUID NOT NULL REFERENCES context_orchestration_briefs(id) ON DELETE CASCADE,
    brief_section_title TEXT NOT NULL,

    -- Post content
    post_text TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    character_count INTEGER NOT NULL,

    -- Google Workspace tracking
    google_doc_id TEXT,
    google_doc_url TEXT,
    google_sheets_row INTEGER,

    -- LinkedIn publishing
    linkedin_post_id TEXT,
    linkedin_post_url TEXT,
    published_at TIMESTAMPTZ,

    -- Status tracking
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'approved', 'posted', 'error')),
    error_message TEXT,

    -- Metadata
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    approved_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Prevent duplicate posts from same brief section
    CONSTRAINT linkedin_posts_unique_section UNIQUE (brief_id, brief_section_title)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_linkedin_posts_brief_id ON linkedin_posts(brief_id);
CREATE INDEX IF NOT EXISTS idx_linkedin_posts_status ON linkedin_posts(status);
CREATE INDEX IF NOT EXISTS idx_linkedin_posts_published_at ON linkedin_posts(published_at) WHERE published_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_linkedin_posts_generated_at ON linkedin_posts(generated_at);

-- Add table and column comments
COMMENT ON TABLE linkedin_posts IS 'Tracks LinkedIn posts generated from Context Orchestration briefs';
COMMENT ON COLUMN linkedin_posts.brief_id IS 'Reference to source Context Orchestration brief';
COMMENT ON COLUMN linkedin_posts.brief_section_title IS 'Title of the section from the brief that this post is based on';
COMMENT ON COLUMN linkedin_posts.post_text IS 'Final LinkedIn post text (150-200 words)';
COMMENT ON COLUMN linkedin_posts.status IS 'Post lifecycle: draft → approved → posted (or error)';
COMMENT ON COLUMN linkedin_posts.google_doc_id IS 'Google Docs file ID for draft editing';
COMMENT ON COLUMN linkedin_posts.google_sheets_row IS 'Row number in tracking spreadsheet';
COMMENT ON COLUMN linkedin_posts.linkedin_post_id IS 'LinkedIn post ID from API response';
COMMENT ON COLUMN linkedin_posts.linkedin_post_url IS 'Public URL of published LinkedIn post';
COMMENT ON COLUMN linkedin_posts.metadata IS 'Flexible JSON for additional tracking data (hashtags, engagement metrics, etc.)';

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_linkedin_posts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-update updated_at
CREATE TRIGGER linkedin_posts_updated_at
    BEFORE UPDATE ON linkedin_posts
    FOR EACH ROW
    EXECUTE FUNCTION update_linkedin_posts_updated_at();
