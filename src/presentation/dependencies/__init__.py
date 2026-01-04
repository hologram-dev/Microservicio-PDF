# ================================
# Presentation Dependencies
# ================================
# Inyección de dependencias para FastAPI.
# ================================

from .container import get_pdf_service, get_pdf_generator

__all__ = ["get_pdf_service", "get_pdf_generator"]
