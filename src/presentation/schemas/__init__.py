# ================================
# Presentation Schemas
# ================================
# Schemas Pydantic para validación de requests y responses.
# Estos schemas son diferentes de los DTOs de aplicación.
# ================================

from .pdf_schemas import (
    PDFGenerateRequest,
    PDFGenerateResponse,
    PDFSectionSchema,
    PDFTableSchema,
    PDFStyleSchema,
    ErrorResponse,
)

__all__ = [
    "PDFGenerateRequest",
    "PDFGenerateResponse",
    "PDFSectionSchema",
    "PDFTableSchema",
    "PDFStyleSchema",
    "ErrorResponse",
]
