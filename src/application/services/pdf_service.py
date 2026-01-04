"""
PDF Service
===========

Servicio de aplicación que actúa como fachada para las operaciones PDF.

Los servicios de aplicación:
- Coordinan múltiples casos de uso si es necesario
- Proporcionan una API simplificada para la capa de presentación
- Pueden manejar transacciones y logging
- No contienen lógica de negocio (eso está en el dominio)

En este caso, el servicio es simple porque solo tenemos un caso de uso,
pero en aplicaciones más complejas podría coordinar múltiples operaciones.
"""

from typing import BinaryIO

from src.domain.interfaces import IPDFGenerator
from src.domain.value_objects import PDFStyle, ColorConfig, FontConfig, MarginConfig
from src.application.dto import PDFRequestDTO, PDFStyleDTO
from src.application.use_cases import GeneratePDFUseCase


class PDFService:
    """
    Servicio de aplicación para operaciones de PDF.
    
    Este servicio actúa como punto de entrada único para todas
    las operaciones relacionadas con PDFs. Coordina los casos
    de uso y maneja la conversión de DTOs.
    
    Ejemplo:
        >>> generator = ReportLabGenerator()
        >>> service = PDFService(generator)
        >>> result = service.generate_pdf(request_dto)
    """
    
    def __init__(self, pdf_generator: IPDFGenerator) -> None:
        """
        Inicializa el servicio.
        
        Args:
            pdf_generator: Implementación del generador de PDF
        """
        self._generator = pdf_generator
        self._generate_use_case = GeneratePDFUseCase(pdf_generator)
    
    def generate_pdf(
        self,
        request: PDFRequestDTO,
    ) -> tuple[bytes, str, str]:
        """
        Genera un PDF a partir de un request.
        
        Args:
            request: DTO con los datos del PDF
            
        Returns:
            Tupla (contenido_bytes, nombre_archivo, document_id)
        """
        # Convertir el style DTO a value object del dominio
        style = self._convert_style(request.style) if request.style else None
        
        # Ejecutar el caso de uso
        result = self._generate_use_case.execute(request, style)
        
        return result.content, result.filename, result.document_id
    
    def generate_pdf_to_stream(
        self,
        request: PDFRequestDTO,
        stream: BinaryIO,
    ) -> str:
        """
        Genera un PDF directamente a un stream.
        
        Args:
            request: DTO con los datos del PDF
            stream: Stream binario para escribir el PDF
            
        Returns:
            ID del documento generado
        """
        style = self._convert_style(request.style) if request.style else None
        return self._generate_use_case.execute_to_stream(request, stream, style)
    
    def _convert_style(self, style_dto: PDFStyleDTO) -> PDFStyle:
        """
        Convierte un StyleDTO a un PDFStyle value object.
        
        Este método mapea los valores simples del DTO
        a los value objects complejos del dominio.
        """
        # Construir configuración de colores
        color_kwargs = {}
        if style_dto.primary_color:
            color_kwargs["primary"] = style_dto.primary_color
        if style_dto.text_color:
            color_kwargs["text"] = style_dto.text_color
        
        colors = ColorConfig(**color_kwargs) if color_kwargs else ColorConfig()
        
        # Construir configuración de fuentes
        font_kwargs = {}
        if style_dto.font_size:
            font_kwargs["size_body"] = style_dto.font_size
        
        fonts = FontConfig(**font_kwargs) if font_kwargs else FontConfig()
        
        # Construir configuración de márgenes
        margin_kwargs = {}
        if style_dto.margin_top is not None:
            margin_kwargs["top"] = style_dto.margin_top
        if style_dto.margin_bottom is not None:
            margin_kwargs["bottom"] = style_dto.margin_bottom
        if style_dto.margin_left is not None:
            margin_kwargs["left"] = style_dto.margin_left
        if style_dto.margin_right is not None:
            margin_kwargs["right"] = style_dto.margin_right
        
        margins = MarginConfig(**margin_kwargs) if margin_kwargs else MarginConfig()
        
        return PDFStyle(colors=colors, fonts=fonts, margins=margins)
