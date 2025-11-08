"""
Main PDF loader with support for multiple backends.
"""

import logging
from pathlib import Path
from typing import List

from langchain_core.documents import Document

from .base import BasePDFLoader, PDFLoaderMethod
from .pypdf_loader import PyPDFLoaderImpl
from .unstructured_loader import UnstructuredPDFLoader
from .textract_loader import AmazonTextractPDFLoader

logger = logging.getLogger(__name__)

# Registry of available PDF loaders
PDF_LOADER_REGISTRY = {
    "pypdf": PyPDFLoaderImpl,
    "unstructured": UnstructuredPDFLoader,
    "amazon_textract": AmazonTextractPDFLoader,
}


class PDFLoader:
    """
    Flexible PDF loader supporting multiple parsing backends.

    By default, uses PyPDF for standard PDF parsing. Users can specify
    alternative methods like 'unstructured' for advanced parsing or
    'amazon_textract' for OCR capabilities.

    Users can also provide custom loader classes that inherit from BasePDFLoader.
    """

    def __init__(
        self,
        file_path: str | Path,
        method: PDFLoaderMethod | str = "pypdf",
        loader_class: type[BasePDFLoader] | None = None,
        **kwargs,
    ):
        """
        Initialize PDF loader with specified method or custom loader.

        Args:
            file_path: Path to PDF file or URL (for amazon_textract)
            method: Loading method - 'pypdf' (default), 'unstructured', or 'amazon_textract'
                   Can also be a custom string if loader_class is provided
            loader_class: Optional custom loader class inheriting from BasePDFLoader.
                         If provided, this takes precedence over the method parameter.
            **kwargs: Additional arguments passed to the specific loader
                For amazon_textract:
                    - client: boto3 Textract client (optional)
                    - region_name: AWS region (default: 'us-east-2')
                For unstructured:
                    - api_key: Unstructured API key (or set UNSTRUCTURED_API_KEY env var)

        Raises:
            ValueError: If method is not supported and no loader_class is provided
            TypeError: If loader_class doesn't inherit from BasePDFLoader

        Examples:
            >>> # Default PyPDF loader
            >>> loader = PDFLoader("document.pdf")
            >>> docs = loader.load()

            >>> # Use Unstructured
            >>> loader = PDFLoader("document.pdf", method="unstructured")
            >>> docs = loader.load()

            >>> # Use custom loader class
            >>> from my_loaders import CustomPDFLoader
            >>> loader = PDFLoader("document.pdf", loader_class=CustomPDFLoader)
            >>> docs = loader.load()
        """
        self.file_path = file_path
        self.method = method
        self.kwargs = kwargs

        # Use custom loader class if provided
        if loader_class is not None:
            if not issubclass(loader_class, BasePDFLoader):
                raise TypeError(
                    f"loader_class must inherit from BasePDFLoader, got {loader_class}"
                )
            self.loader_impl = loader_class(file_path, **kwargs)
            logger.info(f"Using custom PDF loader: {loader_class.__name__}")
        else:
            # Use registered loader based on method
            if method not in PDF_LOADER_REGISTRY:
                available = ", ".join(PDF_LOADER_REGISTRY.keys())
                raise ValueError(
                    f"Unsupported PDF loader method: {method}. "
                    f"Choose from: {available}, or provide a custom loader_class"
                )

            loader_class = PDF_LOADER_REGISTRY[method]
            self.loader_impl = loader_class(file_path, **kwargs)
            logger.info(f"Initialized PDFLoader with method: {method}")

    def load(self) -> List[Document]:
        """
        Load PDF documents using the specified method or loader.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If required dependencies are not installed
            RuntimeError: If loading fails
        """
        return self.loader_impl.load()

    def get_install_command(self) -> str:
        """Get pip install command for the current loader's dependencies."""
        return self.loader_impl.get_install_command()


def load_pdf(
    file_path: str | Path,
    method: PDFLoaderMethod | str = "pypdf",
    loader_class: type[BasePDFLoader] | None = None,
    **kwargs,
) -> List[Document]:
    """
    Convenience function to load a PDF document.

    Args:
        file_path: Path to PDF file or URL
        method: Loading method - 'pypdf' (default), 'unstructured', or 'amazon_textract'
        loader_class: Optional custom loader class inheriting from BasePDFLoader
        **kwargs: Additional arguments for the loader

    Returns:
        List of LangChain Document objects

    Examples:
        >>> # Basic usage with PyPDF (default)
        >>> docs = load_pdf("paper.pdf")

        >>> # Use Unstructured API
        >>> docs = load_pdf("paper.pdf", method="unstructured")

        >>> # Use Amazon Textract with URL
        >>> docs = load_pdf(
        ...     "https://example.com/document.pdf",
        ...     method="amazon_textract"
        ... )

        >>> # Use Amazon Textract with S3
        >>> import boto3
        >>> client = boto3.client("textract", region_name="us-east-2")
        >>> docs = load_pdf(
        ...     "s3://bucket/document.pdf",
        ...     method="amazon_textract",
        ...     client=client
        ... )

        >>> # Use custom loader
        >>> from my_loaders import MyCustomLoader
        >>> docs = load_pdf("paper.pdf", loader_class=MyCustomLoader)
    """
    loader = PDFLoader(file_path, method=method, loader_class=loader_class, **kwargs)
    return loader.load()
