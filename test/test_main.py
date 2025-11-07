"""Test main module and package imports."""

from automated_document_parser import DocumentParser, FileLoader, load_document


def test_package_imports():
    """Test that main package exports are available."""
    assert DocumentParser is not None
    assert FileLoader is not None
    assert load_document is not None


def test_document_parser_class_available():
    """Test that DocumentParser class can be instantiated."""
    parser = DocumentParser()
    assert parser is not None


def test_version_attribute():
    """Test that package has version attribute."""
    import automated_document_parser

    assert hasattr(automated_document_parser, "__version__")
    assert isinstance(automated_document_parser.__version__, str)
