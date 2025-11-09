# Automated Document Parser

[![PyPI version](https://badge.fury.io/py/automated-document-parser.svg)](https://pypi.org/project/automated-document-parser/)
[![Python Version](https://img.shields.io/pypi/pyversions/automated-document-parser.svg)](https://pypi.org/project/automated-document-parser/)
[![CI](https://github.com/Pulkit12dhingra/automated-document-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/Pulkit12dhingra/automated-document-parser/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Pulkit12dhingra/automated-document-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/Pulkit12dhingra/automated-document-parser)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=YOUR_PROJECT&metric=security_rating)](https://sonarcloud.io/dashboard?id=YOUR_PROJECT)
[![GitHub issues](https://img.shields.io/github/issues/Pulkit12dhingra/automated-document-parser)](https://github.com/Pulkit12dhingra/automated-document-parser/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Pulkit12dhingra/automated-document-parser)](https://github.com/Pulkit12dhingra/automated-document-parser/pulls)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)



A powerful and automated document parser built with LangChain for intelligent document processing. This library automatically detects file types and uses the appropriate loader to parse documents into LangChain-compatible formats.

## Features

- **Automatic file type detection** based on file extensions
- **Multiple PDF loading methods** - 9 different PDF loaders for various use cases
- **Modular architecture** - Clean separation with `file_load/` and `pdf_load/` modules
- **Support for multiple document formats**: PDF, TXT, CSV, JSON, DOCX, HTML, Markdown
- Built on LangChain for seamless integration with RAG applications
- Type-safe implementation with comprehensive error handling
- Batch processing support for multiple documents

## Supported File Types

### Text Files
- `.txt` - Plain text files
- `.md` - Markdown files

### Structured Data
- `.csv` - CSV files with encoding support
- `.json` - JSON files with jq schema filtering

### Documents
- `.docx` - Microsoft Word documents
- `.html` - HTML files

### PDF Files (9 loading methods)
- `pypdf` - Basic PDF text extraction (default, no extra dependencies)
- `unstructured` - Advanced OCR and layout detection
- `amazon_textract` - AWS Textract for high-accuracy OCR
- `mathpix` - Specialized for mathematical formulas
- `pdfplumber` - High accuracy text and table extraction
- `pypdfium2` - Google PDFium library
- `pymupdf` - PyMuPDF (fitz) backend
- `pymupdf4llm` - LLM-optimized extraction
- `opendataloader` - Advanced multi-format parsing

## Installation

Install from PyPI:

```bash
pip install automated-document-parser
```

Or using uv:

```bash
uv add automated-document-parser
```

## Quick Start

### Basic Usage - Automatic File Type Detection

The primary feature is **automatic file type detection**. Just point to any supported file and the parser handles the rest:

```python
from automated_document_parser import DocumentParser

# Initialize the parser
parser = DocumentParser()

# Parse any single file - automatically detects type and uses the right loader
documents = parser.parse("document.pdf")        # Auto-detects PDF
documents = parser.parse("data.csv")            # Auto-detects CSV
documents = parser.parse("notes.txt")           # Auto-detects text file

# Parse multiple files of different types - all formats handled automatically
file_paths = ["report.pdf", "data.csv", "notes.txt", "info.docx"]
all_docs = parser.parse_multiple(file_paths)  # Each file auto-detected and loaded

# Access parsed content
for file_path, docs in all_docs.items():
    print(f"File: {file_path}")
    for doc in docs:
        print(f"  Content: {doc.page_content[:100]}...")
        print(f"  Metadata: {doc.metadata}")
```

### Specify Loading Methods

Specify the PDF loading method and other parameters to apply to all files:

```python
from automated_document_parser import DocumentParser

parser = DocumentParser()

# Step 1: Specify the method for PDFs
# Step 2: Parser automatically detects file types and loads them with specified method
file_paths = ["report1.pdf", "report2.pdf", "data.csv", "notes.txt"]
all_docs = parser.parse_multiple(
    file_paths,
    pdf_loader_method="pdfplumber",  # All PDFs will use pdfplumber
    encoding="utf-8"                  # All text files will use UTF-8 encoding
)

# Each file is automatically detected and loaded with the specified settings
for file_path, docs in all_docs.items():
    print(f"Loaded {file_path}: {len(docs)} documents")
```

## Documentation

Full documentation is available at: https://pulkit12dhingra.github.io/automated-document-parser/

## Architecture

The library uses a modular architecture:

```
automated_document_parser/
├── loaders/
│   ├── file_load/          # File loaders module
│   │   ├── base.py         # Base file loader class
│   │   ├── text_loader.py  # Text file loader
│   │   ├── csv_loader.py   # CSV loader
│   │   ├── json_loader.py  # JSON loader
│   │   ├── docx_loader.py  # DOCX loader
│   │   └── html_loader.py  # HTML loader
│   ├── pdf_load/           # PDF loaders module
│   │   ├── base.py         # Base PDF loader class
│   │   ├── pypdf_loader.py
│   │   ├── mathpix_loader.py
│   │   ├── pdfplumber_loader.py
│   │   └── ... (9 PDF loaders total)
│   └── file_loaders.py     # Main orchestrator
└── core.py                 # DocumentParser class
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.