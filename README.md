# Automated Document Parser

[![PyPI version](https://badge.fury.io/py/automated-document-parser.svg)](https://pypi.org/project/automated-document-parser/)
[![Python Version](https://img.shields.io/pypi/pyversions/automated-document-parser.svg)](https://pypi.org/project/automated-document-parser/)
[![CI](https://github.com/Pulkit12dhingra/automated-document-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/Pulkit12dhingra/automated-document-parser/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Pulkit12dhingra/automated-document-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/Pulkit12dhingra/automated-document-parser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A powerful and automated document parser built with LangChain for intelligent document processing. This library automatically detects file types and uses the appropriate loader to parse documents into LangChain-compatible formats.

## Features

- **Automatic file type detection** based on file extensions
- **Support for multiple document formats**: PDF, TXT, CSV, JSON, DOCX, HTML, Markdown
- Built on LangChain for seamless integration with RAG applications
- Type-safe implementation with comprehensive error handling
- Batch processing support for multiple documents

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

### Basic Usage

```python
from automated_document_parser import DocumentParser

# Initialize the parser
parser = DocumentParser()

# Parse a single document
documents = parser.parse("path/to/document.pdf")

# Parse multiple documents
file_paths = ["doc1.pdf", "doc2.txt", "data.csv"]
parsed_docs = parser.parse_multiple(file_paths)
```

### Working with Parsed Documents

```python
# Access document content and metadata
for doc in documents:
    print(f"Content: {doc.page_content}")
    print(f"Source: {doc.metadata['source']}")
    print(f"Type: {doc.metadata['file_type']}")
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.