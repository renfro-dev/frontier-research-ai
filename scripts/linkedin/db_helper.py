"""
Database helper functions for LinkedIn posts tracking
Handles CRUD operations for the linkedin_posts table
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


class LinkedInPostsDB:
    """Database operations for LinkedIn posts"""

    def __init__(self):
        self.supabase = get_supabase_client(use_service_role=True)

    def create_post_record(self, post_data: Dict) -> str:
        """
        Create new LinkedIn post record

        Args:
            post_data: Dictionary containing post information
                - brief_id: UUID of source brief
                - section_title: Title of the section from the brief
                - post_text: Final LinkedIn post text
                - word_count: Word count of post
                - google_doc_id: (optional) Google Docs file ID
                - google_doc_url: (optional) Google Docs URL
                - sheets_row: (optional) Row number in tracking sheet
                - metadata: (optional) Additional metadata

        Returns:
            UUID of created post record

        Raises:
            Exception: If database operation fails
        """
        record = {
            'brief_id': post_data['brief_id'],
            'brief_section_title': post_data['section_title'],
            'post_text': post_data['post_text'],
            'word_count': post_data['word_count'],
            'character_count': len(post_data['post_text']),
            'status': 'draft'
        }

        # Add optional fields
        if 'google_doc_id' in post_data:
            record['google_doc_id'] = post_data['google_doc_id']
        if 'google_doc_url' in post_data:
            record['google_doc_url'] = post_data['google_doc_url']
        if 'sheets_row' in post_data:
            record['google_sheets_row'] = post_data['sheets_row']
        if 'metadata' in post_data:
            record['metadata'] = post_data['metadata']

        try:
            response = self.supabase.table('linkedin_posts').insert(record).execute()
            post_id = response.data[0]['id']
            logger.info(f"Created LinkedIn post record: {post_id}")
            return post_id
        except Exception as e:
            logger.error(f"Failed to create post record: {e}")
            raise

    def update_post_status(
        self,
        post_id: str,
        status: str,
        linkedin_post_id: Optional[str] = None,
        linkedin_post_url: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        """
        Update post status and related fields

        Args:
            post_id: UUID of the post to update
            status: New status ('draft', 'approved', 'posted', 'error')
            linkedin_post_id: (optional) LinkedIn post ID after publishing
            linkedin_post_url: (optional) Public URL of published post
            error_message: (optional) Error message if status is 'error'

        Raises:
            Exception: If database operation fails
        """
        update_data = {'status': status}

        # Set timestamp fields based on status
        if status == 'approved':
            update_data['approved_at'] = datetime.utcnow().isoformat()
        elif status == 'posted':
            update_data['published_at'] = datetime.utcnow().isoformat()
            if linkedin_post_id:
                update_data['linkedin_post_id'] = linkedin_post_id
            if linkedin_post_url:
                update_data['linkedin_post_url'] = linkedin_post_url
        elif status == 'error' and error_message:
            update_data['error_message'] = error_message

        try:
            self.supabase.table('linkedin_posts').update(update_data).eq('id', post_id).execute()
            logger.info(f"Updated post {post_id} status to {status}")
        except Exception as e:
            logger.error(f"Failed to update post status: {e}")
            raise

    def get_post_by_id(self, post_id: str) -> Optional[Dict]:
        """
        Get a post by its ID

        Args:
            post_id: UUID of the post

        Returns:
            Dictionary with post data, or None if not found
        """
        try:
            response = self.supabase.table('linkedin_posts').select('*').eq('id', post_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to get post by ID: {e}")
            raise

    def get_posts_by_brief(self, brief_id: str) -> List[Dict]:
        """
        Get all LinkedIn posts for a specific brief

        Args:
            brief_id: UUID of the source brief

        Returns:
            List of post dictionaries, ordered by generation date
        """
        try:
            response = self.supabase.table('linkedin_posts').select('*').eq(
                'brief_id', brief_id
            ).order('generated_at').execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Failed to get posts by brief: {e}")
            raise

    def get_posts_by_status(self, status: str) -> List[Dict]:
        """
        Get all posts with a specific status

        Args:
            status: Status to filter by ('draft', 'approved', 'posted', 'error')

        Returns:
            List of post dictionaries, ordered by generation date (newest first)
        """
        try:
            response = self.supabase.table('linkedin_posts').select('*').eq(
                'status', status
            ).order('generated_at', desc=True).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Failed to get posts by status: {e}")
            raise

    def get_pending_posts(self) -> List[Dict]:
        """
        Get all draft posts awaiting approval

        Returns:
            List of draft post dictionaries, ordered by generation date (newest first)
        """
        return self.get_posts_by_status('draft')

    def check_post_exists(self, brief_id: str, section_title: str) -> bool:
        """
        Check if a post already exists for a brief section

        Args:
            brief_id: UUID of the source brief
            section_title: Title of the section

        Returns:
            True if post exists, False otherwise
        """
        try:
            response = self.supabase.table('linkedin_posts').select('id').eq(
                'brief_id', brief_id
            ).eq('brief_section_title', section_title).execute()
            return bool(response.data)
        except Exception as e:
            logger.error(f"Failed to check post existence: {e}")
            raise

    def get_brief_by_id(self, brief_id: str) -> Optional[Dict]:
        """
        Get a Context Orchestration brief by ID

        Args:
            brief_id: UUID of the brief

        Returns:
            Dictionary with brief data, or None if not found
        """
        try:
            response = self.supabase.table('context_orchestration_briefs').select('*').eq(
                'id', brief_id
            ).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to get brief by ID: {e}")
            raise

    def get_latest_brief(self) -> Optional[Dict]:
        """
        Get the most recently created Context Orchestration brief

        Returns:
            Dictionary with brief data, or None if no briefs exist
        """
        try:
            response = self.supabase.table('context_orchestration_briefs').select('*').order(
                'created_at', desc=True
            ).limit(1).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to get latest brief: {e}")
            raise

    def update_google_doc_info(self, post_id: str, doc_id: str, doc_url: str):
        """
        Update Google Doc information for a post

        Args:
            post_id: UUID of the post
            doc_id: Google Docs file ID
            doc_url: Google Docs URL
        """
        update_data = {
            'google_doc_id': doc_id,
            'google_doc_url': doc_url
        }
        try:
            self.supabase.table('linkedin_posts').update(update_data).eq('id', post_id).execute()
            logger.info(f"Updated Google Doc info for post {post_id}")
        except Exception as e:
            logger.error(f"Failed to update Google Doc info: {e}")
            raise

    def update_sheets_row(self, post_id: str, row_number: int):
        """
        Update Google Sheets row number for a post

        Args:
            post_id: UUID of the post
            row_number: Row number in tracking spreadsheet
        """
        try:
            self.supabase.table('linkedin_posts').update({
                'google_sheets_row': row_number
            }).eq('id', post_id).execute()
            logger.info(f"Updated sheets row for post {post_id}: row {row_number}")
        except Exception as e:
            logger.error(f"Failed to update sheets row: {e}")
            raise
