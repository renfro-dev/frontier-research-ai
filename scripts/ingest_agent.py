#!/usr/bin/env python3
"""
Ingest Agent - Fetch content from active RSS sources
"""

import sys
import argparse
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client
from lib.feed_parser import parse_feed, FeedEntry
from lib.content_hasher import calculate_content_hash

class IngestAgent:
    """Main ingest agent class"""

    def __init__(self, supabase, dry_run: bool = False, days_back: int = 30,
                 source_filter: Optional[str] = None, full_history: bool = False,
                 fetch_full_content: bool = False):
        """
        Initialize ingest agent

        Args:
            supabase: Supabase client
            dry_run: If True, don't write to database
            days_back: Only fetch entries from last N days
            source_filter: If provided, only process this source by name
            full_history: If True, fetch all entries regardless of date
            fetch_full_content: If True, fetch full HTML from URLs instead of RSS summaries
        """
        self.supabase = supabase
        self.dry_run = dry_run
        self.days_back = days_back
        self.source_filter = source_filter
        self.full_history = full_history
        self.fetch_full_content = fetch_full_content
        self.logger = logging.getLogger(__name__)

        # Initialize URL fetcher if full content fetching enabled
        if self.fetch_full_content:
            from lib.url_fetcher import ArticleFetcher
            self.fetcher = ArticleFetcher(timeout=15, max_retries=3, rate_limit_delay=1.0)
        else:
            self.fetcher = None

        # Calculate cutoff date
        if full_history:
            self.cutoff_date = None
        else:
            self.cutoff_date = datetime.now() - timedelta(days=days_back)

    def fetch_active_sources(self) -> List[Dict[str, Any]]:
        """
        Get all active sources from database

        Returns:
            List of source records
        """
        query = self.supabase.table('sources').select('*').eq('is_active', True)

        if self.source_filter:
            query = query.ilike('name', f'%{self.source_filter}%')

        result = query.execute()
        return result.data if result.data else []

    def should_fetch_entry(self, entry: FeedEntry) -> bool:
        """
        Determine if entry should be fetched based on publish date

        Args:
            entry: Feed entry to check

        Returns:
            True if should fetch, False otherwise
        """
        if self.full_history or self.cutoff_date is None:
            return True

        if entry.published_at is None:
            # No date - fetch it (we'll use fetched_at)
            return True

        return entry.published_at >= self.cutoff_date

    def document_exists(self, url: str) -> bool:
        """
        Check if document with URL already exists

        Args:
            url: Document URL

        Returns:
            True if exists, False otherwise
        """
        try:
            result = self.supabase.table('documents').select('id').eq('url', url).limit(1).execute()
            return len(result.data) > 0
        except Exception as e:
            self.logger.error(f"Error checking document existence: {str(e)}")
            return False

    def process_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single source - fetch feed and insert documents

        Args:
            source: Source record from database

        Returns:
            Processing stats dict
        """
        stats = {
            "source_name": source['name'],
            "success": False,
            "new_docs": 0,
            "skipped_docs": 0,
            "error": None
        }

        try:
            self.logger.info(f"Fetching feed: {source['rss_feed_url']}")
            print(f"  📡 Fetching: {source['rss_feed_url']}")

            # Parse feed
            entries = parse_feed(source['rss_feed_url'])
            self.logger.info(f"Parsed {len(entries)} entries")
            print(f"  ✅ Feed parsed ({len(entries)} entries)")

            if not entries:
                print(f"  ⏭️  No entries found")
                stats["success"] = True
                return stats

            # Process each entry
            for entry in entries:
                # Check date filter
                if not self.should_fetch_entry(entry):
                    stats["skipped_docs"] += 1
                    continue

                # Check if already exists
                if self.document_exists(entry.url):
                    stats["skipped_docs"] += 1
                    continue

                # Insert document (or skip in dry-run)
                if self.dry_run:
                    stats["new_docs"] += 1
                    self.logger.info(f"[DRY RUN] Would add: {entry.title}")
                else:
                    doc_id = self.insert_document(source['id'], entry)
                    if doc_id:
                        stats["new_docs"] += 1
                        self.logger.info(f"Added document: {entry.title} (ID: {doc_id[:8]}...)")

            print(f"  📝 New articles: {stats['new_docs']}")
            print(f"  ⏭️  Skipped (already exist): {stats['skipped_docs']}")
            print(f"  ✅ Processed successfully\n")
            stats["success"] = True

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error processing {source['name']}: {error_msg}")
            print(f"  ❌ Error: {error_msg}")
            print(f"  ⚠️  Skipping source (will retry next run)\n")
            stats["error"] = error_msg

        return stats

    def insert_document(self, source_id: str, entry: FeedEntry) -> Optional[str]:
        """
        Insert document into database

        Args:
            source_id: UUID of source
            entry: Parsed feed entry

        Returns:
            Document ID if successful, None otherwise
        """
        try:
            # Fetch full content if enabled
            if self.fetch_full_content and self.fetcher:
                result = self.fetcher.fetch_url(entry.url, fallback_content=entry.content)

                if result.success:
                    raw_content = result.html
                    self.logger.info(f"Fetched full content from {entry.url}: {len(raw_content)} chars")
                    fetched_via = "url_fetch"
                else:
                    raw_content = entry.content  # Fallback to RSS summary
                    self.logger.warning(f"Fetch failed for {entry.url}, using RSS summary: {result.error}")
                    fetched_via = "rss_fallback"
            else:
                raw_content = entry.content
                fetched_via = "rss"

            # Calculate content hash
            content_hash = calculate_content_hash(raw_content)

            # Prepare document data
            doc_data = {
                "source_id": source_id,
                "url": entry.url,
                "title": entry.title,
                "author": entry.author,
                "published_at": entry.published_at.isoformat() if entry.published_at else None,
                "raw_content": raw_content,
                "content_hash": content_hash,
                "metadata": {
                    "summary": entry.summary,
                    "fetched_via": fetched_via
                }
            }

            # Insert
            result = self.supabase.table('documents').insert(doc_data).execute()
            if result.data:
                return result.data[0]['id']
            return None

        except Exception as e:
            self.logger.error(f"Error inserting document: {str(e)}")
            return None

    def run(self) -> Dict[str, Any]:
        """
        Run the full ingest process

        Returns:
            Summary stats
        """
        summary = {
            "sources_processed": 0,
            "sources_successful": 0,
            "sources_failed": 0,
            "new_documents": 0,
            "skipped_documents": 0,
            "failed_sources": []
        }

        # Fetch sources
        sources = self.fetch_active_sources()

        if not sources:
            self.logger.warning("No active sources found")
            return summary

        self.logger.info(f"Found {len(sources)} active sources")
        print(f"📋 Found {len(sources)} active source{'s' if len(sources) != 1 else ''}\n")
        print("Processing sources...\n")

        # Process each source
        for i, source in enumerate(sources, 1):
            print(f"[{i}/{len(sources)}] {source['name']}")
            summary["sources_processed"] += 1

            stats = self.process_source(source)

            if stats["success"]:
                summary["sources_successful"] += 1
                summary["new_documents"] += stats["new_docs"]
                summary["skipped_documents"] += stats["skipped_docs"]
            else:
                summary["sources_failed"] += 1
                summary["failed_sources"].append({
                    "name": source['name'],
                    "error": stats["error"]
                })

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
    log_file = Path(log_dir) / f"ingest_{timestamp}.log"

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
    parser = argparse.ArgumentParser(description="Ingest content from RSS feeds")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run without writing to database")
    parser.add_argument("--days-back", type=int, default=30,
                       help="Only fetch entries from last N days (default: 30)")
    parser.add_argument("--source", type=str,
                       help="Only process specific source by name")
    parser.add_argument("--full-history", action="store_true",
                       help="Fetch all historical entries (ignores --days-back)")
    parser.add_argument("--fetch-full-content", action="store_true",
                       help="Fetch full article HTML from URLs instead of RSS summaries")
    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    # Print header
    print("=" * 60)
    print("Ingest Agent - RSS Content Fetcher")
    print("=" * 60)
    mode = "DRY RUN (no database writes)" if args.dry_run else "LIVE (writing to database)"
    print(f"Mode: {mode}")
    if args.full_history:
        print(f"Timeframe: All historical content")
    else:
        print(f"Timeframe: Last {args.days_back} days")
    if args.source:
        print(f"Source filter: {args.source}")
    if args.fetch_full_content:
        print(f"Content: Full HTML from URLs (with RSS fallback)")
    else:
        print(f"Content: RSS feed summaries only")
    print()

    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print("✅ Connected to Supabase")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {str(e)}")
        logger.error(f"Failed to connect to Supabase: {str(e)}")
        sys.exit(1)

    # Create and run agent
    agent = IngestAgent(
        supabase=supabase,
        dry_run=args.dry_run,
        days_back=args.days_back,
        source_filter=args.source,
        full_history=args.full_history,
        fetch_full_content=args.fetch_full_content
    )

    summary = agent.run()

    # Print summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Sources processed:     {summary['sources_processed']}")
    print(f"Successful:           {summary['sources_successful']}")
    print(f"Failed:               {summary['sources_failed']}")
    print(f"New documents added:  {summary['new_documents']}")
    print(f"Duplicates skipped:   {summary['skipped_documents']}")

    if summary['failed_sources']:
        print(f"\nFailed sources:")
        for failed in summary['failed_sources']:
            print(f"  - {failed['name']} ({failed['error']})")

    if args.dry_run:
        print(f"\n✅ Dry run completed successfully!")
        print(f"\nRun without --dry-run flag to actually ingest content.")
    elif summary['sources_failed'] > 0:
        print(f"\n⚠️  Some sources failed. Check log file for details.")
    else:
        print(f"\n🎉 All sources processed successfully!")

    print("\nNext steps:")
    if args.dry_run:
        print("  1. Run without --dry-run to actually fetch content")
        print("  2. Check Supabase to verify data")
    else:
        print("  1. Check Supabase to verify documents were added")
        print("  2. Schedule weekly runs via cron")

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
