# ================================
# Application DTOs
# ================================
# Data Transfer Objects: objetos para transferir datos
# entre capas de la aplicación.
#
# Los DTOs son diferentes de las entidades:
# - No tienen comportamiento ni reglas de negocio
# - Son simples contenedores de datos
# - Pueden ser validados con Pydantic en la capa de presentación
# ================================

from .pdf_request_dto import (
    PDFRequestDTO,
    PDFSectionDTO,
    PDFTableDTO,
    PDFStyleDTO,
)

__all__ = [
    "PDFRequestDTO",
    "PDFSectionDTO",
    "PDFTableDTO",
    "PDFStyleDTO",
]
