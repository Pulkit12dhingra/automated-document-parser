"""
Amazon Textract loader implementation.

Reference: https://docs.langchain.com/oss/python/integrations/document_loaders/amazon_textract
"""

import logging
from typing import List

from langchain_core.documents import Document

from .base import BasePDFLoader

logger = logging.getLogger(__name__)


class AmazonTextractPDFLoader(BasePDFLoader):
    """
    PDF loader using Amazon Textract backend.

    OCR service for extracting text from scanned documents and images.
    Supports local files, HTTP/HTTPS URLs, and S3 URIs.

    Requires AWS credentials to be configured.
    """

    def load(self) -> List[Document]:
        """
        Load PDF using Amazon Textract.

        Returns:
            List of LangChain Document objects

        Raises:
            ImportError: If boto3 or amazon-textract-caller is not installed
        """
        try:
            from langchain_community.document_loaders import (
                AmazonTextractPDFLoader as TextractLoader,
            )

            # Get optional boto3 client
            textract_client = self.kwargs.get("client")

            if textract_client is None and str(self.file_path).startswith("s3://"):
                # For S3 files, create a client with specified region
                import boto3

                region = self.kwargs.get("region_name", "us-east-2")
                textract_client = boto3.client("textract", region_name=region)
                logger.info(f"Created Textract client for region: {region}")

            # Load with or without client
            if textract_client:
                loader = TextractLoader(str(self.file_path), client=textract_client)
            else:
                loader = TextractLoader(str(self.file_path))

            docs = loader.load()
            logger.info(f"Loaded {len(docs)} documents with Amazon Textract")
            return docs
        except ImportError as e:
            logger.error(f"Amazon Textract dependencies not installed: {e}")
            raise ImportError(
                f"Required package not installed for amazon_textract. "
                f"Install with: {self.get_install_command()}"
            ) from e
        except Exception as e:
            logger.error(f"Error loading PDF with Amazon Textract: {e}")
            raise RuntimeError(f"Failed to load PDF: {e}") from e

    def get_install_command(self) -> str:
        """Get pip install command for Amazon Textract dependencies."""
        return "pip install boto3 amazon-textract-caller>=0.2.0"
