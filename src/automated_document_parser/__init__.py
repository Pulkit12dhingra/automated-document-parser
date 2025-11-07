"""Automated Document Parser - Intelligent document loading for LangChain."""

from .core import DocumentParser
from .loaders import FileLoader, load_document

__version__ = "0.1.2"
__all__ = ["DocumentParser", "FileLoader", "load_document"]
