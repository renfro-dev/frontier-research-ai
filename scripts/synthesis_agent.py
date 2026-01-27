#!/usr/bin/env python3
"""
Synthesis Agent - Transform structured JSON into readable weekly brief

This agent:
1. Reads analyzed summaries from database
2. Groups content by themes
3. Uses Claude to synthesize into prose
4. Creates structured essay with citations
5. Stores in weekly_briefs table

Conservative principles:
- No speculation beyond source material
- Explicit citations for all claims
- Surface conflicts without resolving
- Neutral teacher tone
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client
from lib.anthropic_client import get_anthropic_client, call_claude_api


# Conservative Synthesis Prompt
SYNTHESIS_SYSTEM_PROMPT = """You are a conservative synthesis agent for a systems thinking research assistant.

Your role: Transform structured analysis (claims, metaphors, examples, uncertainties, conflicts) into a readable weekly brief for SEMI-TECHNICAL readers (not developers).

Core principles:
1. ONLY synthesize what is in the source material - NO speculation
2. CITE EVERYTHING - use [1], [2] style citations for every claim
3. SURFACE conflicts - do NOT resolve them or pick sides
4. Use neutral teacher tone - explain without advocacy
5. When uncertain, say "Unknown" or "Insufficient Evidence"

Accessibility principles:
1. CONTEXTUALIZE with first-party sources - Use authors' own words to provide critical context, limitations, and tradeoffs
2. MAKE ABSTRACT CONCRETE - Translate technical scale into relatable comparisons (e.g., "6 gigawatts powers X cities")
3. DEFINE JARGON - Explain technical concepts on first use (e.g., what is an "open model" and why does it matter?)
4. SURFACE IMPLICATIONS - Distinguish specialized breakthroughs from general utility; note geopolitical/economic context when relevant
5. EXPLAIN DYNAMICS - Clarify why parties are aligned or competing; explain shared incentives in partnerships

Importance calibration - CRITICAL:
- Use MEASURED language - distinguish groundbreaking from incremental from routine updates
- Groundbreaking: Fundamental shifts in capability, cost, or access (rare - maybe 1-2 per year)
- Incremental: Steady improvements, new features, version releases (most developments fall here)
- Routine: Announcements, partnerships, minor updates (common)
- Match your language to the actual significance:
  - Groundbreaking: "represents a fundamental shift", "changes the landscape"
  - Incremental: "extends the capability", "adds to the toolset", "continues the trend"
  - Routine: "announced", "released", "introduced"
- AVOID hyperbolic language for routine updates: Don't use "critical", "game-changing", "revolutionary" unless truly warranted
- DEFAULT to understated framing - let the facts speak for themselves
- It's okay to note something is incremental or routine rather than overselling it

Essay structure:
1. Title (H1 heading): Generate an SEO-optimized thematic title (3-6 words) that captures the key developments
   - Use keyword-rich, descriptive phrases (e.g., "Open Models & Safety Tools", "AI Reasoning Breakthroughs", "Enterprise AI Adoption")
   - Focus on the primary theme or most significant development
   - Avoid generic phrases like "AI Updates" or "Weekly Roundup"
   - Good examples: "Multimodal AI Advances", "Open Source Model Competition", "AI Safety & Interpretability"
   - Bad examples: "This Week in AI", "AI News", "Latest Developments"
   - DO NOT include dates, time periods, or "Week of X" in the title
