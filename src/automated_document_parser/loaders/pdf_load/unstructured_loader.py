"""
Unstructured API loader implementation.

Reference: https://docs.langchain.com/oss/python/integrations/document_loaders/unstructured_file
"""

import logging
import os
from typing import List

from langchain_core.documents import Document

from .base import BasePDFLoader

logger = logging.getLogger(__name__)


class UnstructuredPDFLoader(BasePDFLoader):
    """
    PDF loader using Unstructured API backend.

    Advanced parsing with support for complex document layouts.
    Requires UNSTRUCTURED_API_KEY environment variable or api_key in kwargs.
    """

    def load(self) -> List[Document]:
        """
        Load PDF using Unstructured API.

        Returns:
            List of LangChain Document objects

        Raises:
            ValueError: If API key is not provided
            ImportError: If langchain-unstructured is not installed
        """
        try:
            from langchain_unstructured import UnstructuredLoader

            # Check for API key
            api_key = self.kwargs.get("api_key") or os.environ.get(
                "UNSTRUCTURED_API_KEY"
            )
            if not api_key:
                raise ValueError(
                    "UNSTRUCTURED_API_KEY not found. Set it as environment variable or pass as api_key parameter."
                )

            # Prepare file paths (UnstructuredLoader expects a list)
            file_paths = (
                [str(self.file_path)]
                if not isinstance(self.file_path, list)
                else self.file_path
            )

            loader = UnstructuredLoader(file_paths)
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} documents with Unstructured")
            return docs
        except ImportError as e:
            logger.error(f"Unstructured dependencies not installed: {e}")
            raise ImportError(
                f"Required package not installed for unstructured. "
                f"Install with: {self.get_install_command()}"
            ) from e
        except Exception as e:
            logger.error(f"Error loading PDF with Unstructured: {e}")
            raise RuntimeError(f"Failed to load PDF: {e}") from e

    def get_install_command(self) -> str:
        """Get pip install command for Unstructured dependencies."""
        return 'pip install "langchain-unstructured[local]"'
