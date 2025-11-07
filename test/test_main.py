"""Sample test file for main module."""

import pytest
from main import main


def test_main_runs_successfully(capsys):
    """Test that main function runs without errors."""
    main()
    captured = capsys.readouterr()
    assert "Hello from document-parser!" in captured.out


def test_main_output_format(capsys):
    """Test that main function produces expected output format."""
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello from document-parser!"


@pytest.mark.parametrize(
    "expected_substring",
    [
        "Hello",
        "document-parser",
    ],
)
def test_main_contains_keywords(capsys, expected_substring):
    """Test that main output contains expected keywords."""
    main()
    captured = capsys.readouterr()
    assert expected_substring in captured.out
