"""Test file loaders."""

import tempfile
from pathlib import Path

import pytest

from automated_document_parser.loaders.file_loaders import FileLoader, load_document


@pytest.fixture
def temp_text_file():
    """Create a temporary text file with content."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is a test document.\nIt has multiple lines.\n")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,city\n")
        f.write("Alice,30,NYC\n")
        f.write("Bob,25,LA\n")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write('{"message": "Hello, World!", "count": 42}')
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_markdown_file():
    """Create a temporary Markdown file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# Test Document\n\nThis is a markdown file.\n")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


class TestFileLoader:
    """Tests for FileLoader class."""

    def test_init_with_valid_file(self, temp_text_file):
        """Test initialization with valid file."""
        loader = FileLoader(temp_text_file)
        assert loader.file_path.exists()
        assert loader.file_type == "text"

    def test_init_with_nonexistent_file(self):
        """Test initialization with non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            FileLoader("nonexistent.txt")

    def test_init_with_unsupported_file(self):
        """Test initialization with unsupported file type."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            temp_path = f.name
        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                FileLoader(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_load_text_file(self, temp_text_file):
        """Test loading text file returns documents."""
        loader = FileLoader(temp_text_file)
        documents = loader.load()

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert hasattr(documents[0], "page_content")
        assert hasattr(documents[0], "metadata")
        assert "test document" in documents[0].page_content.lower()

    def test_load_csv_file(self, temp_csv_file):
        """Test loading CSV file."""
        loader = FileLoader(temp_csv_file)
        documents = loader.load()

        assert isinstance(documents, list)
        assert len(documents) > 0
        # CSV loader creates a document per row
        content = " ".join([doc.page_content for doc in documents])
        assert "Alice" in content or "name" in content

    @pytest.mark.skip(reason="JSONLoader requires optional jq dependency")
    def test_load_json_file(self, temp_json_file):
        """Test loading JSON file."""
        loader = FileLoader(temp_json_file)
        documents = loader.load()

        assert isinstance(documents, list)
        assert len(documents) > 0

    def test_load_markdown_file(self, temp_markdown_file):
        """Test loading Markdown file."""
        loader = FileLoader(temp_markdown_file)
        documents = loader.load()

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert "markdown" in documents[0].page_content.lower()


class TestLoadDocument:
    """Tests for load_document convenience function."""

    def test_load_document_function(self, temp_text_file):
        """Test load_document convenience function."""
        documents = load_document(temp_text_file)

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert "test document" in documents[0].page_content.lower()

    def test_load_document_with_path_object(self, temp_text_file):
        """Test load_document with Path object."""
        documents = load_document(Path(temp_text_file))

        assert isinstance(documents, list)
        assert len(documents) > 0

    def test_load_document_invalid_file(self):
        """Test load_document with invalid file raises error."""
        with pytest.raises(FileNotFoundError):
            load_document("nonexistent.txt")


class TestFileLoaderWithPDFMethods:
    """Tests for FileLoader with PDF loader method parameter."""

    def test_file_loader_accepts_pdf_loader_method(self):
        """FileLoader accepts pdf_loader_method parameter."""
        # This won't actually load since we don't have a real PDF, but should initialize
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            loader = FileLoader(temp_path, pdf_loader_method="pypdf")
            assert loader.pdf_loader_method == "pypdf"
            assert loader.file_type == "pdf"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_file_loader_default_pdf_method(self):
        """FileLoader defaults to pypdf for PDFs."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            loader = FileLoader(temp_path)
            assert loader.pdf_loader_method == "pypdf"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_file_loader_accepts_pdf_kwargs(self):
        """FileLoader accepts additional PDF loader kwargs."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            temp_path = f.name

        try:
            loader = FileLoader(
                temp_path, pdf_loader_method="amazon_textract", region_name="us-west-2"
            )
            assert loader.pdf_loader_method == "amazon_textract"
            assert "region_name" in loader.pdf_loader_kwargs
            assert loader.pdf_loader_kwargs["region_name"] == "us-west-2"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_load_document_accepts_pdf_loader_method(self):
        """load_document function accepts pdf_loader_method parameter."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"Test content")
            temp_path = f.name

        try:
            # For non-PDF files, the parameter should be accepted but not used
            documents = load_document(temp_path, pdf_loader_method="pypdf")
            assert isinstance(documents, list)
        finally:
            Path(temp_path).unlink(missing_ok=True)
