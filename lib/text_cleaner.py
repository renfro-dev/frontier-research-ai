"""
Text cleaning utilities for extracting plain text from HTML
"""

from bs4 import BeautifulSoup
import re
from typing import Dict, Any

def clean_html(html_content: str) -> str:
    """
    Extract clean plain text from HTML content

    Args:
        html_content: Raw HTML string

    Returns:
        Cleaned plain text

    Removes:
        - HTML tags
        - Scripts and styles
        - Excessive whitespace
        - Navigation, ads, comments
    """
    # Parse HTML
    soup = BeautifulSoup(html_content, 'lxml')

    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'footer', 'header',
                         'iframe', 'noscript', 'aside']):
        element.decompose()

    # Remove comments
    for comment in soup.find_all(text=lambda text: isinstance(text, str) and text.startswith('<!--')):
        comment.extract()

    # Get text
    text = soup.get_text()

    # Clean up whitespace
    text = _normalize_whitespace(text)

    return text

def _normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)

    # Replace multiple newlines with double newline
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove empty lines at start and end
    text = text.strip()

    return text

def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Calculate estimated reading time in minutes

    Args:
        text: Text content
        words_per_minute: Average reading speed (default: 200 wpm)

    Returns:
        Reading time in minutes (minimum 1)
    """
    word_count = len(text.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes

def calculate_word_count(text: str) -> int:
    """
    Calculate word count

    Args:
        text: Text content

    Returns:
        Number of words
    """
    return len(text.split())

def extract_metadata(html_content: str) -> Dict[str, Any]:
    """
    Extract metadata from HTML (title, description, etc.)

    Args:
        html_content: Raw HTML string

    Returns:
        Dictionary of metadata
    """
    soup = BeautifulSoup(html_content, 'lxml')
    metadata = {}

    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        metadata['html_title'] = title_tag.get_text().strip()

    # Extract meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        metadata['meta_description'] = meta_desc['content'].strip()

    # Extract meta keywords
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords and meta_keywords.get('content'):
        metadata['meta_keywords'] = meta_keywords['content'].strip()

    # Extract Open Graph data
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title and og_title.get('content'):
        metadata['og_title'] = og_title['content'].strip()

    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc and og_desc.get('content'):
        metadata['og_description'] = og_desc['content'].strip()

    return metadata
