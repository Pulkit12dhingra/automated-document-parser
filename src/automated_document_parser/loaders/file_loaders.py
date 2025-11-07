"""Local file system loaders (pdf, txt, csv, etc.)."""

import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
)
from langchain_core.documents import Document

from ..config import LOADER_CONFIG
from ..utils import detect_file_type, validate_file_path

logger = logging.getLogger(__name__)


class FileLoader:
    """Automated file loader that detects file type and loads documents."""

    def __init__(self, file_path: str | Path):
        """
        Initialize the FileLoader.

        Args:
            file_path: Path to the file to load

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is unsupported
        """
        self.file_path = validate_file_path(file_path)
        self.file_type = detect_file_type(self.file_path)

        if self.file_type is None:
            raise ValueError(
                f"Unsupported file type: {self.file_path.suffix}. "
                f"File: {self.file_path}"
            )

        logger.info(f"Initialized loader for {self.file_type} file: {self.file_path}")

    def load(self) -> List[Document]:
        """
        Load documents from the file.

        Returns:
            List of LangChain Document objects

        Raises:
            RuntimeError: If loading fails
        """
        try:
            loader = self._get_loader()
            documents = loader.load()
            logger.info(
                f"Successfully loaded {len(documents)} documents from {self.file_path}"
            )
            return documents
        except Exception as e:
            logger.error(f"Error loading file {self.file_path}: {e}")
            raise RuntimeError(f"Failed to load file: {e}") from e

    def _get_loader(self):
        """
        Get appropriate LangChain loader based on file type.

        Returns:
            LangChain document loader instance
        """
        file_str = str(self.file_path)

        loaders = {
            "text": lambda: TextLoader(
                file_str, encoding=LOADER_CONFIG["text"]["encoding"]
            ),
            "pdf": lambda: PyPDFLoader(file_str),
            "csv": lambda: CSVLoader(
                file_str, encoding=LOADER_CONFIG["csv"]["encoding"]
            ),
            "json": lambda: JSONLoader(file_str, jq_schema=".", text_content=False),
            "docx": lambda: Docx2txtLoader(file_str),
            "html": lambda: UnstructuredHTMLLoader(file_str),
        }

        if self.file_type not in loaders:
            raise ValueError(f"No loader available for file type: {self.file_type}")

        return loaders[self.file_type]()


def load_document(file_path: str | Path) -> List[Document]:
    """
    Convenience function to load a document from a file.

    Args:
        file_path: Path to the file

    Returns:
        List of LangChain Document objects

    Example:
        >>> documents = load_document("path/to/file.pdf")
        >>> for doc in documents:
        ...     print(doc.page_content)
    """
    loader = FileLoader(file_path)
    return loader.load()
