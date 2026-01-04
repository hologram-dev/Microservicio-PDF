"""
Dependency Injection Container
==============================

Contenedor de inyección de dependencias para FastAPI.

La inyección de dependencias en Clean Architecture:
- Conecta las implementaciones concretas con las interfaces
- Permite cambiar implementaciones sin modificar el código
- Facilita el testing con mocks

FastAPI usa el sistema Depends() para inyección de dependencias.
Este archivo define las funciones que crean las dependencias.

Ejemplo de uso en un endpoint:
    @router.post("/generate")
    async def generate_pdf(
        request: PDFGenerateRequest,
        service: PDFService = Depends(get_pdf_service)
    ):
        return service.generate_pdf(...)
"""

from functools import lru_cache

from src.domain.interfaces import IPDFGenerator
from src.infrastructure.pdf import ReportLabGenerator
from src.application.services import PDFService


@lru_cache
def get_pdf_generator() -> IPDFGenerator:
    """
    Obtiene la instancia del generador de PDF.
    
    Usa lru_cache para crear un singleton.
    Aquí es donde se decide qué implementación usar.
    
    Returns:
        Implementación de IPDFGenerator
    """
    return ReportLabGenerator()


@lru_cache
def get_pdf_service() -> PDFService:
    """
    Obtiene la instancia del servicio de PDF.
    
    Construye el grafo de dependencias:
    - PDFService depende de IPDFGenerator
    - Usamos ReportLabGenerator como implementación
    
    Returns:
        Instancia de PDFService
    """
    generator = get_pdf_generator()
    return PDFService(generator)


# ================================
# Ejemplo de cómo intercambiar implementaciones
# ================================
#
# Para testing:
# def get_mock_generator() -> IPDFGenerator:
#     return MockPDFGenerator()
#
# Para producción con otro generador:
# def get_pdf_generator() -> IPDFGenerator:
#     if settings.pdf_backend == "weasyprint":
#         return WeasyPrintGenerator()
#     return ReportLabGenerator()
# ================================
