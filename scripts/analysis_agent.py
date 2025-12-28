#!/usr/bin/env python3
"""
Analysis Agent - Extract structured information from cleaned text using Claude API
"""

import sys
import argparse
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client
from lib.anthropic_client import analyze_text, get_anthropic_client, PROMPT_VERSION
from lib.json_validator import validate_analysis_json, repair_analysis_json, get_analysis_stats

class AnalysisAgent:
    """Main analysis agent class"""

    def __init__(
        self,
        supabase,
        dry_run: bool = False,
        reprocess: bool = False,
        extraction_id: Optional[str] = None,
        limit: Optional[int] = None
    ):
        """
        Initialize analysis agent

        Args:
            supabase: Supabase client
            dry_run: If True, don't write to database
            reprocess: If True, regenerate summaries for all extractions
            extraction_id: If provided, process only this extraction
            limit: If provided, limit number of extractions to process
        """
        self.supabase = supabase
        self.dry_run = dry_run
        self.reprocess = reprocess
        self.extraction_id = extraction_id
        self.limit = limit
        self.logger = logging.getLogger(__name__)

    def fetch_extractions_to_process(self) -> List[Dict[str, Any]]:
        """
        Get extractions that need analysis

        Returns:
            List of extraction records with document metadata
        """
        # If specific extraction requested
        if self.extraction_id:
            result = self.supabase.table('extractions').select(
                'id, document_id, cleaned_text, word_count, documents(title, author, published_at, url)'
            ).eq('id', self.extraction_id).execute()
            return result.data if result.data else []

        # Determine which extractions to fetch
        if self.reprocess:
            # Get all extractions
            query = self.supabase.table('extractions').select(
                'id, document_id, cleaned_text, word_count, documents(title, author, published_at, url)'
            )
        else:
            # Get extractions without summaries
            # First get extraction IDs that already have summaries
            existing = self.supabase.table('summaries').select('extraction_id').execute()
            existing_ids = [e['extraction_id'] for e in (existing.data or [])]

            # Fetch extractions not in existing list
            if existing_ids:
                query = self.supabase.table('extractions').select(
                    'id, document_id, cleaned_text, word_count, documents(title, author, published_at, url)'
                ).not_.in_('id', existing_ids)
            else:
                query = self.supabase.table('extractions').select(
                    'id, document_id, cleaned_text, word_count, documents(title, author, published_at, url)'
                )

        # Apply limit if specified
        if self.limit:
            query = query.limit(self.limit)

        result = query.execute()
        return result.data if result.data else []

    def process_extraction(self, extraction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single extraction - analyze with Claude API

        Args:
            extraction: Extraction record from database

        Returns:
            Processing stats dict
        """
        # Extract document metadata
        doc = extraction.get('documents', {})
        if isinstance(doc, list):
            doc = doc[0] if doc else {}

        title = doc.get('title', 'Unknown')

        stats = {
            "extraction_id": extraction['id'],
            "title": title,
            "success": False,
            "error": None,
            "stats": {},
            "cost_usd": 0.0,
            "input_tokens": 0,
            "output_tokens": 0
        }

        try:
            self.logger.info(f"Analyzing: {title}")

            # Prepare metadata for prompt
            metadata = {
                "title": title,
                "author": doc.get('author', 'Unknown'),
                "published_at": doc.get('published_at', 'Unknown'),
                "word_count": extraction.get('word_count', 0)
            }

            # Call Claude API for analysis
            if self.dry_run:
                # In dry run, simulate successful analysis
                self.logger.info(f"[DRY RUN] Would analyze: {title}")
                stats["success"] = True
                stats["stats"] = {
                    "claims": 10,
                    "metaphors": 3,
                    "examples": 5,
                    "uncertainties": 2,
                    "conflicts": 1
                }
                stats["input_tokens"] = 5000
                stats["output_tokens"] = 1500
                stats["cost_usd"] = 0.038
            else:
                # Real API call
                result = analyze_text(
                    text=extraction['cleaned_text'],
                    metadata=metadata
                )

                # Extract results
                analysis_json = result['analysis_json']
                model_used = result['model_used']
                prompt_version = result['prompt_version']
                input_tokens = result['input_tokens']
                output_tokens = result['output_tokens']
                cost_usd = result['cost_usd']

                # Validate JSON
                is_valid, errors = validate_analysis_json(analysis_json)

                if not is_valid:
                    self.logger.warning(f"Validation errors: {', '.join(errors)}")
                    # Attempt repair
                    try:
                        analysis_json = repair_analysis_json(analysis_json)
                        self.logger.info("Successfully repaired JSON")
                    except Exception as repair_error:
                        raise ValueError(f"JSON validation failed and repair unsuccessful: {errors}")

                # Get stats
                analysis_stats = get_analysis_stats(analysis_json)

                # Insert or update summary
                summary_data = {
                    "extraction_id": extraction['id'],
                    "analysis_json": analysis_json,
                    "model_used": model_used,
                    "prompt_version": prompt_version,
                    "analyzed_at": datetime.now().isoformat()
                }

                # Check if summary already exists (for reprocess case)
                existing = self.supabase.table('summaries').select('id').eq(
                    'extraction_id', extraction['id']
                ).execute()

                if existing.data:
                    # Update existing
                    result = self.supabase.table('summaries').update(summary_data).eq(
                        'extraction_id', extraction['id']
                    ).execute()
                    self.logger.info(f"Updated summary for: {title}")
                else:
                    # Insert new
                    result = self.supabase.table('summaries').insert(summary_data).execute()
                    self.logger.info(f"Created summary for: {title}")

                stats["success"] = True
                stats["stats"] = analysis_stats
                stats["input_tokens"] = input_tokens
                stats["output_tokens"] = output_tokens
                stats["cost_usd"] = cost_usd

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error analyzing {title}: {error_msg}")
            stats["error"] = error_msg

        return stats

    def run(self) -> Dict[str, Any]:
        """
        Run the full analysis process

        Returns:
            Summary stats
        """
        summary = {
            "extractions_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_cost_usd": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "avg_claims": 0,
            "avg_metaphors": 0,
            "avg_examples": 0,
            "avg_uncertainties": 0,
            "avg_conflicts": 0,
            "failed_extractions": []
        }

        # Fetch extractions
        extractions = self.fetch_extractions_to_process()

        if not extractions:
            self.logger.warning("No extractions to process")
            return summary

        self.logger.info(f"Found {len(extractions)} extraction{'s' if len(extractions) != 1 else ''} to process")
        print(f"📋 Found {len(extractions)} extraction{'s' if len(extractions) != 1 else ''} to process")

        if not self.dry_run:
            # Estimate cost
            avg_input_tokens = 5000  # Conservative estimate
            avg_output_tokens = 1500
            estimated_cost = len(extractions) * (
                (avg_input_tokens / 1_000_000) * 3.00 +
                (avg_output_tokens / 1_000_000) * 15.00
            )
            print(f"💰 Estimated cost: ~${estimated_cost:.2f} ({len(extractions)} × ~$0.038/doc)\n")
        else:
            print()

        print("Processing extractions...\n")

        # Track stats for averages
        total_claims = 0
        total_metaphors = 0
        total_examples = 0
        total_uncertainties = 0
        total_conflicts = 0
        successful_count = 0

        # Process each extraction
        for i, extraction in enumerate(extractions, 1):
            # Extract title for display
            doc = extraction.get('documents', {})
            if isinstance(doc, list):
                doc = doc[0] if doc else {}
            title = doc.get('title', 'Unknown')[:70]

            print(f"[{i}/{len(extractions)}] {title}...")
            summary["extractions_processed"] += 1

            stats = self.process_extraction(extraction)

            if stats["success"]:
                summary["successful"] += 1
                summary["total_cost_usd"] += stats["cost_usd"]
                summary["total_input_tokens"] += stats["input_tokens"]
                summary["total_output_tokens"] += stats["output_tokens"]

                # Accumulate stats for averages
                analysis_stats = stats["stats"]
                total_claims += analysis_stats.get("claims", 0)
                total_metaphors += analysis_stats.get("metaphors", 0)
                total_examples += analysis_stats.get("examples", 0)
                total_uncertainties += analysis_stats.get("uncertainties", 0)
                total_conflicts += analysis_stats.get("conflicts", 0)
                successful_count += 1

                if self.dry_run:
                    print(
                        f"  ⏱️  [DRY RUN] {stats['input_tokens']:,} input + "
                        f"{stats['output_tokens']:,} output tokens\n"
                        f"  💰 ${stats['cost_usd']:.4f}\n"
                        f"  📊 Claims: {analysis_stats['claims']}, "
                        f"Metaphors: {analysis_stats['metaphors']}, "
                        f"Examples: {analysis_stats['examples']}\n"
                    )
                else:
                    print(
                        f"  ⏱️  {stats['input_tokens']:,} input + "
                        f"{stats['output_tokens']:,} output tokens\n"
                        f"  💰 ${stats['cost_usd']:.4f}\n"
                        f"  📊 Claims: {analysis_stats['claims']}, "
                        f"Metaphors: {analysis_stats['metaphors']}, "
                        f"Examples: {analysis_stats['examples']}, "
                        f"Uncertainties: {analysis_stats['uncertainties']}, "
                        f"Conflicts: {analysis_stats['conflicts']}\n"
                        f"  ✅ Summary created\n"
                    )
            else:
                summary["failed"] += 1
                summary["failed_extractions"].append({
                    "title": title,
                    "error": stats["error"]
                })
                print(f"  ❌ Error: {stats['error']}\n")

        # Calculate averages
        if successful_count > 0:
            summary["avg_claims"] = round(total_claims / successful_count, 1)
            summary["avg_metaphors"] = round(total_metaphors / successful_count, 1)
            summary["avg_examples"] = round(total_examples / successful_count, 1)
            summary["avg_uncertainties"] = round(total_uncertainties / successful_count, 1)
            summary["avg_conflicts"] = round(total_conflicts / successful_count, 1)

        return summary


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """
    Setup logging to both file and console

    Args:
        log_dir: Directory for log files

    Returns:
        Configured logger
    """
    # Create log directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"analysis_{timestamp}.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging to: {log_file}")

    return logger


def main():
    """Main execution with CLI arguments"""
    parser = argparse.ArgumentParser(description="Analyze cleaned text with Claude API")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run without writing to database")
    parser.add_argument("--reprocess", action="store_true",
                       help="Regenerate summaries for all extractions")
    parser.add_argument("--extraction-id", type=str,
                       help="Process single extraction by ID (UUID)")
    parser.add_argument("--limit", type=int,
                       help="Limit number of extractions to process (for testing)")
    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    # Print header
    print("=" * 60)
    print("Analysis Agent - Claude API Text Analysis")
    print("=" * 60)
    mode = "DRY RUN (no database writes)" if args.dry_run else "LIVE (writing to database)"
    print(f"Mode: {mode}")
    print(f"Model: claude-3-7-sonnet-20250219")
    print(f"Prompt Version: {PROMPT_VERSION}")

    if args.extraction_id:
        print(f"Processing: Single extraction ({args.extraction_id[:8]}...)")
    elif args.reprocess:
        print(f"Reprocessing: All extractions")
    else:
        print(f"Reprocessing: Only new extractions")

    if args.limit:
        print(f"Limit: {args.limit} extraction(s)")

    print()

    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print("✅ Connected to Supabase")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {str(e)}")
        logger.error(f"Failed to connect to Supabase: {str(e)}")
        sys.exit(1)

    # Verify Anthropic API key
    try:
        get_anthropic_client()
        print("✅ Anthropic API key verified\n")
    except Exception as e:
        print(f"❌ Anthropic API key error: {str(e)}")
        logger.error(f"Anthropic API key error: {str(e)}")
        sys.exit(1)

    # Create and run agent
    agent = AnalysisAgent(
        supabase=supabase,
        dry_run=args.dry_run,
        reprocess=args.reprocess,
        extraction_id=args.extraction_id,
        limit=args.limit
    )

    summary = agent.run()

    # Print summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Extractions processed:   {summary['extractions_processed']}")
    print(f"Successful:             {summary['successful']}")
    print(f"Failed:                 {summary['failed']}")
    print(f"Total cost:             ${summary['total_cost_usd']:.2f}")
    print(f"Average cost per doc:   ${summary['total_cost_usd'] / max(summary['successful'], 1):.4f}")
    print(f"Total tokens:           {summary['total_input_tokens']:,} input + {summary['total_output_tokens']:,} output")

    if summary['successful'] > 0:
        print(f"\n📊 Content Statistics:")
        print(f"  Average claims per doc:       {summary['avg_claims']}")
        print(f"  Average metaphors per doc:    {summary['avg_metaphors']}")
        print(f"  Average examples per doc:     {summary['avg_examples']}")
        print(f"  Average uncertainties:        {summary['avg_uncertainties']}")
        print(f"  Average conflicts:            {summary['avg_conflicts']}")

    if summary['failed_extractions']:
        print(f"\nFailed extractions:")
        for failed in summary['failed_extractions'][:5]:  # Show first 5
            print(f"  - {failed['title']}: {failed['error']}")
        if len(summary['failed_extractions']) > 5:
            print(f"  ... and {len(summary['failed_extractions']) - 5} more")

    if args.dry_run:
        print(f"\n✅ Dry run completed successfully!")
        print(f"\nRun without --dry-run flag to actually analyze with Claude API.")
    elif summary['failed'] > 0:
        print(f"\n⚠️  Some extractions failed. Check log file for details.")
    else:
        print(f"\n🎉 All extractions analyzed successfully!")

    print("\nNext steps:")
    if args.dry_run:
        print("  1. Run without --dry-run to actually analyze")
        print("  2. Check Supabase summaries table")
    else:
        print("  1. Verify summaries table in Supabase")
        print("  2. Spot-check 3-5 outputs for quality")
        print("  3. Ready for Phase 6: Synthesis Agent")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
