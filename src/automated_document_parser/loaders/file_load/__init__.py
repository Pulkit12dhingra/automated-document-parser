"""
File loader submodule with support for multiple file types.

Provides flexible file loading with built-in support for:
- Text: .txt and .md files
- CSV: Comma-separated values
- JSON: JSON files with jq schema support
- DOCX: Microsoft Word documents
- HTML: HTML files

Users can also provide custom loader classes for additional flexibility.
"""

from .base import BaseFileLoader
from .csv_loader import CSVFileLoader
from .docx_loader import DOCXFileLoader
from .html_loader import HTMLFileLoader
from .json_loader import JSONFileLoader
from .text_loader import TextFileLoader

__all__ = [
    # Base class
    "BaseFileLoader",
    # Individual loader implementations
    "TextFileLoader",
    "CSVFileLoader",
    "JSONFileLoader",
    "DOCXFileLoader",
    "HTMLFileLoader",
]
