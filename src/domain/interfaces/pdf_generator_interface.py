"""
PDF Generator Interface (Port)
==============================

Define el contrato para generadores de PDF.

En Clean Architecture, las interfaces del dominio definen los "Ports":
- El dominio declara QUÉ necesita, no CÓMO se implementa
- La infraestructura proporciona los "Adapters" que implementan estos ports
- Esto permite intercambiar implementaciones sin tocar el dominio

Ejemplo de flujo:
    1. Domain define: IPDFGenerator.generate(document) -> bytes
    2. Infrastructure implementa: ReportLabGenerator(IPDFGenerator)
    3. Application usa: generator.generate(document)

Beneficios:
- Testability: podemos mockear el generador en tests
- Flexibilidad: podemos cambiar de ReportLab a otra librería
- Separación de concerns: el dominio no conoce ReportLab
"""

from abc import ABC, abstractmethod
from typing import BinaryIO

from src.domain.entities import PDFDocument
from src.domain.value_objects import PDFStyle


class IPDFGenerator(ABC):
    """
    Interfaz abstracta para generadores de PDF.
    
    Esta interfaz define el contrato que cualquier generador de PDF
    debe cumplir. La implementación concreta (ReportLab, WeasyPrint, etc.)
    vive en la capa de infraestructura.
    
    Métodos:
        generate: Genera un PDF a partir de un documento
        generate_to_file: Genera un PDF y lo guarda en un archivo
        generate_to_stream: Genera un PDF y lo escribe en un stream
    
    Ejemplo de implementación:
        >>> class ReportLabGenerator(IPDFGenerator):
        ...     def generate(self, document: PDFDocument, style: PDFStyle) -> bytes:
        ...         # Implementación con ReportLab
        ...         ...
    """
    
    @abstractmethod
    def generate(
        self, 
        document: PDFDocument, 
        style: PDFStyle | None = None
    ) -> bytes:
        """
        Genera un PDF a partir de un documento.
        
        Args:
            document: El documento a convertir en PDF
            style: Estilos opcionales para el PDF
            
        Returns:
            bytes: El contenido del PDF como bytes
            
        Raises:
            PDFGenerationError: Si hay un error al generar el PDF
        """
        pass
    
    @abstractmethod
    def generate_to_file(
        self,
        document: PDFDocument,
        output_path: str,
        style: PDFStyle | None = None,
    ) -> str:
        """
        Genera un PDF y lo guarda en un archivo.
        
        Args:
            document: El documento a convertir en PDF
            output_path: Ruta donde guardar el archivo
            style: Estilos opcionales para el PDF
            
        Returns:
            str: La ruta del archivo generado
            
        Raises:
            PDFGenerationError: Si hay un error al generar el PDF
        """
        pass
    
    @abstractmethod
    def generate_to_stream(
        self,
        document: PDFDocument,
        stream: BinaryIO,
        style: PDFStyle | None = None,
    ) -> None:
        """
        Genera un PDF y lo escribe en un stream.
        
        Útil para streaming responses en FastAPI.
        
        Args:
            document: El documento a convertir en PDF
            stream: Stream binario donde escribir el PDF
            style: Estilos opcionales para el PDF
            
        Raises:
            PDFGenerationError: Si hay un error al generar el PDF
        """
        pass
