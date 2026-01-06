"""
Google Sheets Tracker
Creates and manages tracking spreadsheet for LinkedIn posts with checkboxes
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import Config

logger = logging.getLogger(__name__)


class GoogleSheetsTracker:
    """Creates and manages LinkedIn posts tracking spreadsheet"""

    SHEET_NAME = "LinkedIn Posts Tracker"
    POSTS_TAB_NAME = "Posts"

    # Column headers
    HEADERS = [
        "Google Doc Link",
        "Ready to Post",
        "Post Title",
        "Brief Source",
        "Generated Date",
        "Word Count",
        "Posted Date",
        "LinkedIn URL",
        "Status"
    ]

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Sheets tracker

        Args:
            credentials_path: Path to service account JSON file (optional)

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
            self.sheets_service = build('sheets', 'v4', credentials=self.creds)
            self.drive_service = build('drive', 'v3', credentials=self.creds)
            logger.info("Google Sheets tracker initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets tracker: {e}")
            raise

    def get_or_create_tracking_sheet(self) -> str:
        """
        Get existing tracking spreadsheet or create a new one

        Returns:
            Spreadsheet ID

        Raises:
            Exception: If creation/retrieval fails
        """
        # Check if sheet already exists in config
        if Config.GOOGLE_TRACKING_SHEET_ID:
            logger.info(f"Using existing tracking sheet: {Config.GOOGLE_TRACKING_SHEET_ID}")
            return Config.GOOGLE_TRACKING_SHEET_ID

        # Search for existing sheet
        try:
            results = self.drive_service.files().list(
                q=f"name='{self.SHEET_NAME}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
                spaces='drive',
                fields='files(id, name)'
            ).execute()

            files = results.get('files', [])

            if files:
                spreadsheet_id = files[0]['id']
                logger.info(f"Found existing tracking sheet: {spreadsheet_id}")
                return spreadsheet_id

        except Exception as e:
            logger.warning(f"Failed to search for existing sheet: {e}")

        # Create new spreadsheet
        return self._create_new_spreadsheet()

    def _create_new_spreadsheet(self) -> str:
        """
        Create a new tracking spreadsheet with formatting

        Returns:
            Spreadsheet ID
        """
        try:
            # Create spreadsheet
            spreadsheet = self.sheets_service.spreadsheets().create(body={
                'properties': {
                    'title': self.SHEET_NAME,
                    'locale': 'en_US',
                    'timeZone': 'UTC'
                },
                'sheets': [{
                    'properties': {
                        'title': self.POSTS_TAB_NAME,
                        'gridProperties': {
                            'frozenRowCount': 1,
                            'frozenColumnCount': 0
                        }
                    }
                }]
            }).execute()

            spreadsheet_id = spreadsheet['spreadsheetId']
            logger.info(f"Created new tracking spreadsheet: {spreadsheet_id}")

            # Set up formatting
            self._setup_sheet_formatting(spreadsheet_id)

            # Add header row
            self._add_header_row(spreadsheet_id)

            # Set sharing permissions
            self._set_sharing_permissions(spreadsheet_id)

            logger.info(f"Tracking sheet setup complete: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

            return spreadsheet_id

        except Exception as e:
            logger.error(f"Failed to create tracking spreadsheet: {e}")
            raise

    def _setup_sheet_formatting(self, spreadsheet_id: str):
        """
        Apply formatting to the tracking sheet

        Args:
            spreadsheet_id: Spreadsheet ID
        """
        requests = [
            # Set column widths
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': 0,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 1
                    },
                    'properties': {'pixelSize': 300},
                    'fields': 'pixelSize'
                }
            },
            # Column B (checkbox) - narrow
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': 0,
                        'dimension': 'COLUMNS',
                        'startIndex': 1,
                        'endIndex': 2
                    },
                    'properties': {'pixelSize': 100},
                    'fields': 'pixelSize'
                }
            },
            # Column C (Post Title) - wide
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': 0,
                        'dimension': 'COLUMNS',
                        'startIndex': 2,
                        'endIndex': 3
                    },
                    'properties': {'pixelSize': 250},
                    'fields': 'pixelSize'
                }
            },
            # Freeze header row
            {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': 0,
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            }
        ]

        try:
            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()
            logger.info(f"Applied formatting to spreadsheet {spreadsheet_id}")
        except Exception as e:
            logger.error(f"Failed to apply formatting: {e}")
            raise

    def _add_header_row(self, spreadsheet_id: str):
        """
        Add and format header row

        Args:
            spreadsheet_id: Spreadsheet ID
        """
        try:
            # Add headers
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f'{self.POSTS_TAB_NAME}!A1:I1',
                valueInputOption='RAW',
                body={'values': [self.HEADERS]}
            ).execute()

            # Format header row (bold, background color)
            requests = [
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                                'textFormat': {'bold': True},
                                'horizontalAlignment': 'CENTER'
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
                    }
                }
            ]

            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()

            logger.info(f"Added header row to spreadsheet {spreadsheet_id}")

        except Exception as e:
            logger.error(f"Failed to add header row: {e}")
            raise

    def _set_sharing_permissions(self, spreadsheet_id: str):
        """
        Set spreadsheet sharing permissions (anyone with link can edit)

        Args:
            spreadsheet_id: Spreadsheet ID
        """
        try:
            self.drive_service.permissions().create(
                fileId=spreadsheet_id,
                body={
                    'type': 'anyone',
                    'role': 'writer'  # Allow editing for checkbox
                }
            ).execute()
            logger.info(f"Set sharing permissions for spreadsheet {spreadsheet_id}")
        except Exception as e:
            logger.error(f"Failed to set sharing permissions: {e}")
            raise

    def add_post_row(self, spreadsheet_id: str, post_data: Dict) -> int:
        """
        Add new post to tracking sheet

        Args:
            spreadsheet_id: Spreadsheet ID
            post_data: Dictionary containing:
                - doc_url: Google Doc link
                - section_title: Post title
                - brief_title: Brief source
                - generated_at: Generation timestamp
                - word_count: Word count

        Returns:
            Row number where post was added

        Raises:
            Exception: If adding row fails
        """
        try:
            # Get current row count
            sheet_metadata = self.sheets_service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            sheets = sheet_metadata.get('sheets', [])
            current_rows = sheets[0]['properties']['gridProperties']['rowCount']

            # Prepare row data
            generated_date = post_data.get('generated_at', datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'))

            row_values = [
                post_data['doc_url'],  # A: Google Doc Link
                False,  # B: Ready to Post (checkbox, unchecked)
                post_data['section_title'],  # C: Post Title
                post_data.get('brief_title', 'Context Orchestration Brief'),  # D: Brief Source
                generated_date,  # E: Generated Date
                post_data['word_count'],  # F: Word Count
                '',  # G: Posted Date (empty initially)
                '',  # H: LinkedIn URL (empty initially)
                'Draft'  # I: Status
            ]

            # Append row
            range_name = f'{self.POSTS_TAB_NAME}!A{current_rows + 1}:I{current_rows + 1}'
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': [row_values]}
            ).execute()

            row_number = current_rows + 1
            logger.info(f"Added post to row {row_number} in spreadsheet {spreadsheet_id}")

            # Apply checkbox data validation to column B
            self._apply_checkbox_validation(spreadsheet_id, row_number)

            return row_number

        except Exception as e:
            logger.error(f"Failed to add post row: {e}")
            raise

    def _apply_checkbox_validation(self, spreadsheet_id: str, row_number: int):
        """
        Apply checkbox data validation to a specific row

        Args:
            spreadsheet_id: Spreadsheet ID
            row_number: Row number (1-indexed)
        """
        requests = [
            {
                'setDataValidation': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': row_number - 1,
                        'endRowIndex': row_number,
                        'startColumnIndex': 1,  # Column B (0-indexed)
                        'endColumnIndex': 2
                    },
                    'rule': {
                        'condition': {
                            'type': 'BOOLEAN'
                        },
                        'showCustomUi': True
                    }
                }
            }
        ]

        try:
            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()
            logger.info(f"Applied checkbox validation to row {row_number}")
        except Exception as e:
            logger.error(f"Failed to apply checkbox validation: {e}")
            # Don't raise - this is not critical

    def update_post_status(
        self,
        spreadsheet_id: str,
        row_number: int,
        status: str,
        posted_date: Optional[str] = None,
        linkedin_url: Optional[str] = None
    ):
        """
        Update post status in tracking sheet

        Args:
            spreadsheet_id: Spreadsheet ID
            row_number: Row number to update (1-indexed)
            status: New status
            posted_date: (optional) Date when posted
            linkedin_url: (optional) LinkedIn post URL
        """
        try:
            updates = []

            # Status column (I)
            updates.append({
                'range': f'{self.POSTS_TAB_NAME}!I{row_number}',
                'values': [[status]]
            })

            # Posted date column (G)
            if posted_date:
                updates.append({
                    'range': f'{self.POSTS_TAB_NAME}!G{row_number}',
                    'values': [[posted_date]]
                })

            # LinkedIn URL column (H)
            if linkedin_url:
                updates.append({
                    'range': f'{self.POSTS_TAB_NAME}!H{row_number}',
                    'values': [[linkedin_url]]
                })

            if updates:
                self.sheets_service.spreadsheets().values().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={'data': updates, 'valueInputOption': 'USER_ENTERED'}
                ).execute()
                logger.info(f"Updated row {row_number} in spreadsheet {spreadsheet_id}")

        except Exception as e:
            logger.error(f"Failed to update post status: {e}")
            raise

    def get_sheet_url(self, spreadsheet_id: str) -> str:
        """
        Get public URL for the tracking sheet

        Args:
            spreadsheet_id: Spreadsheet ID

        Returns:
            Public Google Sheets URL
        """
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
