#!/usr/bin/env python3
"""
Context Orchestration Synthesis Agent - Transform structured JSON into context orchestration brief

This agent creates briefs focused on:
- Context orchestration as a meta-skill for high-velocity leaders
- MCP (Model Context Protocol)
- RAG (Retrieval Augmented Generation)
- Vector databases and semantic search
- Agent frameworks and tool use
- Memory systems and context management

The angle: Not "what's new in AI" but "how to leverage context orchestration for decision-making"
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client
from lib.anthropic_client import get_anthropic_client, call_claude_api


# Context Orchestration Synthesis Prompt
SYNTHESIS_SYSTEM_PROMPT = """You are a context orchestration synthesis agent for high-velocity leaders.

Your role: Transform AI developments into actionable insights about CONTEXT ORCHESTRATION - the meta-skill of curating, sequencing, and surfacing information to AI systems for better decision-making.

Core thesis: The bottleneck isn't AI capability—it's humans' ability to orchestrate context effectively.

What is context orchestration?
- **Curation**: Deciding what information to give AI access to (and what to hide)
- **Sequencing**: When to surface what context (real-time vs. pre-loaded)
- **Tools**: MCP, RAG, vector databases, agent frameworks, memory systems
- **Outcome**: Faster decisions with less manual context-switching

Target audience: Non-technical leaders (founders, RevOps, product managers) who need leverage, not technical details.

Essay structure:
1. Title (H1 heading): Generate an SEO-optimized thematic title focused on CONTEXT ORCHESTRATION or LEVERAGE
   - Examples: "Context Orchestration Creates Leverage", "How Leaders Use AI Context Tools", "MCP & RAG for Decision-Makers"
   - Focus on the META-SKILL, not the news
2. Executive Summary: Lead with WHY CONTEXT ORCHESTRATION MATTERS for high-velocity leaders
   - Frame AI developments through the lens of context management
   - Connect to decision-making, velocity, and leverage
3. Core Concepts (2-4 sections): Teach the tools through recent developments
   - Reframe news as examples of context orchestration in action
   - Focus on: MCP, RAG, vector databases, agent frameworks, memory systems
   - **MANDATORY**: Define technical concepts in plain language on first use
4. Practical Applications: How leaders can use these tools TODAY
   - Concrete examples from the articles
   - Reframe "coding agents" as "context orchestration training grounds"
   - Reframe "enterprise AI adoption" as "organizational context management"
5. Tensions & Tradeoffs: Privacy vs. context richness, curation cost vs. AI utility
6. Your Context Orchestration Stack: What to evaluate this quarter
7. Source Cards (at end): APA-style citations

Reframing guidelines:
- "Coding agents" → "Tools that teach context management skills"
- "RAG systems" → "How to surface relevant knowledge at decision time"
- "MCP" → "Giving AI access to your systems without manual copy-paste"
- "Vector databases" → "Making organizational memory searchable"
- "Enterprise adoption" → "What context are they giving 50,000 employees access to?"

Style guide - CRITICAL:
- Write for NON-TECHNICAL executives (NOT developers)
- Lead with LEVERAGE and META-SKILLS before technical details
- Avoid programming jargon entirely
- Use business analogies: "context orchestration is like having a great EA who knows exactly what briefing materials to prepare"
- Focus on DECISION-MAKING VELOCITY, not implementation
- Short paragraphs (3-4 sentences max)
- Active voice, no hype, no speculation
- Target 1500-2000 words, ≤10 minutes reading time

Example reframe:
BAD: "Coding agents are changing software development by managing context windows."
GOOD: "The breakthrough isn't coding agents—it's the meta-skill they expose: context orchestration. Boris Cherny shipped 259 PRs in 30 days not by typing faster, but by learning to curate, prune, and sequence the information his AI sees [27]. This is the same skill high-velocity leaders need: deciding what context to surface, what to hide, and when. Software engineers learned this first; executives are learning it now."

Another example:
BAD: "Commonwealth Bank is rolling out ChatGPT Enterprise to 50,000 employees."
GOOD: "Commonwealth Bank's real innovation isn't deploying ChatGPT—it's the context orchestration problem they solved: which 50,000 employees get access to which organizational knowledge? This is the critical question for every enterprise: not 'should we use AI?' but 'what context should we give it access to?' [33]"

Conservative principles:
1. ONLY synthesize what is in the source material - NO speculation
2. CITE EVERYTHING - use [1], [2] style citations for every claim
3. SURFACE conflicts - do NOT resolve them
4. When uncertain, say "Unknown" or "Insufficient Evidence"
5. Define ALL technical jargon on first use in plain language

