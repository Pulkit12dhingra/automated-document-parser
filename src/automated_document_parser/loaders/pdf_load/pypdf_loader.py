"""
PyPDF loader implementation.

Reference: https://docs.langchain.com/oss/python/integrations/document_loaders/pypdfloader
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BasePDFLoader

logger = logging.getLogger(__name__)


class PyPDFLoaderImpl(BasePDFLoader):
    """
    PDF loader using PyPDF backend.

    Fast and simple PDF parsing suitable for most standard PDFs.
    This is the default loader method.
    """

    def load(self) -> List[Document]:
        """
        Load PDF using PyPDF.

        Returns:
            List of LangChain Document objects
        """
        try:
            from langchain_community.document_loaders import PyPDFLoader

            loader = PyPDFLoader(str(self.file_path))
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} pages with PyPDF")
            return docs
        except ImportError as e:
            logger.error(f"PyPDF dependencies not installed: {e}")
            raise ImportError(
                f"Required package not installed for pypdf. "
                f"Install with: {self.get_install_command()}"
            ) from e
        except Exception as e:
            logger.error(f"Error loading PDF with PyPDF: {e}")
            raise RuntimeError(f"Failed to load PDF: {e}") from e

    def get_install_command(self) -> str:
        """Get pip install command for PyPDF dependencies."""
        return "pip install langchain-community pypdf"
