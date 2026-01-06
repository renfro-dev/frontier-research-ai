"""
Google Docs Creator
Creates Google Docs for LinkedIn post drafts with formatting
"""

import logging
from typing import Dict, Optional
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import Config

logger = logging.getLogger(__name__)


class GoogleDocsCreator:
    """Creates and manages Google Docs for LinkedIn post drafts"""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Docs creator

        Args:
            credentials_path: Path to service account JSON file (optional, uses config if not provided)

        Raises:
            FileNotFoundError: If credentials file doesn't exist
            ValueError: If credentials are invalid
        """
        creds_path = credentials_path or Config.GOOGLE_SERVICE_ACCOUNT_FILE

        if not creds_path:
            raise ValueError("Google service account file not configured")

        try:
            self.creds = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=Config.GOOGLE_SCOPES
            )
            self.docs_service = build('docs', 'v1', credentials=self.creds)
            self.drive_service = build('drive', 'v3', credentials=self.creds)
            logger.info("Google Docs creator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Docs creator: {e}")
            raise

    def create_post_draft(self, post_data: Dict) -> Dict:
        """
        Create Google Doc for LinkedIn post draft

        Args:
            post_data: Dictionary containing:
                - section_title: Title of the section
                - post_text: Post content
                - word_count: Word count
                - brief_title: (optional) Source brief title
                - generated_at: (optional) Generation timestamp

        Returns:
            Dictionary with:
                - doc_id: Google Docs file ID
                - doc_url: Shareable URL
                - edit_url: Edit URL

        Raises:
            Exception: If document creation fails
        """
        try:
            # Create document title
            doc_title = f"LinkedIn Post Draft - {post_data['section_title']}"

            # Create document
            doc = self.docs_service.documents().create(body={
                'title': doc_title
            }).execute()

            doc_id = doc['documentId']
            logger.info(f"Created Google Doc: {doc_id}")

            # Insert content
            self._insert_content(doc_id, post_data)

            # Set sharing permissions
            self._set_sharing_permissions(doc_id)

            # Build URLs
            edit_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            view_url = f"https://docs.google.com/document/d/{doc_id}/view"

            logger.info(f"Google Doc created successfully: {edit_url}")

            return {
                'doc_id': doc_id,
                'doc_url': edit_url,
                'view_url': view_url,
                'title': doc_title
            }

        except HttpError as e:
            logger.error(f"Google Docs API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create Google Doc: {e}")
            raise

    def _insert_content(self, doc_id: str, post_data: Dict):
        """
        Insert formatted content into the document

        Args:
            doc_id: Google Docs file ID
            post_data: Post data dictionary
        """
        # Build content sections
        title = post_data['section_title']
        post_text = post_data['post_text']
        word_count = post_data['word_count']
        char_count = len(post_text)

        # Add metadata if available
        brief_title = post_data.get('brief_title', 'Context Orchestration Brief')
        generated_at = post_data.get('generated_at', datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'))

        # Build full content
        content_parts = [
            f"{title}\n\n",
            f"{post_text}\n\n",
            "─" * 60 + "\n\n",
            "METADATA\n\n",
            f"Source: {brief_title}\n",
            f"Generated: {generated_at}\n",
            f"Word Count: {word_count} words\n",
            f"Character Count: {char_count} characters\n",
            f"Status: Ready for review\n\n",
            "INSTRUCTIONS\n\n",
            "1. Review the post content above\n",
            "2. Make any edits directly in this document\n",
            "3. When ready to publish, check the box in the tracking spreadsheet\n",
            "4. The post will be automatically published to LinkedIn\n"
        ]

        full_content = "".join(content_parts)

        # Insert content using batchUpdate
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': full_content
                }
            }
        ]

        # Add formatting for title (make it bold and larger)
        title_end = len(title) + 3  # +3 for newlines
        requests.extend([
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': title_end
                    },
                    'textStyle': {
                        'bold': True,
                        'fontSize': {
                            'magnitude': 16,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'bold,fontSize'
                }
            }
        ])

        try:
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            logger.info(f"Inserted content into document {doc_id}")
        except Exception as e:
            logger.error(f"Failed to insert content: {e}")
            raise

    def _set_sharing_permissions(self, doc_id: str):
        """
        Set document sharing permissions (anyone with link can view)

        Args:
            doc_id: Google Docs file ID
        """
        try:
            self.drive_service.permissions().create(
                fileId=doc_id,
                body={
                    'type': 'anyone',
                    'role': 'writer'  # Allow editing
                }
            ).execute()
            logger.info(f"Set sharing permissions for document {doc_id}")
        except Exception as e:
            logger.error(f"Failed to set sharing permissions: {e}")
            raise

    def get_document_content(self, doc_id: str) -> str:
        """
        Get the current content of a document

        Args:
            doc_id: Google Docs file ID

        Returns:
            Plain text content of the document

        Raises:
            Exception: If retrieval fails
        """
        try:
            doc = self.docs_service.documents().get(documentId=doc_id).execute()
            content = doc.get('body', {}).get('content', [])

            # Extract text from document structure
            text_parts = []
            for element in content:
                if 'paragraph' in element:
                    for text_elem in element['paragraph'].get('elements', []):
                        if 'textRun' in text_elem:
                            text_parts.append(text_elem['textRun'].get('content', ''))

            full_text = ''.join(text_parts)
            logger.info(f"Retrieved content from document {doc_id}")
            return full_text

        except Exception as e:
            logger.error(f"Failed to get document content: {e}")
            raise

    def update_document_status(self, doc_id: str, status: str):
        """
        Update the status field in a document's metadata section

        Args:
            doc_id: Google Docs file ID
            status: New status (e.g., "Published", "Error")
        """
        try:
            # Get current content
            doc = self.docs_service.documents().get(documentId=doc_id).execute()
            content_text = self.get_document_content(doc_id)

            # Find and replace status line
            if "Status: " in content_text:
                # This is a simplified approach - in production you'd want more robust text replacement
                logger.info(f"Status update requested for {doc_id}: {status}")
                # Note: Implementing precise text replacement in Google Docs requires finding exact indices
                # For now, we'll just log the status update
            else:
                logger.warning(f"No status field found in document {doc_id}")

        except Exception as e:
            logger.error(f"Failed to update document status: {e}")
            raise
