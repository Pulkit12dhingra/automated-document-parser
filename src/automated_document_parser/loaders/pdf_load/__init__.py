"""
PDF loader submodule with support for multiple backends.

Provides flexible PDF loading with built-in support for:
- PyPDF: Fast, simple PDF parsing (default)
- Unstructured: Advanced parsing with API support
- Amazon Textract: OCR for scanned documents

Users can also provide custom loader classes for additional flexibility.
"""

from .base import BasePDFLoader, PDFLoaderMethod
from .loader import PDFLoader, load_pdf
from .pypdf_loader import PyPDFLoaderImpl
from .textract_loader import AmazonTextractPDFLoader
from .unstructured_loader import UnstructuredPDFLoader

__all__ = [
    # Main API
    "PDFLoader",
    "load_pdf",
    # Base classes and types
    "BasePDFLoader",
    "PDFLoaderMethod",
    # Individual loader implementations (for advanced usage)
    "PyPDFLoaderImpl",
    "UnstructuredPDFLoader",
    "AmazonTextractPDFLoader",
]
