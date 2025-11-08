"""Configuration and mappings for document loaders."""

from typing import Dict, List

# Supported file extensions mapped to their loader types
FILE_EXTENSION_MAPPING: Dict[str, str] = {
    # Text files
    ".txt": "text",
    ".md": "text",
    ".markdown": "text",
    # PDF files
    ".pdf": "pdf",
    # CSV files
    ".csv": "csv",
    # JSON files
    ".json": "json",
    # Word documents
    ".docx": "docx",
    ".doc": "docx",
    # HTML files
    ".html": "html",
    ".htm": "html",
}

# File extensions that support different loaders
SUPPORTED_EXTENSIONS: List[str] = list(FILE_EXTENSION_MAPPING.keys())

# Default encoding for text files
DEFAULT_ENCODING: str = "utf-8"

# PDF loader methods
PDF_LOADER_METHODS = ["pypdf", "unstructured", "amazon_textract"]
DEFAULT_PDF_LOADER_METHOD = "pypdf"

# Loader-specific configurations
LOADER_CONFIG: Dict[str, Dict] = {
    "pdf": {
        "extract_images": False,
        "default_method": DEFAULT_PDF_LOADER_METHOD,
        "pypdf": {
            "extract_images": False,
        },
        "unstructured": {
            "requires_api_key": True,
            "env_var": "UNSTRUCTURED_API_KEY",
        },
        "amazon_textract": {
            "requires_boto3": True,
            "default_region": "us-east-2",
        },
    },
    "csv": {
        "encoding": DEFAULT_ENCODING,
    },
    "text": {
        "encoding": DEFAULT_ENCODING,
        "autodetect_encoding": True,
    },
}
