# ================================
# Application Services
# ================================
# Servicios de aplicación: coordinan múltiples casos de uso
# y proporcionan una fachada para la capa de presentación.
# ================================

from .pdf_service import PDFService

__all__ = ["PDFService"]
