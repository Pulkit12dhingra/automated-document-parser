"""Document loaders package."""

from .file_load import (
    BaseFileLoader,
    CSVFileLoader,
    DOCXFileLoader,
    HTMLFileLoader,
    JSONFileLoader,
    TextFileLoader,
)
from .file_loaders import FileLoader, load_document
from .pdf_load import PDFLoader, PDFLoaderMethod, load_pdf

__all__ = [
    # Main loaders
    "FileLoader",
    "load_document",
    # PDF loaders
    "PDFLoader",
    "PDFLoaderMethod",
    "load_pdf",
    # File loaders
    "BaseFileLoader",
    "TextFileLoader",
    "CSVFileLoader",
    "JSONFileLoader",
    "DOCXFileLoader",
    "HTMLFileLoader",
]