Return ONLY the markdown essay. No JSON, no explanations, no meta-commentary."""


SYNTHESIS_USER_PROMPT_TEMPLATE = """Synthesize the following {num_docs} articles into a {timeframe} CONTEXT ORCHESTRATION brief for high-velocity leaders.

TIME PERIOD: {time_period}
**CRITICAL**: This brief covers {timeframe_description}. Use "{timeframe_reference}" throughout (NOT "this week" if it's a monthly brief).

ARTICLES & ANALYSIS:
{articles_json}

INSTRUCTIONS:
1. Identify context orchestration themes: MCP, RAG, vector DBs, agent frameworks, memory, tool use
2. Reframe AI developments through the lens of CONTEXT MANAGEMENT and LEVERAGE
3. Focus on meta-skills leaders can learn, not technical implementations
4. Use [N] citations for EVERY factual claim
5. Include "Tensions & Tradeoffs" section for context orchestration challenges
6. Keep total length under 2000 words (≤10 min read)
7. End with numbered source cards matching your citations

CRITICAL REFRAMING:
- DON'T report AI news generically
- DO extract context orchestration lessons from the news
- Ask: "What does this teach about managing AI context?"
- Connect technical developments to decision-making leverage

CRITICAL CONSTRAINTS:
- DO NOT add your own interpretation or speculation
- DO NOT resolve conflicts - surface them for reader
- DO NOT use "perhaps", "might", "could be" - cite or omit
- Every paragraph MUST have at least one [N] citation
- Use the correct timeframe reference: "{timeframe_reference}" (NOT "this week" for monthly briefs)

Return the markdown essay now."""


class ContextOrchestrationSynthesisAgent:
    """Agent for synthesizing context orchestration focused briefs"""

    def __init__(self, dry_run: bool = False, date_range: Optional[tuple] = None, limit: Optional[int] = None):
        """
        Initialize context orchestration synthesis agent

        Args:
            dry_run: If True, preview without writing to database
            date_range: Tuple of (start_date, end_date) for filtering documents
            limit: Maximum number of summaries to process (for testing)
        """
        self.dry_run = dry_run
        self.date_range = date_range
        self.limit = limit
        self.supabase = get_supabase_client()
        self.anthropic = get_anthropic_client()

        # Setup logging
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'synthesis_orchestration_{timestamp}.log'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logging to: {log_file}")

    def fetch_summaries_to_synthesize(self) -> List[Dict[str, Any]]:
        """
        Fetch summaries for synthesis

        Returns:
            List of summaries with document metadata
        """
        # Get all summaries with their documents
        query = self.supabase.table('summaries').select(
            'id, analysis_json, analyzed_at, '
            'extractions(id, cleaned_text, word_count, '
            'documents(id, title, author, url, published_at, sources(name)))'
        ).order('analyzed_at', desc=True)

        # Apply limit if specified (before filtering by date)
        if self.limit and not self.date_range:
            query = query.limit(self.limit)

        response = query.execute()
        summaries = response.data

        # Filter by document published_at date if date range specified
        if self.date_range:
            start_date, end_date = self.date_range
            filtered_summaries = []
            for summary in summaries:
                pub_date = summary['extractions']['documents'].get('published_at')
                if pub_date:
                    # Extract date part (YYYY-MM-DD) from ISO timestamp
                    doc_date = pub_date.split('T')[0]
                    if start_date <= doc_date <= end_date:
                        filtered_summaries.append(summary)
            summaries = filtered_summaries

            # Apply limit after date filtering if specified
            if self.limit:
                summaries = summaries[:self.limit]

        self.logger.info(f"Found {len(summaries)} summaries to synthesize")
        return summaries

    def prepare_articles_for_synthesis(self, summaries: List[Dict[str, Any]]) -> str:
        """
        Format summaries into JSON for Claude

        Args:
            summaries: List of summary records

        Returns:
            JSON string of formatted articles
        """
        articles = []

        for idx, summary in enumerate(summaries, 1):
            doc = summary['extractions']['documents']
            source = doc['sources']['name']

            article = {
                'citation_number': idx,
                'title': doc['title'],
                'author': doc.get('author') or source,
                'source': source,
                'url': doc['url'],
                'published_at': doc.get('published_at'),
                'analysis': summary['analysis_json']
            }

            articles.append(article)

        return json.dumps(articles, indent=2)

    def synthesize_brief(self, summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate context orchestration brief from summaries

        Args:
            summaries: List of summary records

        Returns:
            Dict with brief_markdown, word_count, reading_time, metadata
        """
        if not summaries:
            raise ValueError("No summaries to synthesize")

        # Determine timeframe from date range
        from datetime import datetime

        pub_dates = []
        for s in summaries:
            pub_date = s['extractions']['documents'].get('published_at')
            if pub_date:
                pub_dates.append(datetime.fromisoformat(pub_date.replace('Z', '+00:00')))

        if pub_dates:
            start_date = min(pub_dates)
            end_date = max(pub_dates)
            days_span = (end_date - start_date).days

            # Determine if weekly or monthly
            if days_span <= 10:
                timeframe = "weekly"
                timeframe_description = f"a week ({start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')})"
                timeframe_reference = "this week"
                time_period = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
            else:
                timeframe = "monthly"
                # Use start_date's month name
                month_name = start_date.strftime('%B %Y')
                timeframe_description = f"the entire month of {month_name}"
                timeframe_reference = "this month"
                time_period = month_name
        else:
            # Fallback
            timeframe = "weekly"
            timeframe_description = "this period"
            timeframe_reference = "this period"
            time_period = "Recent"

        # Prepare articles JSON
        articles_json = self.prepare_articles_for_synthesis(summaries)

        # Build prompt with timeframe context
        user_prompt = SYNTHESIS_USER_PROMPT_TEMPLATE.format(
            num_docs=len(summaries),
            timeframe=timeframe,
            time_period=time_period,
            timeframe_description=timeframe_description,
            timeframe_reference=timeframe_reference,
            articles_json=articles_json
        )

        self.logger.info(f"Calling Claude API to synthesize {len(summaries)} articles...")

        # Call Claude
        response = call_claude_api(
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model="claude-sonnet-4",
            max_tokens=8192,
            temperature=0.0
        )

        brief_markdown = response['content']
        input_tokens = response['input_tokens']
        output_tokens = response['output_tokens']
        cost = response['cost']

        # Calculate reading time (183 words/min average)
        word_count = len(brief_markdown.split())
        reading_time = word_count // 183

        self.logger.info(f"Generated brief: {word_count} words, {reading_time} min read, ${cost:.4f}")

        return {
            'brief_markdown': brief_markdown,
            'word_count': word_count,
            'reading_time_minutes': reading_time,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': cost,
            'num_sources': len(summaries)
        }

    def save_brief(self, brief_data: Dict[str, Any], summaries: List[Dict[str, Any]]) -> str:
        """
        Save context orchestration brief to database

        Args:
            brief_data: Brief content and metadata
            summaries: Source summaries used

        Returns:
            Brief ID
        """
        # Extract date range from document published_at dates
        pub_dates = []
        for s in summaries:
            pub_date = s['extractions']['documents'].get('published_at')
            if pub_date:
                pub_dates.append(pub_date)

        if pub_dates:
            # Use document publication dates
            start_date = min(pub_dates).split('T')[0]
            end_date = max(pub_dates).split('T')[0]
        else:
            # Fallback to analyzed_at if no published_at available
            dates = [s['analyzed_at'] for s in summaries]
            start_date = min(dates).split('T')[0]
            end_date = max(dates).split('T')[0]

        # Extract thematic title from markdown (first # heading)
        essay_content = brief_data['brief_markdown']
        thematic_title = "Context Orchestration Brief"  # Fallback

        if essay_content.startswith('#'):
            first_line = essay_content.split('\n')[0]
            thematic_title = first_line.replace('#', '').strip()

        # Format date range based on timeframe
        from datetime import datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        days_span = (end_dt - start_dt).days

        # Determine period type
        if days_span <= 10:
            period_type = 'weekly'
            # Weekly format: "December 22-28, 2025"
            if start_dt.month == end_dt.month:
                date_range = f"{start_dt.strftime('%B %d')}-{end_dt.strftime('%d, %Y')}"
            else:
                date_range = f"{start_dt.strftime('%B %d')} - {end_dt.strftime('%B %d, %Y')}"
        else:
            period_type = 'monthly'
            # Monthly format: "December 2025"
            date_range = start_dt.strftime('%B %Y')

        # Combine thematic title with date range
        title = f"{thematic_title}: {date_range}"

        # Collect source document IDs
        source_document_ids = []
        for summary in summaries:
            doc_id = summary['extractions']['documents'].get('id')
            if doc_id:
                source_document_ids.append(doc_id)

        # Create record matching context_orchestration_briefs schema
        record = {
            'period_start_date': start_date,
            'period_end_date': end_date,
            'period_type': period_type,
            'title': title,
            'essay_content': essay_content,
            'citations': [],  # TODO: Extract from markdown
            'source_document_ids': source_document_ids,
            'model_used': 'claude-sonnet-4',
            'prompt_version': 'v1.0-context-orchestration',
            'word_count': brief_data['word_count'],
            'reading_time_minutes': brief_data['reading_time_minutes'],
            'metadata': {
                'input_tokens': brief_data['input_tokens'],
                'output_tokens': brief_data['output_tokens'],
                'cost': brief_data['cost']
            }
        }

        if self.dry_run:
            self.logger.info("[DRY RUN] Would save brief to database")
            # Also save to file in dry run mode
            self._save_to_file(essay_content, start_date, period_type)
            return "dry-run-id"

        # Check if brief already exists for this period
        existing = self.supabase.table('context_orchestration_briefs').select('id').eq(
            'period_start_date', start_date
        ).eq('period_type', period_type).execute()

        if existing.data:
            # Update existing brief
            brief_id = existing.data[0]['id']
            self.supabase.table('context_orchestration_briefs').update(record).eq('id', brief_id).execute()
            self.logger.info(f"Updated existing brief in database: {brief_id}")
        else:
            # Insert new brief
            response = self.supabase.table('context_orchestration_briefs').insert(record).execute()
            brief_id = response.data[0]['id']
            self.logger.info(f"Saved brief to database: {brief_id}")

        # Also save to file
        self._save_to_file(essay_content, start_date, period_type)

        return brief_id

    def _save_to_file(self, content: str, start_date: str, period_type: str):
        """Save brief to markdown file"""
        briefs_dir = Path(__file__).parent.parent / 'briefs' / 'context_orchestration'
        briefs_dir.mkdir(parents=True, exist_ok=True)

        # Parse date for filename
        from datetime import datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')

        if period_type == 'monthly':
            filename = f"monthly_brief_{start_dt.strftime('%Y-%m_%B').lower()}.md"
        else:
            filename = f"weekly_brief_{start_date}.md"

        filepath = briefs_dir / filename

        with open(filepath, 'w') as f:
            f.write(content)

        self.logger.info(f"Saved brief to file: {filepath}")

    def run(self) -> Dict[str, Any]:
        """
        Run synthesis pipeline

        Returns:
            Summary statistics
        """
        print("=" * 60)
        print("Context Orchestration Synthesis Agent")
        print("=" * 60)
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE (writing to database)'}")
        print(f"Date range: {self.date_range or 'All summaries'}")
        print()

        # Verify connections
        print("✅ Connected to Supabase")
        print("✅ Anthropic API key verified")
        print()

        # Fetch summaries
        summaries = self.fetch_summaries_to_synthesize()

        if not summaries:
            print("❌ No summaries found to synthesize")
            return {'status': 'no_summaries'}

        print(f"📋 Found {len(summaries)} summaries to synthesize")
        print()

        # Generate brief
        print("🤖 Generating context orchestration brief with Claude...")
        brief_data = self.synthesize_brief(summaries)

        print()
        print("📊 Brief Statistics:")
        print(f"   Word count: {brief_data['word_count']}")
        print(f"   Reading time: {brief_data['reading_time_minutes']} minutes")
        print(f"   Sources: {brief_data['num_sources']}")
        print(f"   Cost: ${brief_data['cost']:.4f}")
        print()

        # Save to database
        brief_id = self.save_brief(brief_data, summaries)

        # Preview first 500 chars
        preview = brief_data['brief_markdown'][:500]
        print("📝 Preview (first 500 chars):")
        print("-" * 60)
        print(preview)
        print("..." if len(brief_data['brief_markdown']) > 500 else "")
        print("-" * 60)
        print()

        print("=" * 60)
        print("✅ Context orchestration brief generated successfully!")
        print(f"   Brief ID: {brief_id}")
        print(f"   Total cost: ${brief_data['cost']:.4f}")
        print()
        print("Next steps:")
        print("  1. Review brief in Supabase context_orchestration_briefs table")
        print("  2. Compare with systems thinking brief")
        print("  3. Spot-check citations and context orchestration framing")
        print("=" * 60)

        return {
            'status': 'success',
            'brief_id': brief_id,
            'word_count': brief_data['word_count'],
            'reading_time': brief_data['reading_time_minutes'],
            'sources': brief_data['num_sources'],
            'cost': brief_data['cost']
        }


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate context orchestration brief from analyzed summaries')
    parser.add_argument('--dry-run', action='store_true', help='Preview without database writes')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--limit', type=int, help='Limit number of summaries (for testing)')

    args = parser.parse_args()

    # Parse date range
    date_range = None
    if args.start_date and args.end_date:
        date_range = (args.start_date, args.end_date)

    # Create and run agent
    agent = ContextOrchestrationSynthesisAgent(
        dry_run=args.dry_run,
        date_range=date_range,
        limit=args.limit
    )

    result = agent.run()

    # Exit with appropriate code
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
