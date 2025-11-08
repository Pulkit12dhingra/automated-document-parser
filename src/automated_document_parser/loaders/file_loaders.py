"""Local file system loaders (pdf, txt, csv, etc.)."""

import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
    TextLoader,
    UnstructuredHTMLLoader,
)
from langchain_core.documents import Document

from ..config import LOADER_CONFIG
from ..utils import detect_file_type, validate_file_path
from .pdf_load import PDFLoader, PDFLoaderMethod

logger = logging.getLogger(__name__)


class FileLoader:
    """Automated file loader that detects file type and loads documents."""

    def __init__(
        self,
        file_path: str | Path,
        pdf_loader_method: PDFLoaderMethod = "pypdf",
        **pdf_loader_kwargs,
    ):
        """
        Initialize the FileLoader.

        Args:
            file_path: Path to the file to load
            pdf_loader_method: Method to use for PDF loading ('pypdf', 'unstructured', 'amazon_textract')
            **pdf_loader_kwargs: Additional keyword arguments for PDF loader (e.g., client, api_key)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is unsupported
        """
        self.file_path = validate_file_path(file_path)
        self.file_type = detect_file_type(self.file_path)
        self.pdf_loader_method = pdf_loader_method
        self.pdf_loader_kwargs = pdf_loader_kwargs

        if self.file_type is None:
            raise ValueError(
                f"Unsupported file type: {self.file_path.suffix}. "
                f"File: {self.file_path}"
            )

        logger.info(f"Initialized loader for {self.file_type} file: {self.file_path}")
        if self.file_type == "pdf":
            logger.info(f"PDF loader method: {pdf_loader_method}")

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

        # Special handling for PDF files with configurable method
        if self.file_type == "pdf":
            return PDFLoader(
                self.file_path,
                method=self.pdf_loader_method,
                **self.pdf_loader_kwargs,
            )

        # Other file type loaders
        loaders = {
            "text": lambda: TextLoader(
                file_str, encoding=LOADER_CONFIG["text"]["encoding"]
            ),
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


def load_document(
    file_path: str | Path,
    pdf_loader_method: PDFLoaderMethod = "pypdf",
    **pdf_loader_kwargs,
) -> List[Document]:
    """
    Convenience function to load a document from a file.

    Args:
        file_path: Path to the file
        pdf_loader_method: Method to use for PDF loading ('pypdf', 'unstructured', 'amazon_textract')
        **pdf_loader_kwargs: Additional keyword arguments for PDF loader

    Returns:
        List of LangChain Document objects

    Examples:
        >>> # Load a text file
        >>> documents = load_document("path/to/file.txt")

        >>> # Load a PDF with default PyPDF
        >>> documents = load_document("path/to/file.pdf")

        >>> # Load a PDF with Unstructured
        >>> documents = load_document("path/to/file.pdf", pdf_loader_method="unstructured")

        >>> # Load a PDF with Amazon Textract
        >>> import boto3
        >>> client = boto3.client("textract", region_name="us-east-2")
        >>> documents = load_document(
        ...     "s3://bucket/file.pdf",
        ...     pdf_loader_method="amazon_textract",
        ...     client=client
        ... )
    """
    loader = FileLoader(
        file_path, pdf_loader_method=pdf_loader_method, **pdf_loader_kwargs
    )
    return loader.load()
