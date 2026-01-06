#!/usr/bin/env python3
"""
Query the vector database for mentions of Slack
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.supabase_client import get_supabase_client

def main():
    """Query database for Slack mentions"""
    print("=" * 60)
    print("Querying Vector Database for Slack Mentions")
    print("=" * 60)
    print()

    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print("✅ Connected to Supabase\n")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {str(e)}")
        sys.exit(1)

    # Query for Slack mentions in extractions
    try:
        result = supabase.table('extractions').select(
            'id, document_id, cleaned_text, created_at'
        ).ilike('cleaned_text', '%slack%').execute()

        if not result.data:
            print("No mentions of 'Slack' found in the database.")
            return

        print(f"Found {len(result.data)} extraction(s) mentioning 'Slack':\n")

        for extraction in result.data:
            print("-" * 60)
            print(f"Extraction ID: {extraction['id'][:8]}...")
            print(f"Document ID: {extraction['document_id'][:8]}...")
            print(f"Created: {extraction['created_at']}")

            # Find and display context around "slack" mention
            text = extraction['cleaned_text']
            text_lower = text.lower()
            slack_positions = []

            # Find all occurrences of "slack"
            pos = 0
            while True:
                pos = text_lower.find('slack', pos)
                if pos == -1:
                    break
                slack_positions.append(pos)
                pos += 1

            print(f"\nFound {len(slack_positions)} mention(s) of 'slack' in this text:\n")

            # Display context for each mention
            for i, pos in enumerate(slack_positions[:3], 1):  # Show first 3 mentions
                start = max(0, pos - 200)
                end = min(len(text), pos + 200)
                context = text[start:end]

                # Add ellipsis if truncated
                if start > 0:
                    context = "..." + context
                if end < len(text):
                    context = context + "..."

                print(f"Mention {i}:")
                print(context)
                print()

            if len(slack_positions) > 3:
                print(f"... and {len(slack_positions) - 3} more mention(s)\n")

        # Also check documents table for source URLs
        print("\n" + "=" * 60)
        print("Checking source documents...")
        print("=" * 60 + "\n")

        doc_ids = [ext['document_id'] for ext in result.data]
        docs_result = supabase.table('documents').select(
            'id, url, title, source_id'
        ).in_('id', doc_ids).execute()

        if docs_result.data:
            print(f"Source document(s):\n")
            for doc in docs_result.data:
                print(f"- {doc.get('title', 'Untitled')}")
                print(f"  URL: {doc['url']}")
                print(f"  Document ID: {doc['id'][:8]}...")
                print()

    except Exception as e:
        print(f"❌ Query failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("=" * 60)

if __name__ == "__main__":
    main()
