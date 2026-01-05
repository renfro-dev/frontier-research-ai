"""
Content hashing utilities for deduplication
"""

import hashlib

def calculate_content_hash(content: str) -> str:
    """
    Calculate SHA256 hash of content for deduplication

    Args:
        content: Text content to hash

    Returns:
        Hex-encoded SHA256 hash
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def content_is_duplicate(hash1: str, hash2: str) -> bool:
    """
    Check if two content hashes match

    Args:
        hash1: First hash
        hash2: Second hash

    Returns:
        True if hashes match (duplicate content)
    """
    return hash1 == hash2
