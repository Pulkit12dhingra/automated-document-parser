"""
Base PDF loader class and type definitions.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Literal

from langchain_core.documents import Document

logger = logging.getLogger(__name__)

PDFLoaderMethod = Literal["pypdf", "unstructured", "amazon_textract"]


class BasePDFLoader(ABC):
    """
    Abstract base class for PDF loaders.

    All PDF loader implementations should inherit from this class.
    """

    def __init__(self, file_path: str | Path, **kwargs):
        """
        Initialize the PDF loader.

        Args:
            file_path: Path to PDF file or URL
            **kwargs: Additional loader-specific arguments
        """
        self.file_path = (
            Path(file_path)
            if not str(file_path).startswith(("http", "s3://"))
            else str(file_path)
        )
        self.kwargs = kwargs
        logger.info(f"Initialized {self.__class__.__name__} for: {file_path}")

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load PDF documents.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If required dependencies are not installed
            RuntimeError: If loading fails
        """
        pass

    @abstractmethod
    def get_install_command(self) -> str:
        """
        Get the pip install command for required dependencies.

        Returns:
            Install command string
        """
        pass
