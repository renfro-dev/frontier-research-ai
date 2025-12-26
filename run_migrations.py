#!/usr/bin/env python3
"""
Run database migrations for Weekly Systems Thinking Brief
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Create and return Supabase client"""
    supabase_url = os.getenv("SUPABASE_URL")
    # Use service role key for migrations (has admin privileges)
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")

    return create_client(supabase_url, supabase_key)

def run_migration_file(supabase: Client, file_path: Path) -> bool:
    """
    Run a single migration SQL file

    Args:
        supabase: Supabase client
        file_path: Path to SQL file

    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Running: {file_path.name}")
    print(f"{'='*60}")

    try:
        # Read SQL file
        with open(file_path, 'r') as f:
            sql_content = f.read()

        # Execute SQL using Supabase's RPC
        # Note: Supabase Python client doesn't have direct SQL execution
        # We'll use the PostgREST API with the service role key
        import httpx

        url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        # Use direct PostgreSQL connection for migrations
        # Split by semicolons and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]

        # For Supabase, we need to use their REST API or direct postgres connection
        # Using httpx to call the Supabase SQL API
        headers = {
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json"
        }

        print(f"✓ Loaded SQL file ({len(statements)} statements)")
        print(f"\nNote: Supabase Python client requires using SQL Editor in dashboard")
        print(f"      or direct PostgreSQL connection for complex migrations.")
        print(f"\nTo run this migration:")
        print(f"1. Go to: {url.replace('https://', 'https://app.')}/project/_/sql")
        print(f"2. Copy and paste the contents of: {file_path}")
        print(f"3. Click 'Run' button")
        print(f"\nOR use psql CLI:")
        print(f"   psql <your-connection-string> -f {file_path}")

        return True

    except Exception as e:
        print(f"❌ Error running migration: {str(e)}")
        return False

def main():
    """Main migration runner"""
    print("=" * 60)
    print("Weekly Systems Thinking Brief - Database Migrations")
    print("=" * 60)

    # Get migrations directory
    migrations_dir = Path(__file__).parent / "migrations"

    if not migrations_dir.exists():
        print(f"❌ Migrations directory not found: {migrations_dir}")
        sys.exit(1)

    # Get all SQL files in order
    migration_files = sorted(migrations_dir.glob("*.sql"))

    if not migration_files:
        print("❌ No migration files found")
        sys.exit(1)

    print(f"\nFound {len(migration_files)} migration(s):")
    for mf in migration_files:
        print(f"  - {mf.name}")

    # Get Supabase client
    try:
        supabase = get_supabase_client()
        print(f"\n✅ Connected to Supabase")
    except Exception as e:
        print(f"\n❌ Failed to connect to Supabase: {str(e)}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"IMPORTANT: Supabase Migration Instructions")
    print(f"{'='*60}")
    print(f"\nThe Supabase Python client doesn't support direct SQL execution.")
    print(f"You have two options to run these migrations:\n")

    print(f"Option 1 - Supabase SQL Editor (Recommended):")
    print(f"  1. Go to: {os.getenv('SUPABASE_URL').replace('https://', 'https://app.')}/project/_/sql/new")
    print(f"  2. Run each migration file in order:\n")

    for i, mf in enumerate(migration_files, 1):
        print(f"     {i}. {mf.name}")

    print(f"\n  3. For each file:")
    print(f"     - Open it in your editor")
    print(f"     - Copy the entire contents")
    print(f"     - Paste into Supabase SQL Editor")
    print(f"     - Click 'Run'")
    print(f"     - Verify success message\n")

    print(f"Option 2 - Use helper script (coming next):")
    print(f"  We'll create a script that uses psycopg2 for direct PostgreSQL access")

    print(f"\n{'='*60}")
    print(f"After running migrations manually, run:")
    print(f"  python3 verify_schema.py")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
