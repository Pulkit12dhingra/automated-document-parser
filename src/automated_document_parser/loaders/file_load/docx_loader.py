"""
DOCX file loader implementation.
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BaseFileLoader

logger = logging.getLogger(__name__)


class DOCXFileLoader(BaseFileLoader):
    """
    DOCX file loader for Microsoft Word documents.

    Uses LangChain's Docx2txtLoader.
    """

    def load(self) -> List[Document]:
        """
        Load DOCX file.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If langchain-community or docx2txt is not installed
        """
        try:
            from langchain_community.document_loaders import Docx2txtLoader

            loader = Docx2txtLoader(str(self.file_path))
            return loader.load()

        except ImportError as e:
            logger.error(f"Failed to import Docx2txtLoader: {e}")
            raise ImportError(
                f"langchain-community and docx2txt are required for DOCX loading. {self.get_install_command()}"
            )
        except Exception as e:
            logger.error(f"Error loading DOCX file: {e}")
            raise

    @staticmethod
    def get_install_command() -> str:
        """
        Return the command to install required dependencies.

        Returns:
            Installation command string
        """
        return "pip install langchain-community docx2txt"
