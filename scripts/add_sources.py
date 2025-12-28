#!/usr/bin/env python3
"""
Add Tier 1 content sources to the database
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client

def get_tier1_sources() -> List[Dict[str, Any]]:
    """
    Return list of Tier 1 sources to add

    Returns:
        List of source configuration dicts
    """
    return [
        {
            "name": "Simon Willison's Weblog",
            "url": "https://simonwillison.net/",
            "domain": "simonwillison.net",
            "source_type": "rss",
            "rss_feed_url": "https://simonwillison.net/atom/everything/",
            "is_active": True,
            "fetch_frequency": "weekly"
        },
        {
            "name": "Eugene Yan",
            "url": "https://eugeneyan.com/",
            "domain": "eugeneyan.com",
            "source_type": "rss",
            "rss_feed_url": "https://eugeneyan.com/feed.xml",
            "is_active": True,
            "fetch_frequency": "weekly"
        },
        {
            "name": "Andrej Karpathy",
            "url": "https://karpathy.github.io/",
            "domain": "karpathy.github.io",
            "source_type": "rss",
            "rss_feed_url": "https://karpathy.github.io/feed.xml",
            "is_active": True,
            "fetch_frequency": "weekly"
        },
        {
            "name": "Lilian Weng's Blog",
            "url": "https://lilianweng.github.io/",
            "domain": "lilianweng.github.io",
            "source_type": "rss",
            "rss_feed_url": "https://lilianweng.github.io/index.xml",
            "is_active": True,
            "fetch_frequency": "weekly"
        },
        {
            "name": "Chip Huyen's Blog",
            "url": "https://huyenchip.com/blog/",
            "domain": "huyenchip.com",
            "source_type": "rss",
            "rss_feed_url": "https://huyenchip.com/feed.xml",
            "is_active": True,
            "fetch_frequency": "weekly"
        },
        {
            "name": "Sebastian Raschka's Blog",
            "url": "https://sebastianraschka.com/blog/",
            "domain": "sebastianraschka.com",
            "source_type": "rss",
            "rss_feed_url": "https://sebastianraschka.com/rss_feed.xml",
            "is_active": True,
            "fetch_frequency": "weekly"
        },
        {
            "name": "Vicki Boykis",
            "url": "https://vickiboykis.com/",
            "domain": "vickiboykis.com",
            "source_type": "rss",
            "rss_feed_url": "https://vickiboykis.com/index.xml",
            "is_active": True,
            "fetch_frequency": "weekly"
        }
    ]

def source_exists(supabase, url: str) -> bool:
    """
    Check if source with given URL already exists

    Args:
        supabase: Supabase client
        url: Source URL to check

    Returns:
        True if exists, False otherwise
    """
    try:
        result = supabase.table('sources').select('id').eq('url', url).execute()
        return len(result.data) > 0
    except Exception as e:
        print(f"    ❌ Error checking source: {str(e)}")
        return False

def insert_source(supabase, source: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a single source into the database

    Args:
        supabase: Supabase client
        source: Source data dict

    Returns:
        Inserted source record with ID

    Raises:
        Exception: If insert fails
    """
    result = supabase.table('sources').insert(source).execute()
    if not result.data:
        raise Exception("Insert returned no data")
    return result.data[0]

def main():
    """Main execution"""
    print("=" * 60)
    print("Adding Content Sources")
    print("=" * 60)

    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print("\n✅ Connected to Supabase")
    except Exception as e:
        print(f"\n❌ Failed to connect to Supabase: {str(e)}")
        sys.exit(1)

    # Get sources to add
    sources = get_tier1_sources()
    print(f"\nChecking {len(sources)} sources...\n")

    # Track stats
    added = 0
    existed = 0
    failed = 0

    # Process each source
    for source in sources:
        print(f"  {source['name']}")
        print(f"    URL: {source['url']}")
        print(f"    RSS: {source['rss_feed_url']}")

        try:
            # Check if already exists
            if source_exists(supabase, source['url']):
                print(f"    ⚠️  Already exists (skipping)\n")
                existed += 1
                continue

            # Insert source
            inserted = insert_source(supabase, source)
            print(f"    ✅ Added successfully (ID: {inserted['id'][:8]}...)\n")
            added += 1

        except Exception as e:
            print(f"    ❌ Failed: {str(e)}\n")
            failed += 1

    # Print summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total sources:     {len(sources)}")
    print(f"Added:            {added}")
    print(f"Already existed:  {existed}")
    print(f"Failed:           {failed}")

    if failed > 0:
        print(f"\n⚠️  Some sources failed. Check errors above.")
        sys.exit(1)
    elif added > 0:
        print(f"\n🎉 All sources configured!")
    else:
        print(f"\n✅ All sources already configured!")

    print("\nNext steps:")
    print("  1. Run: python3 scripts/ingest_agent.py --dry-run")
    print("  2. Verify output looks correct")
    print("  3. Run: python3 scripts/ingest_agent.py")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
