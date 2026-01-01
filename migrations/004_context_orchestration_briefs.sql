-- Migration 004: Context Orchestration Briefs Table
-- Creates a separate table for context orchestration focused briefs
-- This allows maintaining both systems thinking and context orchestration briefs in parallel

-- ============================================================================
-- Table: context_orchestration_briefs
-- Stores briefs focused on context orchestration topics (MCP, RAG, vector DBs, agents)
-- ============================================================================
CREATE TABLE context_orchestration_briefs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    period_type TEXT NOT NULL CHECK (period_type IN ('weekly', 'monthly', 'quarterly')),
    title TEXT NOT NULL,
    essay_content TEXT NOT NULL,
    citations JSONB NOT NULL DEFAULT '[]'::jsonb,
    source_document_ids UUID[] NOT NULL DEFAULT ARRAY[]::UUID[],
    model_used TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    word_count INTEGER,
    reading_time_minutes INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT context_orchestration_briefs_period_unique UNIQUE (period_start_date, period_type)
);

COMMENT ON TABLE context_orchestration_briefs IS 'Context orchestration focused briefs for high-velocity leaders';
COMMENT ON COLUMN context_orchestration_briefs.period_type IS 'Type of brief period: weekly, monthly, or quarterly';
COMMENT ON COLUMN context_orchestration_briefs.essay_content IS 'Full markdown essay content';
COMMENT ON COLUMN context_orchestration_briefs.citations IS 'Array of citation objects with APA formatting';
COMMENT ON COLUMN context_orchestration_briefs.source_document_ids IS 'Array of document UUIDs used in this brief';
COMMENT ON COLUMN context_orchestration_briefs.model_used IS 'LLM model identifier used for synthesis';
COMMENT ON COLUMN context_orchestration_briefs.prompt_version IS 'Version identifier for tracking prompt changes';
COMMENT ON COLUMN context_orchestration_briefs.metadata IS 'Flexible JSON field for additional metadata';

-- Create index for efficient date range queries
CREATE INDEX idx_context_orch_briefs_period_dates
ON context_orchestration_briefs(period_start_date, period_end_date);

-- Create index for published briefs
CREATE INDEX idx_context_orch_briefs_published
ON context_orchestration_briefs(published_at)
WHERE published_at IS NOT NULL;

-- Create index for period type filtering
CREATE INDEX idx_context_orch_briefs_period_type
ON context_orchestration_briefs(period_type);
