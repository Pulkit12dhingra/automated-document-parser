"""Test PDF loader submodule."""

import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from langchain_core.documents import Document

from automated_document_parser.loaders.pdf_load import (
    BasePDFLoader,
    PDFLoader,
    load_pdf,
)
from automated_document_parser.loaders.pdf_load.pypdf_loader import PyPDFLoaderImpl
from automated_document_parser.loaders.pdf_load.unstructured_loader import (
    UnstructuredPDFLoader,
)
from automated_document_parser.loaders.pdf_load.textract_loader import (
    AmazonTextractPDFLoader,
)

# Check for optional dependencies
HAS_UNSTRUCTURED = importlib.util.find_spec("langchain_unstructured") is not None
HAS_BOTO3 = importlib.util.find_spec("boto3") is not None


class TestBasePDFLoader:
    """Test the BasePDFLoader abstract class."""

    def test_cannot_instantiate_abstract_class(self):
        """BasePDFLoader cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BasePDFLoader("test.pdf")

    def test_custom_loader_must_implement_load(self):
        """Custom loader must implement load method."""

        class IncompleteLoader(BasePDFLoader):
            def get_install_command(self):
                return "pip install test"

        with pytest.raises(TypeError):
            IncompleteLoader("test.pdf")

    def test_custom_loader_must_implement_get_install_command(self):
        """Custom loader must implement get_install_command method."""

        class IncompleteLoader(BasePDFLoader):
            def load(self):
                return []

        with pytest.raises(TypeError):
            IncompleteLoader("test.pdf")

    def test_custom_loader_implementation(self):
        """Custom loader can be properly implemented."""

        class CustomLoader(BasePDFLoader):
            def load(self):
                return [Document(page_content="Custom content")]

            def get_install_command(self):
                return "pip install custom-package"

        loader = CustomLoader("test.pdf")
        assert loader.file_path == Path("test.pdf")
        docs = loader.load()
        assert len(docs) == 1
        assert docs[0].page_content == "Custom content"
        assert loader.get_install_command() == "pip install custom-package"


class TestPyPDFLoaderImpl:
    """Test PyPDF loader implementation."""

    def test_initialization(self):
        """PyPDFLoaderImpl initializes correctly."""
        loader = PyPDFLoaderImpl("test.pdf")
        assert loader.file_path == Path("test.pdf")

    def test_get_install_command(self):
        """Returns correct install command."""
        loader = PyPDFLoaderImpl("test.pdf")
        cmd = loader.get_install_command()
        assert "langchain-community" in cmd
        assert "pypdf" in cmd

    @patch("langchain_community.document_loaders.PyPDFLoader")
    def test_load_success(self, mock_pypdf_loader):
        """Successfully loads PDF with PyPDF."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [
            Document(page_content="Page 1"),
            Document(page_content="Page 2"),
        ]
        mock_pypdf_loader.return_value = mock_loader_instance

        loader = PyPDFLoaderImpl("test.pdf")
        docs = loader.load()

        assert len(docs) == 2
        assert docs[0].page_content == "Page 1"
        mock_pypdf_loader.assert_called_once_with("test.pdf")

    @patch("langchain_community.document_loaders.PyPDFLoader")
    def test_load_import_error(self, mock_pypdf_loader):
        """Raises ImportError with helpful message when dependencies missing."""
        mock_pypdf_loader.side_effect = ImportError("No module named 'pypdf'")

        loader = PyPDFLoaderImpl("test.pdf")
        with pytest.raises(ImportError) as exc_info:
            loader.load()

        assert "pip install" in str(exc_info.value)

    @patch("langchain_community.document_loaders.PyPDFLoader")
    def test_load_runtime_error(self, mock_pypdf_loader):
        """Raises RuntimeError when loading fails."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.side_effect = Exception("File corrupted")
        mock_pypdf_loader.return_value = mock_loader_instance

        loader = PyPDFLoaderImpl("test.pdf")
        with pytest.raises(RuntimeError) as exc_info:
            loader.load()

        assert "Failed to load PDF" in str(exc_info.value)


class TestUnstructuredPDFLoader:
    """Test Unstructured loader implementation."""

    def test_initialization(self):
        """UnstructuredPDFLoader initializes correctly."""
        loader = UnstructuredPDFLoader("test.pdf", api_key="test-key")
        assert loader.file_path == Path("test.pdf")
        assert loader.kwargs["api_key"] == "test-key"

    def test_get_install_command(self):
        """Returns correct install command."""
        loader = UnstructuredPDFLoader("test.pdf")
        cmd = loader.get_install_command()
        assert "langchain-unstructured" in cmd

    @pytest.mark.skipif(
        not HAS_UNSTRUCTURED, reason="langchain_unstructured not installed"
    )
    @patch("langchain_unstructured.UnstructuredLoader")
    def test_load_with_api_key_in_kwargs(self, mock_unstructured_loader):
        """Successfully loads with API key in kwargs."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Content")]
        mock_unstructured_loader.return_value = mock_loader_instance

        loader = UnstructuredPDFLoader("test.pdf", api_key="test-key")
        docs = loader.load()

        assert len(docs) == 1
        mock_unstructured_loader.assert_called_once_with(["test.pdf"])

    @pytest.mark.skipif(
        not HAS_UNSTRUCTURED, reason="langchain_unstructured not installed"
    )
    @patch.dict("os.environ", {"UNSTRUCTURED_API_KEY": "env-key"})
    @patch("langchain_unstructured.UnstructuredLoader")
    def test_load_with_api_key_in_env(self, mock_unstructured_loader):
        """Successfully loads with API key from environment."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Content")]
        mock_unstructured_loader.return_value = mock_loader_instance

        loader = UnstructuredPDFLoader("test.pdf")
        docs = loader.load()

        assert len(docs) == 1

    @pytest.mark.skipif(
        not HAS_UNSTRUCTURED, reason="langchain_unstructured not installed"
    )
    @patch.dict("os.environ", {}, clear=True)
    @patch(
        "langchain_unstructured.UnstructuredLoader",
        side_effect=ImportError("No module"),
    )
    def test_load_missing_api_key(self, mock_loader):
        """Raises ImportError when dependencies missing."""
        loader = UnstructuredPDFLoader("test.pdf")
        with pytest.raises(ImportError):
            loader.load()


class TestAmazonTextractPDFLoader:
    """Test Amazon Textract loader implementation."""

    def test_initialization(self):
        """AmazonTextractPDFLoader initializes correctly."""
        loader = AmazonTextractPDFLoader("test.pdf")
        assert loader.file_path == Path("test.pdf")

    def test_initialization_with_url(self):
        """Handles URL paths correctly."""
        url = "https://example.com/doc.pdf"
        loader = AmazonTextractPDFLoader(url)
        assert loader.file_path == url

    def test_initialization_with_s3(self):
        """Handles S3 paths correctly."""
        s3_path = "s3://bucket/doc.pdf"
        loader = AmazonTextractPDFLoader(s3_path)
        assert loader.file_path == s3_path

    def test_get_install_command(self):
        """Returns correct install command."""
        loader = AmazonTextractPDFLoader("test.pdf")
        cmd = loader.get_install_command()
        assert "boto3" in cmd
        assert "amazon-textract-caller" in cmd

    @patch("langchain_community.document_loaders.AmazonTextractPDFLoader")
    def test_load_local_file_without_client(self, mock_textract_loader):
        """Successfully loads local file without explicit client."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Content")]
        mock_textract_loader.return_value = mock_loader_instance

        loader = AmazonTextractPDFLoader("test.pdf")
        docs = loader.load()

        assert len(docs) == 1
        mock_textract_loader.assert_called_once_with("test.pdf")

    @patch("langchain_community.document_loaders.AmazonTextractPDFLoader")
    def test_load_with_client(self, mock_textract_loader):
        """Successfully loads with provided boto3 client."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Content")]
        mock_textract_loader.return_value = mock_loader_instance

        mock_client = Mock()
        loader = AmazonTextractPDFLoader("test.pdf", client=mock_client)
        docs = loader.load()

        assert len(docs) == 1
        mock_textract_loader.assert_called_once_with("test.pdf", client=mock_client)

    @pytest.mark.skipif(not HAS_BOTO3, reason="boto3 not installed")
    @patch("boto3.client")
    @patch("langchain_community.document_loaders.AmazonTextractPDFLoader")
    def test_load_s3_creates_client(self, mock_textract_loader, mock_boto3_client):
        """Creates boto3 client for S3 paths."""
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client

        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Content")]
        mock_textract_loader.return_value = mock_loader_instance

        loader = AmazonTextractPDFLoader("s3://bucket/doc.pdf", region_name="us-west-2")
        docs = loader.load()

        assert len(docs) == 1
        mock_boto3_client.assert_called_once_with("textract", region_name="us-west-2")
        mock_textract_loader.assert_called_once_with(
            "s3://bucket/doc.pdf", client=mock_client
        )


class TestPDFLoader:
    """Test main PDFLoader orchestrator."""

    def test_initialization_with_pypdf(self):
        """Initializes with pypdf method."""
        loader = PDFLoader("test.pdf", method="pypdf")
        assert isinstance(loader.loader_impl, PyPDFLoaderImpl)

    def test_initialization_with_unstructured(self):
        """Initializes with unstructured method."""
        loader = PDFLoader("test.pdf", method="unstructured", api_key="test")
        assert isinstance(loader.loader_impl, UnstructuredPDFLoader)

    def test_initialization_with_textract(self):
        """Initializes with amazon_textract method."""
        loader = PDFLoader("test.pdf", method="amazon_textract")
        assert isinstance(loader.loader_impl, AmazonTextractPDFLoader)

    def test_initialization_with_invalid_method(self):
        """Raises ValueError for invalid method."""
        with pytest.raises(ValueError) as exc_info:
            PDFLoader("test.pdf", method="invalid")

        assert "Unsupported PDF loader method" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test_initialization_with_custom_loader_class(self):
        """Initializes with custom loader class."""

        class CustomLoader(BasePDFLoader):
            def load(self):
                return [Document(page_content="Custom")]

            def get_install_command(self):
                return "pip install custom"

        loader = PDFLoader("test.pdf", loader_class=CustomLoader)
        assert isinstance(loader.loader_impl, CustomLoader)

    def test_initialization_with_invalid_loader_class(self):
        """Raises TypeError if loader_class doesn't inherit from BasePDFLoader."""

        class InvalidLoader:
            pass

        with pytest.raises(TypeError) as exc_info:
            PDFLoader("test.pdf", loader_class=InvalidLoader)

        assert "BasePDFLoader" in str(exc_info.value)

    def test_custom_loader_takes_precedence(self):
        """Custom loader_class takes precedence over method parameter."""

        class CustomLoader(BasePDFLoader):
            def load(self):
                return [Document(page_content="Custom")]

            def get_install_command(self):
                return "pip install custom"

        loader = PDFLoader("test.pdf", method="pypdf", loader_class=CustomLoader)
        assert isinstance(loader.loader_impl, CustomLoader)
        assert not isinstance(loader.loader_impl, PyPDFLoaderImpl)

    @patch("langchain_community.document_loaders.PyPDFLoader")
    def test_load_delegates_to_implementation(self, mock_pypdf_loader):
        """load() delegates to the loader implementation."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Test")]
        mock_pypdf_loader.return_value = mock_loader_instance

        loader = PDFLoader("test.pdf", method="pypdf")
        docs = loader.load()

        assert len(docs) == 1
        assert docs[0].page_content == "Test"

    def test_get_install_command(self):
        """get_install_command() delegates to implementation."""
        loader = PDFLoader("test.pdf", method="pypdf")
        cmd = loader.get_install_command()
        assert "pypdf" in cmd


class TestLoadPdfFunction:
    """Test load_pdf convenience function."""

    @patch("langchain_community.document_loaders.PyPDFLoader")
    def test_load_pdf_with_defaults(self, mock_pypdf_loader):
        """load_pdf uses pypdf by default."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Test")]
        mock_pypdf_loader.return_value = mock_loader_instance

        docs = load_pdf("test.pdf")

        assert len(docs) == 1
        assert docs[0].page_content == "Test"

    @pytest.mark.skipif(
        not HAS_UNSTRUCTURED, reason="langchain_unstructured not installed"
    )
    @patch("langchain_unstructured.UnstructuredLoader")
    def test_load_pdf_with_method(self, mock_unstructured_loader):
        """load_pdf accepts method parameter."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Test")]
        mock_unstructured_loader.return_value = mock_loader_instance

        docs = load_pdf("test.pdf", method="unstructured", api_key="test")

        assert len(docs) == 1

    def test_load_pdf_with_custom_loader(self):
        """load_pdf accepts custom loader_class."""

        class CustomLoader(BasePDFLoader):
            def load(self):
                return [Document(page_content="Custom")]

            def get_install_command(self):
                return "pip install custom"

        docs = load_pdf("test.pdf", loader_class=CustomLoader)

        assert len(docs) == 1
        assert docs[0].page_content == "Custom"


class TestPDFLoaderIntegration:
    """Integration tests for PDF loader."""

    def test_method_literal_type(self):
        """PDFLoaderMethod type includes all expected values."""
        # Should not raise any errors
        loader1 = PDFLoader("test.pdf", method="pypdf")
        loader2 = PDFLoader("test.pdf", method="unstructured", api_key="test")
        loader3 = PDFLoader("test.pdf", method="amazon_textract")

        assert loader1 is not None
        assert loader2 is not None
        assert loader3 is not None

    def test_kwargs_passed_to_implementation(self):
        """Kwargs are passed through to the loader implementation."""
        loader = PDFLoader(
            "test.pdf", method="amazon_textract", region_name="eu-west-1"
        )
        assert loader.loader_impl.kwargs["region_name"] == "eu-west-1"

    @patch("langchain_community.document_loaders.PyPDFLoader")
    def test_file_path_types(self, mock_pypdf_loader):
        """Handles both string and Path file paths."""
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Document(page_content="Test")]
        mock_pypdf_loader.return_value = mock_loader_instance

        # String path
        loader1 = PDFLoader("test.pdf")
        docs1 = loader1.load()
        assert len(docs1) == 1

        # Path object
        loader2 = PDFLoader(Path("test.pdf"))
        docs2 = loader2.load()
        assert len(docs2) == 1
