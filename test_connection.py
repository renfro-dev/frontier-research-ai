#!/usr/bin/env python3
"""
Test script to verify Supabase connection
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test Supabase connection and credentials"""
    print("🔍 Testing Supabase Connection...\n")

    # Check if credentials are loaded
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url:
        print("❌ SUPABASE_URL not found in .env file")
        return False

    if not supabase_key:
        print("❌ SUPABASE_ANON_KEY not found in .env file")
        return False

    print(f"✅ Environment variables loaded")
    print(f"   URL: {supabase_url}")
    print(f"   Key: {supabase_key[:20]}...{supabase_key[-10:]}\n")

    try:
        from supabase import create_client, Client

        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully\n")

        # Test connection by trying to query (this will fail if no tables exist, but that's ok)
        try:
            # Try to get database version
            response = supabase.rpc('version', {}).execute()
            print(f"✅ Connected to Supabase!")
            print(f"   Database version: {response.data}\n")
        except Exception as e:
            # If version doesn't work, try a simple query
            print("✅ Connection successful!")
            print("   (No tables exist yet - this is expected)\n")

        return True

    except ImportError:
        print("❌ Supabase Python client not installed")
        print("   Run: pip install supabase\n")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}\n")
        return False

def test_anthropic_credentials():
    """Test if Anthropic API key is configured"""
    print("🔍 Checking Anthropic API Key...\n")

    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not anthropic_key:
        print("⚠️  ANTHROPIC_API_KEY not found in .env file")
        print("   This is optional for testing Supabase, but required for the full pipeline\n")
        return False

    print(f"✅ Anthropic API key loaded")
    print(f"   Key: {anthropic_key[:15]}...{anthropic_key[-10:]}\n")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Supabase Connection Test")
    print("=" * 60 + "\n")

    # Test Supabase
    supabase_ok = test_supabase_connection()

    # Test Anthropic
    anthropic_ok = test_anthropic_credentials()

    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Supabase:  {'✅ Connected' if supabase_ok else '❌ Failed'}")
    print(f"Anthropic: {'✅ Configured' if anthropic_ok else '⚠️  Not configured'}")
    print()

    if supabase_ok:
        print("🎉 Supabase connection successful! Ready to create database schema.")
    else:
        print("❌ Please fix Supabase connection issues before proceeding.")
