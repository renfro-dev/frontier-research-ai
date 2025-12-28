#!/usr/bin/env python3
"""
Embedding Agent - Generate vector embeddings for extracted text
"""

import sys
import argparse
import logging
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client
from lib.embedding_generator import generate_embedding, generate_embeddings_batch

class EmbeddingAgent:
    """Main embedding agent class"""

    def __init__(self, supabase, dry_run: bool = False, reprocess: bool = False, batch_size: int = 10):
        """
        Initialize embedding agent

        Args:
            supabase: Supabase client
            dry_run: If True, don't write to database
            reprocess: If True, regenerate embeddings for all extractions
            batch_size: Number of texts to process in a single API call (max 2048)
        """
        self.supabase = supabase
        self.dry_run = dry_run
        self.reprocess = reprocess
        self.batch_size = min(batch_size, 2048)  # OpenAI limit
        self.logger = logging.getLogger(__name__)

    def fetch_extractions_to_process(self) -> List[Dict[str, Any]]:
        """
        Get extractions that need embeddings

        Returns:
            List of extraction records
        """
        if self.reprocess:
            # Get all extractions
            result = self.supabase.table('extractions').select('*').execute()
        else:
            # Get extractions without embeddings (embedding is NULL)
            result = self.supabase.table('extractions').select('*').is_('embedding', 'null').execute()

        return result.data if result.data else []

    def process_batch(self, extractions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process a batch of extractions - generate embeddings

        Args:
            extractions: List of extraction records

        Returns:
            Processing stats dict
        """
        stats = {
            "batch_size": len(extractions),
            "success": 0,
            "failed": 0,
            "errors": []
        }

        try:
            self.logger.info(f"Processing batch of {len(extractions)} extractions")

            # Extract texts
            texts = [ext['cleaned_text'] for ext in extractions]

            # Generate embeddings in batch
            embeddings = generate_embeddings_batch(texts)

            # Update each extraction
            for extraction, embedding in zip(extractions, embeddings):
                try:
                    if self.dry_run:
                        self.logger.info(f"[DRY RUN] Would update extraction {extraction['id'][:8]}... with {len(embedding)}-dim embedding")
                        stats["success"] += 1
                    else:
                        # Update extraction with embedding
                        # Convert list to pgvector format (PostgreSQL array)
                        result = self.supabase.table('extractions').update({
                            'embedding': embedding
                        }).eq('id', extraction['id']).execute()

                        if result.data:
                            self.logger.info(f"Updated embedding for extraction {extraction['id'][:8]}...")
                            stats["success"] += 1
                        else:
                            raise Exception("Update returned no data")

                except Exception as e:
                    error_msg = f"Extraction {extraction['id'][:8]}...: {str(e)}"
                    self.logger.error(f"Error updating extraction: {error_msg}")
                    stats["failed"] += 1
                    stats["errors"].append(error_msg)

        except Exception as e:
            error_msg = f"Batch processing failed: {str(e)}"
            self.logger.error(error_msg)
            stats["failed"] = len(extractions)
            stats["errors"].append(error_msg)

        return stats

    def run(self) -> Dict[str, Any]:
        """
        Run the full embedding generation process

        Returns:
            Summary stats
        """
        summary = {
            "extractions_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_tokens_estimated": 0,
            "estimated_cost": 0.0,
            "errors": []
        }

        # Fetch extractions
        extractions = self.fetch_extractions_to_process()

        if not extractions:
            self.logger.warning("No extractions to process")
            return summary

        self.logger.info(f"Found {len(extractions)} extraction{'s' if len(extractions) != 1 else ''} to process")
        print(f"📋 Found {len(extractions)} extraction{'s' if len(extractions) != 1 else ''} to process")

        # Estimate tokens and cost
        total_words = sum(ext['word_count'] for ext in extractions)
        estimated_tokens = int(total_words * 1.3)  # ~1.3 tokens per word
        estimated_cost = (estimated_tokens / 1_000_000) * 0.02  # $0.02 per 1M tokens

        summary["total_tokens_estimated"] = estimated_tokens
        summary["estimated_cost"] = estimated_cost

        print(f"📊 Estimated: ~{estimated_tokens:,} tokens, ~${estimated_cost:.4f} cost\n")

        # Process in batches
        total_batches = (len(extractions) + self.batch_size - 1) // self.batch_size
        print(f"Processing in {total_batches} batch{'es' if total_batches != 1 else ''}...\n")

        for i in range(0, len(extractions), self.batch_size):
            batch = extractions[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1

            print(f"[Batch {batch_num}/{total_batches}] Processing {len(batch)} extractions...")

            stats = self.process_batch(batch)

            summary["extractions_processed"] += stats["batch_size"]
            summary["successful"] += stats["success"]
            summary["failed"] += stats["failed"]
            summary["errors"].extend(stats["errors"])

            print(f"  ✅ Success: {stats['success']}, ❌ Failed: {stats['failed']}\n")

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
    log_file = Path(log_dir) / f"embedding_{timestamp}.log"

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
    parser = argparse.ArgumentParser(description="Generate embeddings for extracted text")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run without writing to database")
    parser.add_argument("--reprocess", action="store_true",
                       help="Regenerate embeddings for all extractions")
    parser.add_argument("--batch-size", type=int, default=10,
                       help="Number of texts to process per API call (default: 10, max: 2048)")
    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    # Print header
    print("=" * 60)
    print("Embedding Agent - Generate Vector Embeddings")
    print("=" * 60)
    mode = "DRY RUN (no database writes)" if args.dry_run else "LIVE (writing to database)"
    print(f"Mode: {mode}")
    print(f"Model: text-embedding-3-small (1536 dimensions)")
    print(f"Batch size: {args.batch_size}")
    if args.reprocess:
        print(f"Reprocessing: All extractions")
    else:
        print(f"Reprocessing: Only new extractions")
    print()

    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print("✅ Connected to Supabase")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {str(e)}")
        logger.error(f"Failed to connect to Supabase: {str(e)}")
        sys.exit(1)

    # Verify OpenAI API key
    try:
        from lib.embedding_generator import get_openai_client
        get_openai_client()
        print("✅ OpenAI API key verified\n")
    except Exception as e:
        print(f"❌ OpenAI API key error: {str(e)}")
        logger.error(f"OpenAI API key error: {str(e)}")
        sys.exit(1)

    # Create and run agent
    agent = EmbeddingAgent(
        supabase=supabase,
        dry_run=args.dry_run,
        reprocess=args.reprocess,
        batch_size=args.batch_size
    )

    summary = agent.run()

    # Print summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Extractions processed: {summary['extractions_processed']}")
    print(f"Successful:           {summary['successful']}")
    print(f"Failed:               {summary['failed']}")
    print(f"Estimated tokens:     ~{summary['total_tokens_estimated']:,}")
    print(f"Estimated cost:       ~${summary['estimated_cost']:.4f}")

    if summary['errors']:
        print(f"\nErrors:")
        for error in summary['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
        if len(summary['errors']) > 5:
            print(f"  ... and {len(summary['errors']) - 5} more errors")

    if args.dry_run:
        print(f"\n✅ Dry run completed successfully!")
        print(f"\nRun without --dry-run flag to actually generate embeddings.")
    elif summary['failed'] > 0:
        print(f"\n⚠️  Some extractions failed. Check log file for details.")
    else:
        print(f"\n🎉 All embeddings generated successfully!")

    print("\nNext steps:")
    if args.dry_run:
        print("  1. Run without --dry-run to generate embeddings")
        print("  2. Check Supabase extractions.embedding column")
    else:
        print("  1. Verify embeddings in Supabase extractions table")
        print("  2. Ready for semantic similarity queries!")

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
