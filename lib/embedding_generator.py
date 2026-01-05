"""
Embedding generation utilities using OpenAI API
"""

import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_openai_client() -> OpenAI:
    """
    Create and return OpenAI client

    Returns:
        OpenAI client

    Raises:
        ValueError: If API key not found in environment
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env")

    return OpenAI(api_key=api_key)

def generate_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate embedding vector for text

    Args:
        text: Text to embed
        model: OpenAI embedding model (default: text-embedding-3-small)
               - text-embedding-3-small: 1536 dimensions, $0.02/1M tokens
               - text-embedding-3-large: 3072 dimensions, $0.13/1M tokens

    Returns:
        List of floats representing the embedding vector (1536 dimensions)

    Raises:
        Exception: If API call fails
    """
    client = get_openai_client()

    # Truncate text if too long (max 8191 tokens ≈ 32,000 chars)
    # For safety, limit to 30,000 chars
    if len(text) > 30000:
        text = text[:30000]

    # Generate embedding
    response = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float"
    )

    embedding = response.data[0].embedding

    return embedding

def generate_embeddings_batch(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """
    Generate embeddings for multiple texts in a single API call
    More efficient than calling generate_embedding multiple times

    Args:
        texts: List of texts to embed (max 2048 texts per batch)
        model: OpenAI embedding model

    Returns:
        List of embedding vectors

    Raises:
        Exception: If API call fails
    """
    client = get_openai_client()

    # Truncate texts if too long
    truncated_texts = [t[:30000] if len(t) > 30000 else t for t in texts]

    # OpenAI allows up to 2048 inputs per request
    if len(truncated_texts) > 2048:
        raise ValueError("Too many texts (max 2048 per batch)")

    # Generate embeddings
    response = client.embeddings.create(
        model=model,
        input=truncated_texts,
        encoding_format="float"
    )

    # Extract embeddings in order
    embeddings = [item.embedding for item in response.data]

    return embeddings

def calculate_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Similarity score between 0 and 1 (1 = identical, 0 = unrelated)
    """
    import math

    # Dot product
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

    # Magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in embedding1))
    magnitude2 = math.sqrt(sum(b * b for b in embedding2))

    # Cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    similarity = dot_product / (magnitude1 * magnitude2)

    return similarity
