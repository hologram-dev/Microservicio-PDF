"""
Pytest Configuration
====================

Fixtures y configuración compartida para tests.
"""

import pytest
from io import BytesIO

from src.domain.entities import PDFDocument, PDFSection, PDFTable
from src.domain.value_objects import PDFStyle
from src.domain.interfaces import IPDFGenerator
from src.application.dto import PDFRequestDTO, PDFSectionDTO, PDFTableDTO


# ================================
# Domain Fixtures
# ================================

@pytest.fixture
def sample_document() -> PDFDocument:
    """Documento de ejemplo para tests."""
    doc = PDFDocument(
        title="Test Document",
        author="Test Author",
    )
    doc.add_section(PDFSection(
        title="Introduction",
        content="This is a test document.",
    ))
    return doc


@pytest.fixture
def sample_style() -> PDFStyle:
    """Estilo de ejemplo para tests."""
    return PDFStyle.default()


@pytest.fixture
def sample_table() -> PDFTable:
    """Tabla de ejemplo para tests."""
    return PDFTable(
        headers=["Name", "Value"],
        rows=[
            ["Item 1", "100"],
            ["Item 2", "200"],
        ],
        title="Sample Table",
    )


# ================================
# Application Fixtures
# ================================

@pytest.fixture
def sample_request_dto() -> PDFRequestDTO:
    """DTO de request de ejemplo."""
    return PDFRequestDTO(
        title="Test Report",
        sections=[
            PDFSectionDTO(
                title="Summary",
                content="This is the summary section.",
            ),
            PDFSectionDTO(
                title="Data",
                tables=[
                    PDFTableDTO(
                        headers=["Column A", "Column B"],
                        rows=[["1", "2"], ["3", "4"]],
                    )
                ],
            ),
        ],
        author="Test System",
    )


# ================================
# Mock Generator
# ================================

class MockPDFGenerator(IPDFGenerator):
    """
    Mock del generador de PDF para tests.
    
    Implementa la interfaz pero no genera PDFs reales.
    """
    
    def __init__(self):
        self.generate_called = False
        self.last_document = None
        self.last_style = None
    
    def generate(self, document: PDFDocument, style: PDFStyle | None = None) -> bytes:
        self.generate_called = True
        self.last_document = document
        self.last_style = style
        return b"%PDF-1.4 mock content"
    
    def generate_to_file(
        self,
        document: PDFDocument,
        output_path: str,
        style: PDFStyle | None = None,
    ) -> str:
        self.generate_called = True
        self.last_document = document
        return output_path
    
    def generate_to_stream(
        self,
        document: PDFDocument,
        stream,
        style: PDFStyle | None = None,
    ) -> None:
        self.generate_called = True
        self.last_document = document
        stream.write(b"%PDF-1.4 mock content")


@pytest.fixture
def mock_generator() -> MockPDFGenerator:
    """Mock del generador para tests."""
    return MockPDFGenerator()
