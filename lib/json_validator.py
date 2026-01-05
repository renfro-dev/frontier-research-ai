"""
JSON schema validation for analysis outputs
"""

from typing import Dict, Any, List, Tuple
import logging

# Expected schema for analysis_json
ANALYSIS_SCHEMA = {
    "claims": {
        "type": "array",
        "required": True,
        "items": {
            "claim": {"type": "str", "required": True},
            "context": {"type": "str", "required": True}
        }
    },
    "metaphors": {
        "type": "array",
        "required": True,
        "items": {
            "metaphor": {"type": "str", "required": True},
            "explanation": {"type": "str", "required": True}
        }
    },
    "examples": {
        "type": "array",
        "required": True,
        "items": {
            "example": {"type": "str", "required": True},
            "context": {"type": "str", "required": True}
        }
    },
    "uncertainties": {
        "type": "array",
        "required": True,
        "items": {
            "topic": {"type": "str", "required": True},
            "nature_of_uncertainty": {"type": "str", "required": True},
            "author_statement": {"type": "str", "required": False}
        }
    },
    "conflicts": {
        "type": "array",
        "required": True,
        "items": {
            "topic": {"type": "str", "required": True},
            "description": {"type": "str", "required": True}
        }
    }
}


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_analysis_json(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate analysis JSON against required schema

    Args:
        data: The analysis JSON dict to validate

    Returns:
        Tuple of (is_valid, error_messages)
        - is_valid: Boolean indicating if validation passed
        - error_messages: List of validation error messages (empty if valid)

    Example:
        >>> data = {"claims": [], "metaphors": [], ...}
        >>> is_valid, errors = validate_analysis_json(data)
        >>> if not is_valid:
        ...     print(f"Validation failed: {errors}")
    """
    logger = logging.getLogger(__name__)
    errors = []

    # Check for all required top-level fields
    required_fields = ["claims", "metaphors", "examples", "uncertainties", "conflicts"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    # If missing fields, return early
    if errors:
        return False, errors

    # Validate each field is an array
    for field in required_fields:
        if not isinstance(data[field], list):
            errors.append(f"Field '{field}' must be an array, got {type(data[field]).__name__}")

    # If field types are wrong, return early
    if errors:
        return False, errors

    # Validate structure of items in each array
    field_schemas = {
        "claims": ["claim", "context"],
        "metaphors": ["metaphor", "explanation"],
        "examples": ["example", "context"],
        "uncertainties": ["topic", "nature_of_uncertainty"],  # author_statement is optional
        "conflicts": ["topic", "description"]
    }

    for field, required_subfields in field_schemas.items():
        items = data[field]

        for i, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{field}[{i}] must be an object, got {type(item).__name__}")
                continue

            # Check required subfields
            for subfield in required_subfields:
                if subfield not in item:
                    errors.append(f"{field}[{i}] missing required subfield: '{subfield}'")
                elif not isinstance(item[subfield], str):
                    errors.append(
                        f"{field}[{i}].{subfield} must be a string, "
                        f"got {type(item[subfield]).__name__}"
                    )
                elif not item[subfield].strip():
                    errors.append(f"{field}[{i}].{subfield} cannot be empty")

    # Check for unexpected top-level fields (warn but don't fail)
    unexpected_fields = set(data.keys()) - set(required_fields)
    for field in unexpected_fields:
        if not field.startswith("_"):  # Allow fields starting with _ (like _note)
            logger.warning(f"Unexpected field in analysis JSON: '{field}'")

    is_valid = len(errors) == 0
    return is_valid, errors


def repair_analysis_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Attempt to repair common JSON issues automatically

    Args:
        data: The analysis JSON dict to repair

    Returns:
        Repaired JSON dict

    Raises:
        ValidationError: If JSON cannot be repaired

    Common repairs:
        - Add missing fields as empty arrays
        - Remove null entries from arrays
        - Fix capitalization of field names
        - Remove empty string values
    """
    logger = logging.getLogger(__name__)
    repaired = data.copy()

    # Add missing required fields as empty arrays
    required_fields = ["claims", "metaphors", "examples", "uncertainties", "conflicts"]
    for field in required_fields:
        if field not in repaired:
            logger.info(f"Repair: Adding missing field '{field}' as empty array")
            repaired[field] = []

    # Fix capitalization of field names
    field_mapping = {
        "Claims": "claims",
        "Metaphors": "metaphors",
        "Examples": "examples",
        "Uncertainties": "uncertainties",
        "Conflicts": "conflicts"
    }
    for wrong, correct in field_mapping.items():
        if wrong in repaired and correct not in repaired:
            logger.info(f"Repair: Renaming '{wrong}' to '{correct}'")
            repaired[correct] = repaired.pop(wrong)

    # Ensure all fields are arrays
    for field in required_fields:
        if field in repaired and not isinstance(repaired[field], list):
            logger.info(f"Repair: Converting '{field}' to array")
            # If it's a single dict, wrap in array
            if isinstance(repaired[field], dict):
                repaired[field] = [repaired[field]]
            else:
                repaired[field] = []

    # Remove null entries from arrays
    for field in required_fields:
        if field in repaired:
            original_len = len(repaired[field])
            repaired[field] = [item for item in repaired[field] if item is not None]
            if len(repaired[field]) < original_len:
                logger.info(
                    f"Repair: Removed {original_len - len(repaired[field])} null entries "
                    f"from '{field}'"
                )

    # Remove items with missing required subfields
    field_schemas = {
        "claims": ["claim", "context"],
        "metaphors": ["metaphor", "explanation"],
        "examples": ["example", "context"],
        "uncertainties": ["topic", "nature_of_uncertainty"],
        "conflicts": ["topic", "description"]
    }

    for field, required_subfields in field_schemas.items():
        if field in repaired:
            original_len = len(repaired[field])
            repaired[field] = [
                item for item in repaired[field]
                if isinstance(item, dict) and all(
                    subfield in item and item[subfield] and str(item[subfield]).strip()
                    for subfield in required_subfields
                )
            ]
            if len(repaired[field]) < original_len:
                removed = original_len - len(repaired[field])
                logger.info(f"Repair: Removed {removed} invalid items from '{field}'")

    # Validate repaired JSON
    is_valid, errors = validate_analysis_json(repaired)

    if not is_valid:
        error_msg = f"Could not repair JSON. Remaining errors: {', '.join(errors)}"
        logger.error(error_msg)
        raise ValidationError(error_msg)

    logger.info("Successfully repaired JSON")
    return repaired


def get_analysis_stats(data: Dict[str, Any]) -> Dict[str, int]:
    """
    Get statistics about the analysis JSON

    Args:
        data: The analysis JSON dict

    Returns:
        Dict with counts for each field type

    Example:
        >>> stats = get_analysis_stats(data)
        >>> print(f"Found {stats['claims']} claims")
    """
    return {
        "claims": len(data.get("claims", [])),
        "metaphors": len(data.get("metaphors", [])),
        "examples": len(data.get("examples", [])),
        "uncertainties": len(data.get("uncertainties", [])),
        "conflicts": len(data.get("conflicts", []))
    }
