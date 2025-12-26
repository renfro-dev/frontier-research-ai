#!/usr/bin/env python3
"""
Run database migrations using direct PostgreSQL connection
Requires: psycopg2 (install with: pip install psycopg2-binary)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection_string():
    """Build PostgreSQL connection string from Supabase credentials"""
    supabase_url = os.getenv("SUPABASE_URL")

    if not supabase_url:
        raise ValueError("SUPABASE_URL must be set in .env")

    # Extract project ref from Supabase URL
    # Format: https://xxxxx.supabase.co
    project_ref = supabase_url.replace("https://", "").replace(".supabase.co", "")

    # Get password from user (Supabase doesn't store this in env vars)
    print(f"\nYour Supabase project: {project_ref}")
    print("Enter your Supabase database password")
    print("(This was set when you created the project)")

    password = input("Password: ").strip()

    if not password:
        raise ValueError("Password cannot be empty")

    # Build connection string
    conn_str = f"postgresql://postgres:{password}@db.{project_ref}.supabase.co:5432/postgres"

    return conn_str

def run_migrations():
    """Run all migration files in order"""
    try:
        import psycopg2
    except ImportError:
        print("❌ psycopg2 not installed")
        print("   Install with: pip install psycopg2-binary")
        sys.exit(1)

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

    # Get connection string
    try:
        conn_str = get_connection_string()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

    # Connect to database
    print(f"\n🔌 Connecting to database...")
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = False  # Use transactions
        cursor = conn.cursor()
        print(f"✅ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        sys.exit(1)

    # Run each migration
    success_count = 0
    for mf in migration_files:
        print(f"\n{'='*60}")
        print(f"Running: {mf.name}")
        print(f"{'='*60}")

        try:
            # Read SQL file
            with open(mf, 'r') as f:
                sql_content = f.read()

            # Execute SQL
            cursor.execute(sql_content)
            conn.commit()

            print(f"✅ Migration successful")
            success_count += 1

        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            conn.rollback()
            print(f"\nRolling back. Fix the error and try again.")
            cursor.close()
            conn.close()
            sys.exit(1)

    # Close connection
    cursor.close()
    conn.close()

    # Summary
    print(f"\n{'='*60}")
    print(f"Migration Summary")
    print(f"{'='*60}")
    print(f"✅ Successfully ran {success_count}/{len(migration_files)} migrations")
    print(f"\nNext step: Run verification script")
    print(f"  python3 verify_schema.py")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_migrations()
