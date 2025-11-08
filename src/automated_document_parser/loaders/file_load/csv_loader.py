"""
CSV file loader implementation.
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BaseFileLoader

logger = logging.getLogger(__name__)


class CSVFileLoader(BaseFileLoader):
    """
    CSV file loader.

    Uses LangChain's CSVLoader with configurable encoding.
    """

    def load(self) -> List[Document]:
        """
        Load CSV file.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If langchain-community is not installed
        """
        try:
            from langchain_community.document_loaders import CSVLoader

            encoding = self.kwargs.get("encoding", "utf-8")
            loader = CSVLoader(str(self.file_path), encoding=encoding)
            return loader.load()

        except ImportError as e:
            logger.error(f"Failed to import CSVLoader: {e}")
            raise ImportError(
                f"langchain-community is required for CSV loading. {self.get_install_command()}"
            )
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    @staticmethod
    def get_install_command() -> str:
        """
        Return the command to install required dependencies.

        Returns:
            Installation command string
        """
        return "pip install langchain-community"
