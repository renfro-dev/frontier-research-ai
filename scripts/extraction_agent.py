#!/usr/bin/env python3
"""
Extraction Agent - Clean HTML and extract structured text from documents
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
from lib.text_cleaner import clean_html, calculate_word_count, calculate_reading_time, extract_metadata
from lib.text_segmenter import segment_text, create_summary_excerpt

class ExtractionAgent:
    """Main extraction agent class"""

    def __init__(self, supabase, dry_run: bool = False, reprocess: bool = False):
        """
        Initialize extraction agent

        Args:
            supabase: Supabase client
            dry_run: If True, don't write to database
            reprocess: If True, reprocess documents that already have extractions
        """
        self.supabase = supabase
        self.dry_run = dry_run
        self.reprocess = reprocess
        self.logger = logging.getLogger(__name__)

    def fetch_documents_to_process(self) -> List[Dict[str, Any]]:
        """
        Get documents that need extraction

        Returns:
            List of document records
        """
        if self.reprocess:
            # Get all documents
            result = self.supabase.table('documents').select('*').execute()
        else:
            # Get documents without extractions
            # First get document IDs that already have extractions
            existing = self.supabase.table('extractions').select('document_id').execute()
            existing_ids = [e['document_id'] for e in (existing.data or [])]

            # Fetch documents not in existing list
            if existing_ids:
                result = self.supabase.table('documents').select('*').not_.in_('id', existing_ids).execute()
            else:
                result = self.supabase.table('documents').select('*').execute()

        return result.data if result.data else []

    def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single document - extract clean text

        Args:
            document: Document record from database

        Returns:
            Processing stats dict
        """
        stats = {
            "document_id": document['id'],
            "title": document['title'],
            "success": False,
            "error": None
        }

        try:
            self.logger.info(f"Processing: {document['title']}")

            # Clean HTML
            cleaned_text = clean_html(document['raw_content'])

            if not cleaned_text or len(cleaned_text.strip()) < 100:
                raise ValueError("Cleaned text too short (< 100 chars)")

            # Calculate metrics
            word_count = calculate_word_count(cleaned_text)
            reading_time = calculate_reading_time(cleaned_text)

            # Segment text
            sections = segment_text(cleaned_text)

            # Extract metadata
            html_metadata = extract_metadata(document['raw_content'])

            # Create excerpt
            excerpt = create_summary_excerpt(cleaned_text)

            # Prepare extraction data
            extraction_data = {
                "document_id": document['id'],
                "cleaned_text": cleaned_text,
                "sections": sections,
                "word_count": word_count,
                "reading_time_minutes": reading_time,
                "extracted_at": datetime.now().isoformat()
            }

            # Insert or update extraction
            if self.dry_run:
                stats["success"] = True
                stats["word_count"] = word_count
                stats["reading_time"] = reading_time
                stats["sections"] = len(sections)
                self.logger.info(f"[DRY RUN] Would create extraction: {word_count} words, {reading_time} min read, {len(sections)} sections")
            else:
                # Check if extraction already exists (for reprocess case)
                existing = self.supabase.table('extractions').select('id').eq('document_id', document['id']).execute()

                if existing.data:
                    # Update existing
                    result = self.supabase.table('extractions').update(extraction_data).eq('document_id', document['id']).execute()
                    self.logger.info(f"Updated extraction for: {document['title']}")
                else:
                    # Insert new
                    result = self.supabase.table('extractions').insert(extraction_data).execute()
                    self.logger.info(f"Created extraction for: {document['title']}")

                stats["success"] = True
                stats["word_count"] = word_count
                stats["reading_time"] = reading_time
                stats["sections"] = len(sections)

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error processing {document['title']}: {error_msg}")
            stats["error"] = error_msg

        return stats

    def run(self) -> Dict[str, Any]:
        """
        Run the full extraction process

        Returns:
            Summary stats
        """
        summary = {
            "documents_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_words": 0,
            "total_reading_time": 0,
            "failed_documents": []
        }

        # Fetch documents
        documents = self.fetch_documents_to_process()

        if not documents:
            self.logger.warning("No documents to process")
            return summary

        self.logger.info(f"Found {len(documents)} document{'s' if len(documents) != 1 else ''} to process")
        print(f"📋 Found {len(documents)} document{'s' if len(documents) != 1 else ''} to process\n")
        print("Processing documents...\n")

        # Process each document
        for i, document in enumerate(documents, 1):
            print(f"[{i}/{len(documents)}] {document['title'][:60]}...")
            summary["documents_processed"] += 1

            stats = self.process_document(document)

            if stats["success"]:
                summary["successful"] += 1
                summary["total_words"] += stats.get("word_count", 0)
                summary["total_reading_time"] += stats.get("reading_time", 0)
                print(f"  ✅ {stats['word_count']} words, {stats['reading_time']} min read, {stats['sections']} sections\n")
            else:
                summary["failed"] += 1
                summary["failed_documents"].append({
                    "title": document['title'],
                    "error": stats["error"]
                })
                print(f"  ❌ Error: {stats['error']}\n")

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
    log_file = Path(log_dir) / f"extraction_{timestamp}.log"

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
    parser = argparse.ArgumentParser(description="Extract clean text from HTML documents")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run without writing to database")
    parser.add_argument("--reprocess", action="store_true",
                       help="Reprocess documents that already have extractions")
    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    # Print header
    print("=" * 60)
    print("Extraction Agent - HTML to Clean Text")
    print("=" * 60)
    mode = "DRY RUN (no database writes)" if args.dry_run else "LIVE (writing to database)"
    print(f"Mode: {mode}")
    if args.reprocess:
        print(f"Reprocessing: All documents (including already extracted)")
    else:
        print(f"Reprocessing: Only new documents")
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
    agent = ExtractionAgent(
        supabase=supabase,
        dry_run=args.dry_run,
        reprocess=args.reprocess
    )

    summary = agent.run()

    # Print summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Documents processed:  {summary['documents_processed']}")
    print(f"Successful:          {summary['successful']}")
    print(f"Failed:              {summary['failed']}")
    print(f"Total words:         {summary['total_words']:,}")
    print(f"Total reading time:  {summary['total_reading_time']} minutes")

    if summary['failed_documents']:
        print(f"\nFailed documents:")
        for failed in summary['failed_documents']:
            print(f"  - {failed['title']}: {failed['error']}")

    if args.dry_run:
        print(f"\n✅ Dry run completed successfully!")
        print(f"\nRun without --dry-run flag to actually extract content.")
    elif summary['failed'] > 0:
        print(f"\n⚠️  Some documents failed. Check log file for details.")
    else:
        print(f"\n🎉 All documents processed successfully!")

    print("\nNext steps:")
    if args.dry_run:
        print("  1. Run without --dry-run to actually extract")
        print("  2. Check Supabase extractions table")
    else:
        print("  1. Check Supabase extractions table to verify")
        print("  2. Ready for Phase 4: Generate embeddings")

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
