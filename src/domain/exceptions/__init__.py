# ================================
# Domain Exceptions
# ================================
# Excepciones específicas del dominio.
# Estas excepciones representan violaciones de reglas de negocio.
# ================================

from .domain_exceptions import (
    DomainException,
    PDFGenerationError,
    InvalidDocumentError,
    InvalidStyleError,
    DocumentNotFoundError,
)

__all__ = [
    "DomainException",
    "PDFGenerationError",
    "InvalidDocumentError",
    "InvalidStyleError",
    "DocumentNotFoundError",
]
