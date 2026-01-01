#!/usr/bin/env python3
"""
Add new sources to the sources table
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client


# New sources to add
NEW_SOURCES = [
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/news",
        "domain": "openai.com",
        "source_type": "rss",
        "rss_feed_url": "https://openai.com/news/rss.xml",
        "is_active": True,
        "fetch_frequency": "weekly"
    },
    {
        "name": "Matt Rickard",
        "url": "https://matt-rickard.com",
        "domain": "matt-rickard.com",
        "source_type": "rss",
        "rss_feed_url": "https://matt-rickard.com/rss",
        "is_active": True,
        "fetch_frequency": "daily"  # Matt posts daily
    },
    {
        "name": "Interconnects (Nathan Lambert)",
        "url": "https://www.interconnects.ai",
        "domain": "interconnects.ai",
        "source_type": "rss",
        "rss_feed_url": "https://www.interconnects.ai/feed",
        "is_active": True,
        "fetch_frequency": "weekly"
    },
    {
        "name": "The Batch (DeepLearning.AI)",
        "url": "https://www.deeplearning.ai/the-batch/",
        "domain": "deeplearning.ai",
        "source_type": "rss",
        "rss_feed_url": "https://rsshub.app/deeplearning/the-batch",
        "is_active": True,
        "fetch_frequency": "weekly"
    },
    {
        "name": "Google DeepMind Blog",
        "url": "https://deepmind.google/discover/blog/",
        "domain": "deepmind.google",
        "source_type": "rss",
        "rss_feed_url": "https://deepmind.google/blog/rss.xml",
        "is_active": True,
        "fetch_frequency": "weekly"
    },
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/news",
        "domain": "anthropic.com",
        "source_type": "rss",
        "rss_feed_url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feed_anthropic_news.xml",
        "is_active": True,
        "fetch_frequency": "weekly"
    },
    {
        "name": "Sebastian Ruder",
        "url": "https://ruder.io",
        "domain": "ruder.io",
        "source_type": "rss",
        "rss_feed_url": "http://ruder.io/rss/",
        "is_active": True,
        "fetch_frequency": "monthly"
    },
    {
        "name": "Nelson Elhage (Made of Bugs)",
        "url": "https://blog.nelhage.com",
        "domain": "nelhage.com",
        "source_type": "rss",
        "rss_feed_url": "https://blog.nelhage.com/feed/",
        "is_active": True,
        "fetch_frequency": "monthly"
    },
    {
        "name": "Aleksa Gordić",
        "url": "https://www.aleksagordic.com/blog",
        "domain": "aleksagordic.com",
        "source_type": "rss",
        "rss_feed_url": "https://www.aleksagordic.com/blog/feed",
        "is_active": True,
        "fetch_frequency": "monthly"
    }
]


def source_exists(supabase, url: str) -> bool:
    """Check if source already exists by URL"""
    result = supabase.table('sources').select('id').eq('url', url).execute()
    return len(result.data) > 0


def main():
    """Add new sources to database"""
    print("Adding new sources to database...")
    print()

    supabase = get_supabase_client()

    added = 0
    skipped = 0

    for source in NEW_SOURCES:
        name = source['name']
        url = source['url']

        if source_exists(supabase, url):
            print(f"⚠️  SKIP: {name} (already exists)")
            skipped += 1
        else:
            try:
                supabase.table('sources').insert(source).execute()
                print(f"✅ ADDED: {name}")
                print(f"   Feed: {source['rss_feed_url']}")
                added += 1
            except Exception as e:
                print(f"❌ ERROR: {name} - {str(e)}")
        print()

    print("=" * 60)
    print(f"Summary: {added} added, {skipped} skipped")
    print("=" * 60)


if __name__ == "__main__":
    main()
