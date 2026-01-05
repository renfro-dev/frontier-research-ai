"""
Text segmentation utilities for breaking content into logical sections
"""

import re
from typing import List, Dict, Any

def segment_text(text: str, min_section_length: int = 100) -> List[Dict[str, Any]]:
    """
    Segment text into logical sections

    Args:
        text: Clean text content
        min_section_length: Minimum characters for a section (default: 100)

    Returns:
        List of section dictionaries with 'heading' and 'content'

    Strategy:
        - Detect headings (lines ending with colon, all caps, etc.)
        - Split on double newlines for paragraphs
        - Group paragraphs into logical sections
    """
    sections = []

    # Split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    if not paragraphs:
        return [{'heading': None, 'content': text}]

    current_section = {'heading': None, 'content': []}

    for para in paragraphs:
        # Check if this looks like a heading
        if _is_heading(para):
            # Save previous section if it has content
            if current_section['content']:
                sections.append({
                    'heading': current_section['heading'],
                    'content': '\n\n'.join(current_section['content'])
                })

            # Start new section
            current_section = {'heading': para, 'content': []}
        else:
            # Add to current section
            current_section['content'].append(para)

    # Add final section
    if current_section['content']:
        sections.append({
            'heading': current_section['heading'],
            'content': '\n\n'.join(current_section['content'])
        })

    # If no sections detected, return whole text as one section
    if not sections:
        return [{'heading': None, 'content': text}]

    # Filter out sections that are too short
    sections = [s for s in sections if len(s['content']) >= min_section_length]

    # If filtering removed everything, return original text
    if not sections:
        return [{'heading': None, 'content': text}]

    return sections

def _is_heading(text: str) -> bool:
    """
    Determine if text looks like a heading

    Args:
        text: Text to check

    Returns:
        True if text appears to be a heading
    """
    # Short text (less than 100 chars)
    if len(text) > 100:
        return False

    # Ends with colon (common for headings)
    if text.endswith(':'):
        return True

    # All caps (common for section titles)
    if text.isupper() and len(text.split()) <= 8:
        return True

    # Starts with common heading markers
    heading_patterns = [
        r'^#+\s+',           # Markdown headers
        r'^\d+\.\s+',        # Numbered sections (1. Introduction)
        r'^[IVX]+\.\s+',     # Roman numerals (I. Introduction)
        r'^[A-Z][a-z]+:$',   # Title Case: (Introduction:)
    ]

    for pattern in heading_patterns:
        if re.match(pattern, text):
            return True

    return False

def create_summary_excerpt(text: str, max_length: int = 300) -> str:
    """
    Create a summary excerpt from beginning of text

    Args:
        text: Full text content
        max_length: Maximum length of excerpt (default: 300)

    Returns:
        Excerpt string
    """
    if len(text) <= max_length:
        return text

    # Try to break at sentence boundary
    excerpt = text[:max_length]
    last_period = excerpt.rfind('.')
    last_question = excerpt.rfind('?')
    last_exclamation = excerpt.rfind('!')

    break_point = max(last_period, last_question, last_exclamation)

    if break_point > max_length * 0.7:  # At least 70% of target length
        return text[:break_point + 1]
    else:
        # Break at word boundary
        excerpt = text[:max_length]
        last_space = excerpt.rfind(' ')
        if last_space > 0:
            return excerpt[:last_space] + '...'
        else:
            return excerpt + '...'
