# ================================
# Domain Interfaces (Ports)
# ================================
# Interfaces que definen los contratos (Ports) del dominio.
# La infraestructura implementa estos contratos (Adapters).
# Esto logra la inversión de dependencias.
# ================================

from .pdf_generator_interface import IPDFGenerator

__all__ = ["IPDFGenerator"]
