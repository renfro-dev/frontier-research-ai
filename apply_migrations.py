#!/usr/bin/env python3
"""
Apply migrations by displaying them for you to copy/paste into Supabase SQL Editor
"""

from pathlib import Path
import sys

def main():
    """Display migrations for manual application"""
    print("=" * 70)
    print("Database Migration Application")
    print("=" * 70)

    migrations_dir = Path(__file__).parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        print("❌ No migration files found")
        sys.exit(1)

    print(f"\nFound {len(migration_files)} migration files to apply")
    print("\nInstructions:")
    print("1. Open your Supabase SQL Editor:")
    print("   https://app.supabase.com (go to your project → SQL Editor)")
    print("2. For each migration below, copy the ENTIRE content")
    print("3. Paste into SQL Editor and click 'Run'")
    print("4. Verify success message before moving to next migration\n")

    for i, mf in enumerate(migration_files, 1):
        print("=" * 70)
        print(f"MIGRATION {i}/{len(migration_files)}: {mf.name}")
        print("=" * 70)

        with open(mf, 'r') as f:
            content = f.read()

        print(f"\nFile path: {mf}")
        print(f"Lines: {len(content.splitlines())}")
        print(f"Size: {len(content)} characters")

        print(f"\n{'-' * 70}")
        print("COPY THE CONTENT BELOW (including all lines):")
        print(f"{'-' * 70}\n")
        print(content)
        print(f"\n{'-' * 70}")
        print("END OF MIGRATION CONTENT")
        print(f"{'-' * 70}\n")

        if i < len(migration_files):
            input(f"Press Enter after you've successfully run migration {i}...")
            print()

    print("=" * 70)
    print("All migrations displayed!")
    print("=" * 70)
    print("\nAfter running all migrations in Supabase, verify with:")
    print("  python3 verify_schema.py")
    print()

if __name__ == "__main__":
    main()
