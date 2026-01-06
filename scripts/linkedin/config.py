"""
Configuration management for LinkedIn automation system
Handles credential loading, validation, and path configurations
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for LinkedIn posting system"""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    BRIEFS_DIR = PROJECT_ROOT / 'briefs' / 'context_orchestration'
    LOGS_DIR = PROJECT_ROOT / 'logs'
    CREDENTIALS_DIR = PROJECT_ROOT / 'credentials'

    # Google Workspace
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
    GOOGLE_TRACKING_SHEET_ID = os.getenv('GOOGLE_TRACKING_SHEET_ID')  # Optional
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # LinkedIn API
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
    LINKEDIN_REFRESH_TOKEN = os.getenv('LINKEDIN_REFRESH_TOKEN')
    LINKEDIN_COMPANY_URN = os.getenv('LINKEDIN_COMPANY_URN')
    LINKEDIN_API_BASE_URL = 'https://api.linkedin.com/v2'

    # Webhook configuration
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 5000))
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '0.0.0.0')

    # Anthropic API (reuse existing)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Supabase (reuse existing)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    # Post generation settings
    POST_MIN_WORDS = 150
    POST_MAX_WORDS = 200
    POST_MAX_CHARS = 3000
    POSTS_PER_BRIEF = 2  # Can be 2-3

    # LinkedIn hashtags
    DEFAULT_HASHTAGS = [
        '#AI',
        '#ArtificialIntelligence',
        '#Leadership',
        '#ContextOrchestration',
        '#ExecutiveInsights'
    ]

    @classmethod
    def validate(cls, skip_optional: bool = False) -> bool:
        """
        Validate all required credentials are present

        Args:
            skip_optional: If True, skip validation of optional credentials (useful for testing)

        Returns:
            bool: True if all required credentials are present

        Raises:
            ValueError: If missing required environment variables
            FileNotFoundError: If required files don't exist
        """
        required = [
            'ANTHROPIC_API_KEY',
            'SUPABASE_URL',
            'SUPABASE_SERVICE_ROLE_KEY'
        ]

        if not skip_optional:
            required.extend([
                'GOOGLE_SERVICE_ACCOUNT_FILE',
                'LINKEDIN_CLIENT_ID',
                'LINKEDIN_CLIENT_SECRET',
                'LINKEDIN_ACCESS_TOKEN',
                'LINKEDIN_COMPANY_URN',
                'WEBHOOK_SECRET'
            ])

        missing = [key for key in required if not getattr(cls, key)]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please update your .env file with the required credentials."
            )

        # Validate Google service account file exists
        if not skip_optional and cls.GOOGLE_SERVICE_ACCOUNT_FILE:
            service_account_path = Path(cls.GOOGLE_SERVICE_ACCOUNT_FILE)
            if not service_account_path.exists():
                raise FileNotFoundError(
                    f"Google service account file not found: {cls.GOOGLE_SERVICE_ACCOUNT_FILE}\n"
                    f"Please ensure the file exists and the path is correct."
                )

        logger.info("Configuration validation successful")
        return True

    @classmethod
    def get_google_credentials_path(cls) -> Optional[Path]:
        """
        Get the path to Google service account credentials

        Returns:
            Path object if configured, None otherwise
        """
        if cls.GOOGLE_SERVICE_ACCOUNT_FILE:
            return Path(cls.GOOGLE_SERVICE_ACCOUNT_FILE)
        return None

    @classmethod
    def get_linkedin_config(cls) -> dict:
        """
        Get LinkedIn API configuration as a dictionary

        Returns:
            dict: LinkedIn configuration
        """
        return {
            'client_id': cls.LINKEDIN_CLIENT_ID,
            'client_secret': cls.LINKEDIN_CLIENT_SECRET,
            'access_token': cls.LINKEDIN_ACCESS_TOKEN,
            'refresh_token': cls.LINKEDIN_REFRESH_TOKEN,
            'company_urn': cls.LINKEDIN_COMPANY_URN,
            'base_url': cls.LINKEDIN_API_BASE_URL
        }

    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        cls.BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("Ensured all required directories exist")


# Validate configuration on import (with optional credentials)
try:
    Config.validate(skip_optional=True)  # Only validate core credentials
except (ValueError, FileNotFoundError) as e:
    logger.warning(f"Configuration validation warning: {e}")
    logger.warning("Some features may not work until all credentials are configured")
