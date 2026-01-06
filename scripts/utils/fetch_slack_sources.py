#!/usr/bin/env python3
"""
Fetch full text from Slack-related source documents
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.supabase_client import get_supabase_client

def main():
    """Fetch full text from key Slack-related documents"""
    supabase = get_supabase_client()

    # Document IDs of interest
    doc_ids = [
        '4849e172',  # LangSmith Agent Builder
        'fad2b6aa',  # OpenAI Codex
        '0941a970',  # Context Engineering
    ]

    for doc_id_prefix in doc_ids:
        print("=" * 80)

        # Get extraction
        result = supabase.table('extractions').select(
            'id, cleaned_text, document_id'
        ).like('id', f'{doc_id_prefix}%').execute()

        if result.data:
            extraction = result.data[0]

            # Get document info
            doc_result = supabase.table('documents').select(
                'title, url, published_at'
            ).eq('id', extraction['document_id']).execute()

            if doc_result.data:
                doc = doc_result.data[0]
                print(f"Title: {doc['title']}")
                print(f"URL: {doc['url']}")
                print(f"Published: {doc.get('published_at', 'N/A')}")
                print()
                print("Content:")
                print("-" * 80)
                print(extraction['cleaned_text'])
                print()
        else:
            print(f"No extraction found for document ID prefix: {doc_id_prefix}")

        print()

if __name__ == "__main__":
    main()
