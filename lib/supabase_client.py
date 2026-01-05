"""
Shared Supabase client utility
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client(use_service_role: bool = True) -> Client:
    """
    Create and return Supabase client

    Args:
        use_service_role: If True, use service role key (for writes)
                         If False, use anon key (for reads only)

    Returns:
        Supabase client

    Raises:
        ValueError: If credentials not found in environment
    """
    supabase_url = os.getenv("SUPABASE_URL")

    if use_service_role:
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not supabase_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY not found in .env")
    else:
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        if not supabase_key:
            raise ValueError("SUPABASE_ANON_KEY not found in .env")

    if not supabase_url:
        raise ValueError("SUPABASE_URL not found in .env")

    return create_client(supabase_url, supabase_key)
