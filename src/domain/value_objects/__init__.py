# ================================
# Domain Value Objects
# ================================
# Value Objects: objetos inmutables definidos por sus atributos.
# No tienen identidad única - dos value objects con los mismos
# valores son considerados iguales.
# ================================

from .pdf_style import PDFStyle, FontConfig, ColorConfig, MarginConfig

__all__ = ["PDFStyle", "FontConfig", "ColorConfig", "MarginConfig"]
