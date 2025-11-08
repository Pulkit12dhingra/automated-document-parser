"""
Text file loader implementation.

Supports .txt and .md (markdown) files.
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BaseFileLoader

logger = logging.getLogger(__name__)


class TextFileLoader(BaseFileLoader):
    """
    Text file loader for .txt and .md files.

    Uses LangChain's TextLoader with configurable encoding.
    """

    def load(self) -> List[Document]:
        """
        Load text file.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If langchain-community is not installed
        """
        try:
            from langchain_community.document_loaders import TextLoader

            encoding = self.kwargs.get("encoding", "utf-8")
            loader = TextLoader(str(self.file_path), encoding=encoding)
            return loader.load()

        except ImportError as e:
            logger.error(f"Failed to import TextLoader: {e}")
            raise ImportError(
                f"langchain-community is required for text loading. {self.get_install_command()}"
            )
        except Exception as e:
            logger.error(f"Error loading text file: {e}")
            raise

    @staticmethod
    def get_install_command() -> str:
        """
        Return the command to install required dependencies.

        Returns:
            Installation command string
        """
        return "pip install langchain-community"
