#!/usr/bin/env python3
"""
Generate LinkedIn posts from Context Orchestration briefs

Usage:
    # Generate from latest brief
    python scripts/linkedin/generate_linkedin_posts.py

    # Generate from specific brief
    python scripts/linkedin/generate_linkedin_posts.py --brief-id <uuid>

    # Dry run (preview only)
    python scripts/linkedin/generate_linkedin_posts.py --dry-run

    # Regenerate posts for existing brief
    python scripts/linkedin/generate_linkedin_posts.py --brief-id <uuid> --regenerate
"""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.linkedin.config import Config
from scripts.linkedin.post_generator import PostGenerator
from scripts.linkedin.google_docs_creator import GoogleDocsCreator
from scripts.linkedin.google_sheets_tracker import GoogleSheetsTracker
from scripts.linkedin.db_helper import LinkedInPostsDB

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for LinkedIn post generation"""
    parser = argparse.ArgumentParser(
        description='Generate LinkedIn posts from Context Orchestration briefs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from latest brief
  python scripts/linkedin/generate_linkedin_posts.py

  # Generate from specific brief
  python scripts/linkedin/generate_linkedin_posts.py --brief-id abc123...

  # Preview without creating docs
  python scripts/linkedin/generate_linkedin_posts.py --dry-run

  # Regenerate posts (replace existing)
  python scripts/linkedin/generate_linkedin_posts.py --brief-id abc123... --regenerate
        """
    )

    parser.add_argument(
        '--brief-id',
        type=str,
        help='Specific brief UUID to generate posts from'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview posts without creating docs/database records'
    )
    parser.add_argument(
        '--regenerate',
        action='store_true',
        help='Regenerate posts even if they exist'
    )
    parser.add_argument(
        '--num-posts',
        type=int,
        choices=[2, 3],
        default=2,
        help='Number of posts to generate (2 or 3, default: 2)'
    )
    parser.add_argument(
        '--skip-google',
        action='store_true',
        help='Skip Google Docs/Sheets creation (database only)'
    )

    args = parser.parse_args()

    # Print header
    print("=" * 70)
    print("LinkedIn Post Generator")
    print("Context Orchestration Briefs → LinkedIn Posts")
    print("=" * 70)
    print()

    # Validate configuration
    try:
        Config.validate(skip_optional=args.dry_run or args.skip_google)
    except (ValueError, FileNotFoundError) as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease set up credentials following the documentation:")
        print("  docs/setup/LINKEDIN_SETUP.md")
        sys.exit(1)

    # Initialize database
    db = LinkedInPostsDB()

    # Get brief
    if args.brief_id:
        logger.info(f"Loading brief: {args.brief_id}")
        brief = db.get_brief_by_id(args.brief_id)
        if not brief:
            print(f"❌ Brief not found: {args.brief_id}")
            sys.exit(1)
    else:
        logger.info("Loading latest brief")
        brief = db.get_latest_brief()
        if not brief:
            print("❌ No briefs found in database")
            print("\nRun synthesis_agent_orchestration.py first to generate a brief")
            sys.exit(1)

    # Display brief info
    print(f"📄 Brief: {brief['title']}")
    print(f"   ID: {brief['id']}")
    print(f"   Period: {brief['period_start_date']} to {brief['period_end_date']}")
    print(f"   Type: {brief['period_type']}")
    print()

    # Check if posts already exist
    if not args.regenerate and not args.dry_run:
        existing_posts = db.get_posts_by_brief(brief['id'])
        if existing_posts:
            print(f"⚠️  {len(existing_posts)} posts already exist for this brief:")
            for post in existing_posts:
                print(f"   - {post['brief_section_title']} ({post['status']})")
            print()
            print("   Use --regenerate to create new posts anyway")
            sys.exit(0)

    # Generate posts
    print(f"🤖 Generating {args.num_posts} LinkedIn posts with Claude...")
    print()

    try:
        generator = PostGenerator(dry_run=args.dry_run)
        result = generator.generate_posts_from_brief(
            brief_id=brief['id'],
            brief_content=brief['essay_content'],
            brief_title=brief['title'],
            brief_date=f"{brief['period_start_date']} to {brief['period_end_date']}",
            num_posts=args.num_posts
        )

        posts = result['posts']
        cost = result['cost']
        tokens = result['tokens']

        print(f"✅ Generated {len(posts)} posts")
        print(f"   Cost: ${cost:.4f}")
        print(f"   Tokens: {tokens['total']:,} ({tokens['input']:,} in, {tokens['output']:,} out)")
        print()

        # Preview posts
        for i, post in enumerate(posts, 1):
            print(f"--- Post {i}: {post['section_title']} ---")
            print(f"Word count: {post['word_count']}")
            print(f"Char count: {post['character_count']}")
            print()
            # Preview first 150 chars
            preview = post['post_text'][:150]
            if len(post['post_text']) > 150:
                preview += "..."
            print(preview)
            print()

        if args.dry_run:
            print("🔍 DRY RUN - No database records or Google Docs created")
            print()
            print("To actually generate posts, run without --dry-run flag")
            sys.exit(0)

        # Save to database
        print("💾 Saving posts to database...")
        post_ids = []
        for post in posts:
            post_id = db.create_post_record(post)
            post_ids.append(post_id)
            logger.info(f"Created post record: {post_id}")

        print(f"   Saved {len(post_ids)} posts to database")
        print()

        # Create Google Docs and Sheets
        if not args.skip_google:
            print("📝 Creating Google Docs and tracking sheet...")

            docs_creator = GoogleDocsCreator()
            sheets_tracker = GoogleSheetsTracker()

            # Get or create tracking sheet
            spreadsheet_id = sheets_tracker.get_or_create_tracking_sheet()
            sheet_url = sheets_tracker.get_sheet_url(spreadsheet_id)

            # Create docs and add to sheet
            for i, (post, post_id) in enumerate(zip(posts, post_ids), 1):
                # Add brief metadata
                post_with_meta = {
                    **post,
                    'brief_title': brief['title'],
                    'generated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
                }

                # Create Google Doc
                doc_result = docs_creator.create_post_draft(post_with_meta)
                logger.info(f"Created Google Doc: {doc_result['doc_url']}")

                # Add to tracking sheet
                row_number = sheets_tracker.add_post_row(
                    spreadsheet_id=spreadsheet_id,
                    post_data={
                        'doc_url': doc_result['doc_url'],
                        'section_title': post['section_title'],
                        'brief_title': brief['title'],
                        'generated_at': post_with_meta['generated_at'],
                        'word_count': post['word_count']
                    }
                )

                # Update database with Google info
                db.update_google_doc_info(
                    post_id=post_id,
                    doc_id=doc_result['doc_id'],
                    doc_url=doc_result['doc_url']
                )
                db.update_sheets_row(post_id=post_id, row_number=row_number)

                print(f"   ✅ Post {i}: {doc_result['doc_url']}")

            print()
            print("📊 Tracking Sheet:")
            print(f"   {sheet_url}")
            print()

        # Print next steps
        print("=" * 70)
        print("✅ LinkedIn Post Generation Complete!")
        print()
        print("Next steps:")
        print("  1. Review posts in tracking sheet (or Google Docs directly)")
        print("  2. Edit posts as needed")
        print("  3. Check boxes in tracking sheet to approve posts")
        print("  4. Webhook will automatically publish to LinkedIn")
        print()
        print("Webhook server:")
        print("  Start: python scripts/linkedin/webhook_listener.py")
        print("  Health check: http://localhost:5000/health")
        print("=" * 70)

    except Exception as e:
        logger.error(f"Post generation failed: {e}", exc_info=True)
        print()
        print(f"❌ Error: {e}")
        print()
        print("Check logs for details")
        sys.exit(1)


if __name__ == '__main__':
    main()