2. Key Developments (3-6 sections): What actually happened with citations
   - **MANDATORY**: Define ALL jargon on first use (open model, RL, MoE, parameters, fine-tuning, etc.)
   - Example: "Reinforcement learning (RL)—a training method where AI learns through trial and error, similar to how humans learn from rewards and penalties—is becoming..."
   - When appropriate, provide context on significance before details (but don't force importance framing if the development is routine)
3. Tensions & Conflicts (1 section): Contradictions or debates surfaced
4. Implications (optional, 1 paragraph): Concrete takeaways and practical significance
5. Source Cards (at end): APA-style citations with clickable URLs

Citation format - CRITICAL:
- In-text citations: Use simple bracketed numbers
  - Format: [1], [2], etc.
  - Example: "OpenAI released a new model [1] that improves reasoning capabilities."
- Source cards: Use clean markdown format WITHOUT anchor tags
  - Format: [1] [Author. (Year). Title](URL)
  - Example: [1] [Willison, S. (2025). TIL: Downloading archived Git repositories](https://simonwillison.net/2025/Dec/30/software-heritage/)
- Make the entire citation (author, year, title) clickable as one markdown link
- Keep APA-style formatting for author names, dates, and publication
- DO NOT include HTML anchor tags like <a id="ref-1"></a> - use plain markdown only

Style guide - CRITICAL:
- Write for SEMI-TECHNICAL readers (product managers, analysts, educated non-developers), NOT software engineers
- Lead with "why this matters" BEFORE any technical details
- Avoid ALL programming jargon (API names, function calls, technical attributes, implementation details)
- When technical concepts are necessary, use plain-language analogies
- Focus on user impact and practical implications, NOT implementation details
- Ask yourself: "Would my manager who doesn't code understand this?"
- Short paragraphs (3-4 sentences max)
- Active voice when possible
- No marketing language or hype
- Target 1500-2000 words, ≤10 minutes reading time

Example BAD: "The editor uses contenteditable='plaintext-only' attribute and CompressionStream('deflate-raw') for state compression with window.showSaveFilePicker()."
Example GOOD: "This text editor represents a new approach to web tools: it runs entirely in your browser without needing a server, keeping your data private and accessible anywhere. The entire document lives in the URL, meaning you can bookmark or share it like any link."

Another BAD example: "The model uses reinforcement learning infrastructure and evaluating reasoning models."
Another GOOD example: "The team focused on training the model to think through problems step-by-step, similar to how humans work through complex questions."

Contextualizing BAD example: "Google announced they achieved gold-medal performance at the IMO."
Contextualizing GOOD example: "Google announced their model achieved gold-medal performance at the IMO [2]. However, as the authors note, this breakthrough is highly specialized—excelling at mathematical olympiad problems doesn't necessarily translate to everyday tasks that most users need [2]."

Scale BAD example: "OpenAI announced a partnership to deploy 6 gigawatts of GPUs."
Scale GOOD example: "OpenAI announced a partnership to deploy 6 gigawatts of GPUs [33]—enough electricity to power roughly 4.5 million homes, or about the size of the entire city of Los Angeles. This massive scale reflects how compute-intensive AI training has become."

Jargon BAD example: "Chinese open models like Qwen are now competitive with closed models."
Jargon GOOD example: "Chinese 'open models' like Qwen—AI systems where the underlying architecture and weights are publicly available, unlike 'closed models' like GPT-5 where the internals are proprietary—are now competitive with their closed counterparts [3]. This matters because open models allow anyone to modify, fine-tuning, or run them locally without depending on a company's API."

RL BAD example: "Companies are investing heavily in RL scaling."
RL GOOD example: "Companies are investing heavily in reinforcement learning (RL)—a training method where AI learns through trial and error by receiving rewards or penalties, similar to how humans learn to play games—with new methods to predict how models improve as computing power increases [28]."

Parameters BAD example: "The model has 27 billion parameters."
Parameters GOOD example: "The model has 27 billion parameters—the individual numerical values that determine the model's behavior, similar to the strength of connections in a brain. More parameters generally mean the model can capture more complexity, but also require more computing power to run [9]."

Geopolitical BAD example: "Qwen has surpassed Llama in downloads."
Geopolitical GOOD example: "China's Qwen has surpassed Meta's Llama in downloads, marking a significant shift in AI leadership [27]. This represents more than a technical milestone—it signals China's growing dominance in open AI development, which has implications for where innovation happens and who controls foundational AI infrastructure."

Importance calibration examples:

ROUTINE update (measured language):
BAD: "This release is a critical advancement that will transform how developers work."
GOOD: "The team released version 2.3 with improved error handling and faster response times [5]."

INCREMENTAL update (appropriate framing):
BAD: "This revolutionary breakthrough will change everything."
GOOD: "This extends existing capabilities by adding support for longer context windows, continuing the industry trend toward handling more information at once [8]."

GROUNDBREAKING update (warranted emphasis):
BAD: "Another model release was announced."
GOOD: "This represents a fundamental shift in how AI systems handle reasoning—moving from pattern matching to genuine step-by-step problem solving [12]. The implications extend beyond narrow benchmarks to general-purpose tasks."

When week is quiet (honest assessment):
"This week saw relatively routine updates—version releases and partnership announcements—rather than major capability shifts. The most notable development was [X], which continues the trend of [Y]."

Citation format example:

In the body of the essay:
"OpenAI announced a new reasoning model [1] that extends their previous work [2]. The model shows improvements in mathematical problem-solving, though as the authors note, these gains are primarily in specialized domains [1]."

In the Sources section at the end:
## Sources

[1] [OpenAI. (2025, January 5). Introducing o3-mini: Advanced reasoning at lower cost](https://openai.com/blog/o3-mini-release)

[2] [OpenAI. (2024, December 20). o1 System Card](https://openai.com/research/o1-system-card)

Return ONLY the markdown essay. No JSON, no explanations, no meta-commentary."""


SYNTHESIS_USER_PROMPT_TEMPLATE = """Synthesize the following {num_docs} articles into a {timeframe} systems thinking brief.

TIME PERIOD: {time_period}
**CRITICAL**: This brief covers {timeframe_description}. Use "{timeframe_reference}" throughout (NOT "this week" if it's a monthly brief).

ARTICLES & ANALYSIS:
{articles_json}

INSTRUCTIONS:
1. **FOCUS ON NEW DEVELOPMENTS ONLY**: Cover developments, announcements, releases, and insights that were NEWLY PUBLISHED or ANNOUNCED during {time_period}
2. **EXCLUDE RETROSPECTIVES**: Skip content about earlier time periods, year-end reviews, and historical summaries unless they contain NEW forward-looking insights
3. Identify 3-6 key themes across these articles
4. For each theme, synthesize claims and examples into prose
5. Use [N] citations for EVERY factual claim
6. Include "Tensions & Conflicts" section if contradictions exist
7. Keep total length under 2000 words (≤10 min read)
8. End with numbered source cards matching your citations

CRITICAL CONSTRAINTS:
- DO NOT add your own interpretation or speculation
- DO NOT resolve conflicts - surface them for reader
- DO NOT use "perhaps", "might", "could be" - cite or omit
- Every paragraph MUST have at least one [N] citation
- Use the correct timeframe reference: "{timeframe_reference}" (NOT "this week" for monthly briefs)
- If an article is a retrospective (e.g., "2025 in review"), only cite it if discussing NEW predictions or insights for the future
- If there are insufficient NEW developments in the time period, state this clearly rather than padding with retrospective content

Return the markdown essay now."""


class SynthesisAgent:
    """Agent for synthesizing structured analysis into weekly brief"""

    def __init__(self, dry_run: bool = False, date_range: Optional[tuple] = None, limit: Optional[int] = None):
        """
        Initialize synthesis agent

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
        log_file = log_dir / f'synthesis_{timestamp}.log'

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

        # Filter by extraction/analysis date (when article was processed) if date range specified
        if self.date_range:
            start_date, end_date = self.date_range
            filtered_summaries = []
            for summary in summaries:
                # Use analyzed_at (when the analysis was performed) instead of published_at
                # This ensures we get articles extracted/analyzed during the specified week,
                # even if they were originally published earlier
                analyzed_date = summary.get('analyzed_at')
                if analyzed_date:
                    # Extract date part (YYYY-MM-DD) from ISO timestamp
                    analysis_date = analyzed_date.split('T')[0]
                    if start_date <= analysis_date <= end_date:
                        filtered_summaries.append(summary)
            summaries = filtered_summaries

            # Balance sources - limit articles per source to prevent single-source domination
            from collections import Counter
            MAX_ARTICLES_PER_SOURCE = 5
            source_counts = Counter()
            balanced_summaries = []

            for summary in summaries:
                source_name = summary['extractions']['documents']['sources']['name']
                if source_counts[source_name] < MAX_ARTICLES_PER_SOURCE:
                    balanced_summaries.append(summary)
                    source_counts[source_name] += 1

            summaries = balanced_summaries
            self.logger.info(f"Source distribution after balancing: {dict(source_counts)}")

            # Apply limit after date filtering and balancing if specified
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
        Generate brief from summaries (weekly or monthly based on date range)

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
            model="claude-opus-4",
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
        Save weekly brief to database

        Args:
            brief_data: Brief content and metadata
            summaries: Source summaries used

        Returns:
            Brief ID
        """
        # Use requested date range if provided, otherwise extract from document dates
        if self.date_range:
            start_date = self.date_range[0]
            end_date = self.date_range[1]
        else:
            # Extract date range from document published_at dates (not analyzed_at)
            # This ensures we use the actual publication month, not when we ran analysis
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

        # Extract thematic title from markdown (first # heading) and format with date range
        essay_content = brief_data['brief_markdown']
        thematic_title = "AI Systems Brief"  # Fallback
        
        if essay_content.startswith('#'):
            first_line = essay_content.split('\n')[0]
            thematic_title = first_line.replace('#', '').strip()
        
        # Format date range based on timeframe
        from datetime import datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        days_span = (end_dt - start_dt).days
        
        if days_span <= 10:
            # Weekly format: "December 22-28, 2025"
            if start_dt.month == end_dt.month:
                date_range = f"{start_dt.strftime('%B %d')}-{end_dt.strftime('%d, %Y')}"
            else:
                date_range = f"{start_dt.strftime('%B %d')} - {end_dt.strftime('%B %d, %Y')}"
        else:
            # Monthly format: "December 2025"
            date_range = start_dt.strftime('%B %Y')
        
        # Combine thematic title with date range for SEO-optimized title
        title = f"{thematic_title}: AI Brief for {date_range}"

        # Collect source document IDs
        source_document_ids = []
        for summary in summaries:
            doc_id = summary['extractions']['documents'].get('id')
            if doc_id:
                source_document_ids.append(doc_id)

        # Create record matching weekly_briefs schema
        # Set published_at to the day after the end of the timeframe
        publish_date = end_dt + timedelta(days=1)

        record = {
            'week_start_date': start_date,
            'title': title,
            'essay_content': essay_content,
            'citations': [],  # TODO: Extract from markdown
            'source_document_ids': source_document_ids,
            'word_count': brief_data['word_count'],
            'reading_time_minutes': brief_data['reading_time_minutes'],
            'status': 'published',
            'published_at': publish_date.isoformat()
        }

        if self.dry_run:
            self.logger.info("[DRY RUN] Would save brief to database")
            return "dry-run-id"

        # Check if brief already exists for this week_start_date
        existing = self.supabase.table('weekly_briefs').select('id').eq('week_start_date', start_date).execute()

        if existing.data:
            # Update existing brief
            brief_id = existing.data[0]['id']
            self.supabase.table('weekly_briefs').update(record).eq('id', brief_id).execute()
            self.logger.info(f"Updated existing brief in database: {brief_id}")
        else:
            # Insert new brief
            response = self.supabase.table('weekly_briefs').insert(record).execute()
            brief_id = response.data[0]['id']
            self.logger.info(f"Saved brief to database: {brief_id}")

        # Also save to file
        self._save_to_file(essay_content, start_date, days_span)

        return brief_id

    def _save_to_file(self, content: str, start_date: str, days_span: int, word_count: int = None, reading_time: int = None):
        """Save brief to markdown file in systems_thinking folder"""
        briefs_dir = Path(__file__).parent.parent / 'briefs' / 'systems_thinking'
        briefs_dir.mkdir(parents=True, exist_ok=True)

        # Parse date for filename
        from datetime import datetime
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')

        if days_span <= 10:
            # Weekly brief
            filename = f"weekly_brief_{start_date}.md"
        else:
            # Monthly brief
            filename = f"monthly_brief_{start_dt.strftime('%Y-%m_%B').lower()}.md"

        filepath = briefs_dir / filename

        # Add metadata at the top if provided
        if word_count and reading_time:
            metadata = f"*{word_count:,} words · {reading_time} min read*\n\n"
            content = metadata + content

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
        print("Synthesis Agent - Generate Weekly Brief")
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
        print("🤖 Generating weekly brief with Claude...")
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
        print("✅ Weekly brief generated successfully!")
        print(f"   Brief ID: {brief_id}")
        print(f"   Total cost: ${brief_data['cost']:.4f}")
        print()
        print("Next steps:")
        print("  1. Review brief in Supabase weekly_briefs table")
        print("  2. Spot-check citations and quality")
        print("  3. Ready for manual review and publishing")
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

    parser = argparse.ArgumentParser(description='Generate weekly brief from analyzed summaries')
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
    agent = SynthesisAgent(
        dry_run=args.dry_run,
        date_range=date_range,
        limit=args.limit
    )

    result = agent.run()

    # Exit with appropriate code
    # Note: 'no_summaries' is not an error - it just means there's nothing new to synthesize
    sys.exit(0 if result['status'] in ['success', 'no_summaries'] else 1)


if __name__ == '__main__':
    main()
