"""
HTML file loader implementation.
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BaseFileLoader

logger = logging.getLogger(__name__)


class HTMLFileLoader(BaseFileLoader):
    """
    HTML file loader.

    Uses LangChain's UnstructuredHTMLLoader.
    """

    def load(self) -> List[Document]:
        """
        Load HTML file.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If langchain-community or unstructured is not installed
        """
        try:
            from langchain_community.document_loaders import UnstructuredHTMLLoader

            loader = UnstructuredHTMLLoader(str(self.file_path))
            return loader.load()

        except ImportError as e:
            logger.error(f"Failed to import UnstructuredHTMLLoader: {e}")
            raise ImportError(
                f"langchain-community and unstructured are required for HTML loading. {self.get_install_command()}"
            )
        except Exception as e:
            logger.error(f"Error loading HTML file: {e}")
            raise

    @staticmethod
    def get_install_command() -> str:
        """
        Return the command to install required dependencies.

        Returns:
            Installation command string
        """
        return "pip install langchain-community unstructured"
