"""Example usage of automated document parser."""


def main():
    """Demonstrate basic usage of DocumentParser."""
    # Example: Create a parser instance and parse a document
    # parser = DocumentParser()
    # documents = parser.parse("path/to/your/document.pdf")
    # for doc in documents:
    #     print(doc.page_content)
    #     print(doc.metadata)

    print("Automated Document Parser")
    print("=========================")
    print()
    print("Supported file formats:")
    print("- PDF (.pdf)")
    print("- Text (.txt, .md)")
    print("- CSV (.csv)")
    print("- JSON (.json)")
    print("- Word (.docx, .doc)")
    print("- HTML (.html, .htm)")
    print()
    print("Usage:")
    print("  from automated_document_parser import DocumentParser")
    print("  parser = DocumentParser()")
    print("  documents = parser.parse('document.pdf')")
    print()
    print("Ready for LangChain RAG pipelines!")


if __name__ == "__main__":
    main()
