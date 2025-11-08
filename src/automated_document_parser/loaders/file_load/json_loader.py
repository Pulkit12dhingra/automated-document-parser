"""
JSON file loader implementation.
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BaseFileLoader

logger = logging.getLogger(__name__)


class JSONFileLoader(BaseFileLoader):
    """
    JSON file loader.

    Uses LangChain's JSONLoader with jq schema support.
    """

    def load(self) -> List[Document]:
        """
        Load JSON file.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If langchain-community or jq is not installed
        """
        try:
            from langchain_community.document_loaders import JSONLoader

            jq_schema = self.kwargs.get("jq_schema", ".")
            text_content = self.kwargs.get("text_content", False)
            loader = JSONLoader(
                str(self.file_path), jq_schema=jq_schema, text_content=text_content
            )
            return loader.load()

        except ImportError as e:
            logger.error(f"Failed to import JSONLoader: {e}")
            raise ImportError(
                f"langchain-community and jq are required for JSON loading. {self.get_install_command()}"
            )
        except Exception as e:
            logger.error(f"Error loading JSON file: {e}")
            raise

    @staticmethod
    def get_install_command() -> str:
        """
        Return the command to install required dependencies.

        Returns:
            Installation command string
        """
        return "pip install langchain-community jq"
