#!/usr/bin/env python3
"""
Migration Runner Script

This script applies database migrations to Supabase.

Usage:
    python scripts/run_migration.py 004

Requirements:
    - psycopg2-binary (install: pip install psycopg2-binary)
    - SUPABASE_DB_PASSWORD environment variable

Connection String Format:
    postgresql://postgres.PROJECT_REF:PASSWORD@aws-0-us-west-1.pooler.supabase.com:6543/postgres
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection_string():
    """Construct PostgreSQL connection string from Supabase credentials."""
    url = os.getenv('SUPABASE_URL')
    password = os.getenv('SUPABASE_DB_PASSWORD')

    if not url:
        print("Error: SUPABASE_URL not found in environment")
        return None

    if not password:
        print("Error: SUPABASE_DB_PASSWORD not found in environment")
        print("\nTo get your database password:")
        print("1. Go to https://app.supabase.com/project/_/settings/database")
        print("2. Find 'Database password' section")
        print("3. Add to .env file: SUPABASE_DB_PASSWORD=your_password")
        return None

    # Parse project ref from URL
    match = re.search(r'https://([^.]+)\.supabase\.co', url)
    if not match:
        print(f"Error: Could not parse project ref from URL: {url}")
        return None

    project_ref = match.group(1)

    # Construct connection string
    conn_str = f"postgresql://postgres.{project_ref}:{password}@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    return conn_str

def run_migration(migration_number):
    """Run a specific migration file."""
    # Find migration file
    migration_file = Path(f"migrations/{migration_number:03d}_*.sql")
    migration_files = list(Path("migrations").glob(f"{migration_number:03d}_*.sql"))

    if not migration_files:
        print(f"Error: No migration file found matching pattern: {migration_number:03d}_*.sql")
        return False

    if len(migration_files) > 1:
        print(f"Error: Multiple migration files found: {migration_files}")
        return False

    migration_file = migration_files[0]
    print(f"Found migration: {migration_file}")

    # Read migration SQL
    with open(migration_file, 'r') as f:
        sql = f.read()

    # Get connection string
    conn_str = get_connection_string()
    if not conn_str:
        print("\n" + "="*60)
        print("ALTERNATIVE: Run migration manually in Supabase SQL Editor")
        print("="*60)
        print(f"\n1. Go to: https://app.supabase.com/project/_/sql")
        print(f"2. Copy and paste the SQL from: {migration_file}")
        print("3. Click 'Run' to execute")
        print("\nOr add SUPABASE_DB_PASSWORD to .env and run this script again")
        return False

    # Import psycopg2
    try:
        import psycopg2
    except ImportError:
        print("Error: psycopg2-binary not installed")
        print("Install with: pip install psycopg2-binary")
        return False

    # Execute migration
    try:
        print(f"\nConnecting to database...")
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()

        print(f"Executing migration {migration_number:03d}...")
        cursor.execute(sql)
        conn.commit()

        print(f"✓ Migration {migration_number:03d} completed successfully!")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"✗ Error executing migration: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_migration.py <migration_number>")
        print("Example: python scripts/run_migration.py 004")
        sys.exit(1)

    try:
        migration_number = int(sys.argv[1])
    except ValueError:
        print(f"Error: Migration number must be an integer, got: {sys.argv[1]}")
        sys.exit(1)

    success = run_migration(migration_number)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
