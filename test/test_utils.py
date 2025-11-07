"""Test utility functions."""

import tempfile
from pathlib import Path

import pytest

from automated_document_parser.utils import (
    detect_file_type,
    get_file_info,
    is_supported_file,
    validate_file_path,
)


@pytest.fixture
def temp_text_file():
    """Create a temporary text file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_pdf_file():
    """Create a temporary PDF file."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as f:
        # Minimal PDF header
        f.write(b"%PDF-1.4\n")
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


class TestDetectFileType:
    """Tests for detect_file_type function."""

    def test_detect_text_file(self, temp_text_file):
        """Test detection of text file."""
        file_type = detect_file_type(temp_text_file)
        assert file_type == "text"

    def test_detect_pdf_file(self, temp_pdf_file):
        """Test detection of PDF file."""
        file_type = detect_file_type(temp_pdf_file)
        assert file_type == "pdf"

    def test_detect_nonexistent_file(self):
        """Test detection raises error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            detect_file_type("nonexistent.txt")

    def test_detect_unsupported_extension(self, temp_text_file):
        """Test detection of unsupported file type."""
        # Rename to unsupported extension
        unsupported = Path(temp_text_file).with_suffix(".xyz")
        Path(temp_text_file).rename(unsupported)
        try:
            result = detect_file_type(unsupported)
            assert result is None
        finally:
            unsupported.unlink(missing_ok=True)


class TestIsSupportedFile:
    """Tests for is_supported_file function."""

    def test_supported_extensions(self):
        """Test that common extensions are recognized as supported."""
        supported = [".txt", ".pdf", ".csv", ".json", ".docx", ".html"]
        for ext in supported:
            # Use a fake path - just checking extension
            assert is_supported_file(f"file{ext}") is True

    def test_unsupported_extension(self):
        """Test that unsupported extensions return False."""
        assert is_supported_file("file.xyz") is False

    def test_case_insensitive(self):
        """Test that extension check is case-insensitive."""
        assert is_supported_file("file.PDF") is True
        assert is_supported_file("file.TXT") is True


class TestValidateFilePath:
    """Tests for validate_file_path function."""

    def test_validate_existing_file(self, temp_text_file):
        """Test validation of existing file."""
        path = validate_file_path(temp_text_file)
        assert isinstance(path, Path)
        assert path.exists()
        assert path.is_file()

    def test_validate_nonexistent_file(self):
        """Test validation raises error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            validate_file_path("nonexistent.txt")

    def test_validate_directory(self, tmp_path):
        """Test validation raises error for directory."""
        with pytest.raises(ValueError, match="not a file"):
            validate_file_path(tmp_path)


class TestGetFileInfo:
    """Tests for get_file_info function."""

    def test_get_file_info(self, temp_text_file):
        """Test getting file information."""
        info = get_file_info(temp_text_file)

        assert isinstance(info, dict)
        assert "name" in info
        assert "extension" in info
        assert "size_bytes" in info
        assert "absolute_path" in info

        assert info["extension"] == ".txt"
        assert info["size_bytes"] > 0
        assert Path(info["absolute_path"]).exists()

    def test_file_info_has_correct_name(self, temp_text_file):
        """Test that file info contains correct file name."""
        info = get_file_info(temp_text_file)
        expected_name = Path(temp_text_file).name
        assert info["name"] == expected_name
