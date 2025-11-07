"""Main DocumentParser class for automated document loading."""

import logging
from pathlib import Path
from typing import List, Union

from langchain_core.documents import Document

from .loaders.file_loaders import FileLoader
from .utils import get_file_info, is_supported_file

logger = logging.getLogger(__name__)


class DocumentParser:
    """
    Main class for automated document parsing.

    Automatically detects file type and loads documents using appropriate loaders.
    Designed for seamless integration with LangChain RAG pipelines.
    """

    def __init__(self):
        """Initialize the DocumentParser."""
        self.loaded_files: List[str] = []

    def parse(self, file_path: str | Path) -> List[Document]:
        """
        Parse a document from file path.

        Args:
            file_path: Path to the document file

        Returns:
            List of LangChain Document objects

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is unsupported
            RuntimeError: If parsing fails

        Example:
            >>> parser = DocumentParser()
            >>> docs = parser.parse("document.pdf")
            >>> print(f"Loaded {len(docs)} documents")
        """
        if not is_supported_file(file_path):
            path = Path(file_path)
            raise ValueError(
                f"Unsupported file type: {path.suffix}. "
                f"Supported types: .txt, .pdf, .csv, .json, .docx, .html, .md"
            )

        loader = FileLoader(file_path)
        documents = loader.load()

        # Track loaded files
        self.loaded_files.append(str(Path(file_path).resolve()))

        # Add file metadata to documents
        file_info = get_file_info(file_path)
        for doc in documents:
            doc.metadata.update(
                {
                    "source": file_info["absolute_path"],
                    "file_name": file_info["name"],
                    "file_type": file_info["extension"],
                }
            )

        logger.info(f"Parsed {len(documents)} documents from {file_path}")
        return documents

    def parse_multiple(
        self, file_paths: List[Union[str, Path]]
    ) -> dict[str, List[Document]]:
        """
        Parse multiple documents.

        Args:
            file_paths: List of file paths

        Returns:
            Dictionary mapping file paths to their loaded documents

        Example:
            >>> parser = DocumentParser()
            >>> results = parser.parse_multiple(["doc1.pdf", "doc2.txt"])
            >>> for file, docs in results.items():
            ...     print(f"{file}: {len(docs)} documents")
        """
        results = {}
        for file_path in file_paths:
            try:
                documents = self.parse(file_path)
                results[str(file_path)] = documents
            except Exception as e:
                logger.error(f"Failed to parse {file_path}: {e}")
                results[str(file_path)] = []

        return results

    def get_loaded_files(self) -> List[str]:
        """
        Get list of successfully loaded files.

        Returns:
            List of file paths that were successfully loaded
        """
        return self.loaded_files.copy()
