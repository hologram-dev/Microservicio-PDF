# ================================
# Domain Entities
# ================================
# Entidades: objetos con identidad única que persisten en el tiempo.
# Ejemplo: un PDFDocument tiene un ID único.
# ================================

from .pdf_document import PDFDocument, PDFSection, PDFTable

__all__ = ["PDFDocument", "PDFSection", "PDFTable"]
