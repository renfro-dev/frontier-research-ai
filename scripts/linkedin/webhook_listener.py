"""
Webhook Listener
Flask server that handles checkbox triggers from Google Sheets and publishes to LinkedIn
"""

import logging
import hmac
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from typing import Dict

from .config import Config
from .google_docs_creator import GoogleDocsCreator
from .google_sheets_tracker import GoogleSheetsTracker
from .linkedin_publisher import LinkedInPublisher
from .db_helper import LinkedInPostsDB

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize services
docs_creator = None
sheets_tracker = None
linkedin_publisher = None
db = None


def init_services():
    """Initialize all services (lazy loading)"""
    global docs_creator, sheets_tracker, linkedin_publisher, db

    if docs_creator is None:
        try:
            docs_creator = GoogleDocsCreator()
            sheets_tracker = GoogleSheetsTracker()
            linkedin_publisher = LinkedInPublisher()
            db = LinkedInPostsDB()
            logger.info("All services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify webhook signature for security

    Args:
        payload: Raw request payload
        signature: X-Webhook-Secret header value

    Returns:
        True if signature is valid
    """
    if not Config.WEBHOOK_SECRET:
        logger.warning("No webhook secret configured - skipping verification")
        return True

    if signature != Config.WEBHOOK_SECRET:
        logger.warning("Invalid webhook signature")
        return False

    return True


@app.route('/webhook/linkedin-post', methods=['POST'])
def handle_linkedin_post_webhook():
    """
    Handle webhook from Google Sheets when checkbox is checked

    Expected payload:
    {
        "doc_link": "https://docs.google.com/document/d/...",
        "title": "Post title",
        "brief_source": "Brief title",
        "generated_date": "2025-01-05 12:00 UTC",
        "word_count": 180,
        "row_number": 2,
        "spreadsheet_id": "..."
    }
    """
    try:
        # Initialize services
        init_services()

        # Verify signature
        signature = request.headers.get('X-Webhook-Secret', '')
        if not verify_webhook_signature(request.data, signature):
            logger.warning(f"Unauthorized webhook attempt from {request.remote_addr}")
            return jsonify({'error': 'Unauthorized'}), 401

        # Parse payload
        payload = request.get_json()
        if not payload:
            logger.error("No JSON payload received")
            return jsonify({'error': 'Invalid payload'}), 400

        logger.info(f"Received webhook for post: {payload.get('title', 'Unknown')}")

        # Extract required fields
        doc_link = payload.get('doc_link')
        row_number = payload.get('row_number')
        spreadsheet_id = payload.get('spreadsheet_id')
        post_title = payload.get('title', 'Unknown')

        if not all([doc_link, row_number, spreadsheet_id]):
            logger.error("Missing required fields in payload")
            return jsonify({'error': 'Missing required fields'}), 400

        # Extract document ID from link
        doc_id = extract_doc_id_from_url(doc_link)
        if not doc_id:
            logger.error(f"Could not extract document ID from: {doc_link}")
            return jsonify({'error': 'Invalid document link'}), 400

        # Update status to "Processing"
        sheets_tracker.update_post_status(
            spreadsheet_id=spreadsheet_id,
            row_number=row_number,
            status='Processing'
        )

        # Get post content from Google Doc
        logger.info(f"Fetching content from Google Doc: {doc_id}")
        doc_content = docs_creator.get_document_content(doc_id)

        # Extract just the post text (before the metadata section)
        post_text = extract_post_text_from_doc(doc_content)

        if not post_text:
            logger.error("No post text found in document")
            sheets_tracker.update_post_status(
                spreadsheet_id=spreadsheet_id,
                row_number=row_number,
                status='Error - No content'
            )
            return jsonify({'error': 'No post text found'}), 400

        logger.info(f"Extracted post text ({len(post_text)} chars)")

        # Publish to LinkedIn
        logger.info("Publishing to LinkedIn...")
        result = linkedin_publisher.create_post(post_text, add_hashtags=True)

        posted_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

        # Update Google Sheet with results
        sheets_tracker.update_post_status(
            spreadsheet_id=spreadsheet_id,
            row_number=row_number,
            status='Posted',
            posted_date=posted_date,
            linkedin_url=result['post_url']
        )

        # Update database if we can find the post record
        # (This requires looking up by doc_id or other identifier)
        try:
            # Find post in database by google_doc_id
            posts = db.get_posts_by_status('draft')
            matching_post = next(
                (p for p in posts if p.get('google_doc_id') == doc_id),
                None
            )

            if matching_post:
                db.update_post_status(
                    post_id=matching_post['id'],
                    status='posted',
                    linkedin_post_id=result['post_id'],
                    linkedin_post_url=result['post_url']
                )
                logger.info(f"Updated database record for post {matching_post['id']}")
        except Exception as e:
            logger.warning(f"Could not update database: {e}")
            # Don't fail the webhook if database update fails

        logger.info(f"Successfully published post to LinkedIn: {result['post_url']}")

        return jsonify({
            'success': True,
            'post_id': result['post_id'],
            'post_url': result['post_url'],
            'posted_at': posted_date
        }), 200

    except Exception as e:
        logger.error(f"Webhook processing failed: {e}", exc_info=True)

        # Update sheet with error status
        try:
            if 'spreadsheet_id' in locals() and 'row_number' in locals():
                sheets_tracker.update_post_status(
                    spreadsheet_id=spreadsheet_id,
                    row_number=row_number,
                    status=f'Error - {str(e)[:50]}'
                )
        except Exception as sheet_error:
            logger.error(f"Failed to update sheet with error: {sheet_error}")

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'LinkedIn Webhook Listener',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/test', methods=['POST'])
def test_webhook():
    """Test endpoint for debugging webhook payload"""
    payload = request.get_json()
    logger.info(f"Test webhook received: {payload}")
    return jsonify({
        'received': payload,
        'headers': dict(request.headers)
    }), 200


def extract_doc_id_from_url(url: str) -> str:
    """
    Extract document ID from Google Docs URL

    Args:
        url: Google Docs URL

    Returns:
        Document ID or empty string if extraction fails
    """
    # URL format: https://docs.google.com/document/d/{doc_id}/...
    try:
        if '/document/d/' in url:
            parts = url.split('/document/d/')[1]
            doc_id = parts.split('/')[0]
            return doc_id
        return ''
    except Exception as e:
        logger.error(f"Failed to extract doc ID from URL: {e}")
        return ''


def extract_post_text_from_doc(doc_content: str) -> str:
    """
    Extract post text from Google Doc content (before metadata section)

    Args:
        doc_content: Full document content

    Returns:
        Just the post text (excluding title and metadata)
    """
    # Split by the separator line
    if '─' * 60 in doc_content or '---' in doc_content:
        separator = '─' * 60 if '─' * 60 in doc_content else '---'
        parts = doc_content.split(separator)
        if len(parts) > 0:
            # Get content before separator
            content = parts[0].strip()

            # Remove title (first line)
            lines = content.split('\n')
            if len(lines) > 1:
                # Skip first line (title) and rejoin
                post_text = '\n'.join(lines[1:]).strip()
                return post_text

    # Fallback: try to find "METADATA" section
    if 'METADATA' in doc_content:
        post_text = doc_content.split('METADATA')[0].strip()
        # Remove title
        lines = post_text.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return post_text

    # Last resort: return everything
    logger.warning("Could not find content separator, returning full content")
    return doc_content.strip()


def run_webhook_server(host: str = None, port: int = None, debug: bool = False):
    """
    Run the webhook server

    Args:
        host: Host to bind to (default from config)
        port: Port to bind to (default from config)
        debug: Enable debug mode
    """
    host = host or Config.WEBHOOK_HOST
    port = port or Config.WEBHOOK_PORT

    logger.info(f"Starting webhook server on {host}:{port}")
    logger.info(f"Webhook endpoint: http://{host}:{port}/webhook/linkedin-post")
    logger.info(f"Health check: http://{host}:{port}/health")

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    # Validate configuration
    try:
        Config.validate()
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        logger.error("Please set up all required credentials before starting the webhook server")
        exit(1)

    # Run server
    run_webhook_server(debug=False)
