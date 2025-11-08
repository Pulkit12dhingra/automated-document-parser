"""
Base file loader interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from langchain_core.documents import Document


class BaseFileLoader(ABC):
    """
    Abstract base class for file loaders.

    All file loader implementations should inherit from this class.
    """

    def __init__(self, file_path: str | Path, **kwargs):
        """
        Initialize the file loader.

        Args:
            file_path: Path to the file
            **kwargs: Additional loader-specific arguments
        """
        self.file_path = Path(file_path) if isinstance(file_path, str) else file_path
        self.kwargs = kwargs

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load documents from the file.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If required dependencies are not installed
            RuntimeError: If loading fails
        """
        pass

    @staticmethod
    @abstractmethod
    def get_install_command() -> str:
        """
        Return the command to install required dependencies.

        Returns:
            Installation command string
        """
        pass
