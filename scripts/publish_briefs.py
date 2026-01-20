#!/usr/bin/env python3
"""
Publish existing briefs to make them visible on the website
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client

def publish_briefs():
    """Publish briefs with the given date ranges"""

    supabase = get_supabase_client()

    print("=" * 60)
    print("Publishing Briefs")
    print("=" * 60)
    print()

    # Dates to publish
    dates_to_publish = ['2026-01-12', '2026-01-05']
    now = datetime.now().isoformat()

    # Publish weekly_briefs
    print("📝 Publishing weekly briefs (Systems Thinking)...")
    for date in dates_to_publish:
        result = supabase.table('weekly_briefs').update({
            'status': 'published',
            'published_at': now
        }).eq('week_start_date', date).execute()

        if result.data:
            print(f"  ✅ Published brief for {date}")
            for brief in result.data:
                print(f"     ID: {brief['id']}")
                print(f"     Title: {brief['title']}")
        else:
            print(f"  ⚠️  No brief found for {date}")

    print()

    # Publish context_orchestration_briefs
    print("📝 Publishing context orchestration briefs...")
    for date in dates_to_publish:
        result = supabase.table('context_orchestration_briefs').update({
            'published_at': now
        }).eq('period_start_date', date).execute()

        if result.data:
            print(f"  ✅ Published brief for {date}")
            for brief in result.data:
                print(f"     ID: {brief['id']}")
                print(f"     Title: {brief['title']}")
        else:
            print(f"  ⚠️  No brief found for {date}")

    print()
    print("=" * 60)
    print("✅ All briefs published successfully!")
    print("=" * 60)
    print()
    print("The briefs should now appear on the website.")

if __name__ == "__main__":
    publish_briefs()
