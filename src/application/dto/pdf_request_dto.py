"""
PDF Request DTOs
================

Data Transfer Objects para requests de generación de PDF.

Los DTOs en Clean Architecture:
- Transportan datos entre capas
- No contienen lógica de negocio
- Son diferentes de las entidades del dominio
- Pueden ser mapeados a/desde entidades

Decisiones técnicas:
- Se usan dataclasses simples (no Pydantic) para independencia del framework
- La validación con Pydantic se hace en la capa de presentación
- Los DTOs se mapean a entidades en los casos de uso
"""

from dataclasses import dataclass, field
from typing import Any

from src.domain.entities.pdf_document import PageSize, PageOrientation


@dataclass
class PDFTableDTO:
    """
    DTO para una tabla en el PDF.
    
    Atributos:
        headers: Encabezados de la tabla
        rows: Filas de datos
        title: Título opcional de la tabla
    """
    headers: list[str]
    rows: list[list[str]]
    title: str | None = None


@dataclass
class PDFSectionDTO:
    """
    DTO para una sección del documento.
    
    Atributos:
        title: Título de la sección
        content: Contenido de texto
        level: Nivel de encabezado (1-6)
        tables: Tablas dentro de la sección
    """
    title: str
    content: str | None = None
    level: int = 1
    tables: list[PDFTableDTO] = field(default_factory=list)


@dataclass
class PDFStyleDTO:
    """
    DTO para estilos del PDF.
    
    Este DTO permite especificar estilos de forma simple,
    que luego se mapean a los value objects del dominio.
    
    Atributos:
        primary_color: Color primario (hex)
        text_color: Color del texto (hex)
        font_family: Familia de fuente
        font_size: Tamaño base de fuente
        margin_top: Margen superior (puntos)
        margin_bottom: Margen inferior (puntos)
        margin_left: Margen izquierdo (puntos)
        margin_right: Margen derecho (puntos)
    """
    primary_color: str | None = None
    text_color: str | None = None
    font_family: str | None = None
    font_size: float | None = None
    margin_top: float | None = None
    margin_bottom: float | None = None
    margin_left: float | None = None
    margin_right: float | None = None


@dataclass
class PDFRequestDTO:
    """
    DTO principal para solicitar generación de PDF.
    
    Este es el objeto que recibe el caso de uso.
    Contiene toda la información necesaria para generar un PDF.
    
    Atributos:
        title: Título del documento (requerido)
        sections: Lista de secciones (requerido, al menos una)
        author: Autor del documento
        page_size: Tamaño de página
        orientation: Orientación de la página
        style: Estilos opcionales
        metadata: Metadatos adicionales
    
    Ejemplo:
        >>> dto = PDFRequestDTO(
        ...     title="Reporte Mensual",
        ...     sections=[
        ...         PDFSectionDTO(title="Resumen", content="..."),
        ...         PDFSectionDTO(title="Datos", tables=[table_dto]),
        ...     ],
        ...     author="Sistema de Reportes",
        ... )
    """
    title: str
    sections: list[PDFSectionDTO]
    author: str | None = None
    page_size: PageSize = PageSize.A4
    orientation: PageOrientation = PageOrientation.PORTRAIT
    style: PDFStyleDTO | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
