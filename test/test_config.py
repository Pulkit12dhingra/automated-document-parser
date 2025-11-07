"""Test configuration module."""

from automated_document_parser.config import (
    DEFAULT_ENCODING,
    FILE_EXTENSION_MAPPING,
    LOADER_CONFIG,
    SUPPORTED_EXTENSIONS,
)


def test_file_extension_mapping_exists():
    """Test that file extension mapping is defined."""
    assert isinstance(FILE_EXTENSION_MAPPING, dict)
    assert len(FILE_EXTENSION_MAPPING) > 0


def test_supported_extensions_matches_mapping():
    """Test that supported extensions list matches mapping keys."""
    assert set(SUPPORTED_EXTENSIONS) == set(FILE_EXTENSION_MAPPING.keys())


def test_common_extensions_supported():
    """Test that common file extensions are supported."""
    common_extensions = [".txt", ".pdf", ".csv", ".json", ".docx", ".html", ".md"]
    for ext in common_extensions:
        assert ext in SUPPORTED_EXTENSIONS


def test_loader_config_structure():
    """Test that loader config has expected structure."""
    assert isinstance(LOADER_CONFIG, dict)
    assert "text" in LOADER_CONFIG
    assert "pdf" in LOADER_CONFIG
    assert "csv" in LOADER_CONFIG


def test_default_encoding():
    """Test that default encoding is defined."""
    assert DEFAULT_ENCODING == "utf-8"
