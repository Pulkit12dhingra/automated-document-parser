"""Test core DocumentParser class."""

import tempfile
from pathlib import Path

import pytest

from automated_document_parser import DocumentParser


@pytest.fixture
def temp_text_file():
    """Create a temporary text file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Sample text content for testing.")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("col1,col2\n")
        f.write("val1,val2\n")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def parser():
    """Create a DocumentParser instance."""
    return DocumentParser()


class TestDocumentParser:
    """Tests for DocumentParser class."""

    def test_parser_initialization(self, parser):
        """Test DocumentParser initializes correctly."""
        assert isinstance(parser, DocumentParser)
        assert parser.loaded_files == []

    def test_parse_text_file(self, parser, temp_text_file):
        """Test parsing a text file."""
        documents = parser.parse(temp_text_file)

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert "sample text" in documents[0].page_content.lower()

    def test_parse_adds_metadata(self, parser, temp_text_file):
        """Test that parsing adds file metadata to documents."""
        documents = parser.parse(temp_text_file)

        metadata = documents[0].metadata
        assert "source" in metadata
        assert "file_name" in metadata
        assert "file_type" in metadata
        assert metadata["file_type"] == ".txt"

    def test_parse_tracks_loaded_files(self, parser, temp_text_file):
        """Test that parser tracks loaded files."""
        parser.parse(temp_text_file)

        loaded = parser.get_loaded_files()
        assert len(loaded) == 1
        assert str(Path(temp_text_file).resolve()) in loaded[0]

    def test_parse_unsupported_file(self, parser):
        """Test parsing unsupported file type raises error."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            temp_path = f.name
        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                parser.parse(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_parse_nonexistent_file(self, parser):
        """Test parsing non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            parser.parse("nonexistent.txt")

    def test_parse_multiple_files(self, parser, temp_text_file, temp_csv_file):
        """Test parsing multiple files."""
        results = parser.parse_multiple([temp_text_file, temp_csv_file])

        assert isinstance(results, dict)
        assert len(results) == 2
        assert str(temp_text_file) in results
        assert str(temp_csv_file) in results
        assert len(results[str(temp_text_file)]) > 0
        assert len(results[str(temp_csv_file)]) > 0

    def test_parse_multiple_with_invalid_file(self, parser, temp_text_file):
        """Test parse_multiple continues on error."""
        results = parser.parse_multiple([temp_text_file, "nonexistent.txt"])

        assert len(results) == 2
        assert len(results[str(temp_text_file)]) > 0
        assert len(results["nonexistent.txt"]) == 0

    def test_get_loaded_files_returns_copy(self, parser, temp_text_file):
        """Test that get_loaded_files returns a copy."""
        parser.parse(temp_text_file)
        loaded1 = parser.get_loaded_files()
        loaded2 = parser.get_loaded_files()

        assert loaded1 == loaded2
        assert loaded1 is not loaded2

    def test_parse_with_path_object(self, parser, temp_text_file):
        """Test parsing works with Path objects."""
        documents = parser.parse(Path(temp_text_file))

        assert isinstance(documents, list)
        assert len(documents) > 0
