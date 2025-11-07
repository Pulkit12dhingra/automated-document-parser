"""Helper functions for document parsing."""

import logging
from pathlib import Path
from typing import Optional

from .config import FILE_EXTENSION_MAPPING, SUPPORTED_EXTENSIONS

# Configure logging
logger = logging.getLogger(__name__)


def detect_file_type(file_path: str | Path) -> Optional[str]:
    """
    Detect file type based on extension.

    Args:
        file_path: Path to the file

    Returns:
        Loader type string or None if unsupported

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    extension = path.suffix.lower()

    if extension not in FILE_EXTENSION_MAPPING:
        logger.warning(f"Unsupported file extension: {extension}")
        return None

    return FILE_EXTENSION_MAPPING[extension]


def is_supported_file(file_path: str | Path) -> bool:
    """
    Check if file type is supported.

    Args:
        file_path: Path to the file

    Returns:
        True if supported, False otherwise
    """
    try:
        extension = Path(file_path).suffix.lower()
        return extension in SUPPORTED_EXTENSIONS
    except Exception as e:
        logger.error(f"Error checking file support: {e}")
        return False


def validate_file_path(file_path: str | Path) -> Path:
    """
    Validate and normalize file path.

    Args:
        file_path: Path to validate

    Returns:
        Normalized Path object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If path is not a file
    """
    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    return path


def get_file_info(file_path: str | Path) -> dict:
    """
    Get basic file information.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file metadata
    """
    path = Path(file_path)
    stat = path.stat()

    return {
        "name": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "absolute_path": str(path.resolve()),
    }
