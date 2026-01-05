"""
RSS/Atom feed parsing utilities
"""

import feedparser
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
import requests

@dataclass
class FeedEntry:
    """Parsed feed entry data"""
    title: str
    url: str
    author: Optional[str]
    published_at: Optional[datetime]
    content: str  # Full text content
    summary: str  # Short summary/excerpt
    raw_entry: Dict[str, Any]  # Original feedparser entry

def parse_feed(feed_url: str, timeout: int = 30) -> List[FeedEntry]:
    """
    Parse RSS/Atom feed and return structured entries

    Args:
        feed_url: URL of RSS/Atom feed
        timeout: Request timeout in seconds

    Returns:
        List of FeedEntry objects

    Raises:
        requests.exceptions.RequestException: Network errors
        ValueError: Malformed feed
    """
    # Fetch feed with timeout and User-Agent header
    headers = {
        'User-Agent': 'Weekly-Systems-Thinking-Brief/1.0 (Educational RSS reader; +https://github.com)'
    }
    response = requests.get(feed_url, headers=headers, timeout=timeout)
    response.raise_for_status()

    # Parse feed
    feed = feedparser.parse(response.content)

    if feed.bozo:  # feedparser error indicator
        if hasattr(feed, 'bozo_exception'):
            raise ValueError(f"Malformed feed: {feed.bozo_exception}")

    entries = []
    for entry in feed.entries:
        entries.append(_parse_entry(entry))

    return entries

def _parse_entry(entry: Dict[str, Any]) -> FeedEntry:
    """Parse single feed entry"""
    # Extract content (try multiple fields)
    content = ""
    if hasattr(entry, 'content') and entry.content:
        content = entry.content[0].value
    elif hasattr(entry, 'summary'):
        content = entry.summary
    elif hasattr(entry, 'description'):
        content = entry.description

    # Extract summary
    summary = ""
    if hasattr(entry, 'summary'):
        summary = entry.summary
    elif hasattr(entry, 'description'):
        summary = entry.description

    # Extract published date
    published_at = None
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            published_at = datetime(*entry.published_parsed[:6])
        except (TypeError, ValueError):
            pass
    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            published_at = datetime(*entry.updated_parsed[:6])
        except (TypeError, ValueError):
            pass

    # Extract author
    author = None
    if hasattr(entry, 'author'):
        author = entry.author
    elif hasattr(entry, 'authors') and entry.authors:
        author = entry.authors[0].get('name', None)

    return FeedEntry(
        title=entry.get('title', 'Untitled'),
        url=entry.get('link', ''),
        author=author,
        published_at=published_at,
        content=content,
        summary=summary,
        raw_entry=entry
    )
