"""
PDF Style Value Objects
=======================

Value Objects para configuración de estilos del PDF.

Un Value Object en Clean Architecture:
- Es inmutable (frozen=True en dataclass)
- Se define por sus atributos, no por identidad
- Dos value objects con mismos valores son iguales
- Encapsula validación de sus propios datos

Decisiones técnicas:
- Se usa frozen=True para inmutabilidad
- Los colores se validan en formato hexadecimal
- Los márgenes usan puntos (1 punto = 1/72 pulgadas)
"""

from dataclasses import dataclass
from enum import Enum
import re


class FontFamily(str, Enum):
    """Familias de fuentes disponibles en ReportLab."""
    HELVETICA = "Helvetica"
    TIMES = "Times-Roman"
    COURIER = "Courier"


@dataclass(frozen=True)
class ColorConfig:
    """
    Value Object para configuración de colores.
    
    Los colores se definen en formato hexadecimal (#RRGGBB).
    Este objeto es inmutable - para cambiar un color,
    se debe crear un nuevo ColorConfig.
    
    Atributos:
        primary: Color primario (encabezados, títulos)
        secondary: Color secundario (subtítulos)
        text: Color del texto principal
        background: Color de fondo
        accent: Color de acento (links, destacados)
    
    Ejemplo:
        >>> colors = ColorConfig(primary="#1a73e8", text="#333333")
    """
    
    primary: str = "#1a73e8"
    secondary: str = "#5f6368"
    text: str = "#202124"
    background: str = "#ffffff"
    accent: str = "#1967d2"
    
    def __post_init__(self) -> None:
        """Valida que todos los colores estén en formato hexadecimal."""
        hex_pattern = re.compile(r"^#[0-9A-Fa-f]{6}$")
        
        for field_name in ["primary", "secondary", "text", "background", "accent"]:
            value = getattr(self, field_name)
            if not hex_pattern.match(value):
                raise ValueError(
                    f"Color '{field_name}' inválido: '{value}'. "
                    f"Debe estar en formato #RRGGBB"
                )
    
    def to_rgb(self, color_name: str) -> tuple[float, float, float]:
        """
        Convierte un color hex a tupla RGB normalizada (0-1).
        
        Args:
            color_name: Nombre del atributo de color
            
        Returns:
            Tupla (R, G, B) con valores entre 0 y 1
        """
        hex_color = getattr(self, color_name)
        hex_color = hex_color.lstrip("#")
        
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        
        return (r, g, b)


@dataclass(frozen=True)
class FontConfig:
    """
    Value Object para configuración de fuentes.
    
    Atributos:
        family: Familia de fuente
        size_title: Tamaño para títulos (puntos)
        size_heading: Tamaño para encabezados (puntos)
        size_body: Tamaño para texto normal (puntos)
        size_small: Tamaño para texto pequeño (puntos)
        line_height: Altura de línea (multiplicador)
    
    Ejemplo:
        >>> fonts = FontConfig(family=FontFamily.HELVETICA, size_body=11)
    """
    
    family: FontFamily = FontFamily.HELVETICA
    size_title: float = 24.0
    size_heading: float = 16.0
    size_body: float = 10.0
    size_small: float = 8.0
    line_height: float = 1.2
    
    def __post_init__(self) -> None:
        """Valida los tamaños de fuente."""
        sizes = {
            "size_title": self.size_title,
            "size_heading": self.size_heading,
            "size_body": self.size_body,
            "size_small": self.size_small,
        }
        
        for name, size in sizes.items():
            if size <= 0:
                raise ValueError(f"El tamaño de fuente '{name}' debe ser positivo")
            if size > 72:
                raise ValueError(f"El tamaño de fuente '{name}' no puede exceder 72pt")
        
        if self.line_height < 1.0 or self.line_height > 3.0:
            raise ValueError("line_height debe estar entre 1.0 y 3.0")


@dataclass(frozen=True)
class MarginConfig:
    """
    Value Object para configuración de márgenes.
    
    Los márgenes se especifican en puntos (1 pulgada = 72 puntos).
    
    Atributos:
        top: Margen superior
        bottom: Margen inferior
        left: Margen izquierdo
        right: Margen derecho
    
    Constantes útiles:
        - 72 puntos = 1 pulgada
        - 28.35 puntos = 1 cm
    
    Ejemplo:
        >>> margins = MarginConfig(top=72, bottom=72, left=54, right=54)
    """
    
    top: float = 72.0      # 1 pulgada
    bottom: float = 72.0   # 1 pulgada
    left: float = 72.0     # 1 pulgada
    right: float = 72.0    # 1 pulgada
    
    def __post_init__(self) -> None:
        """Valida que los márgenes sean positivos."""
        for margin_name in ["top", "bottom", "left", "right"]:
            value = getattr(self, margin_name)
            if value < 0:
                raise ValueError(f"El margen '{margin_name}' no puede ser negativo")
            if value > 300:  # ~10 cm, máximo razonable
                raise ValueError(f"El margen '{margin_name}' excede el máximo permitido")
    
    @classmethod
    def from_inches(
        cls, 
        top: float = 1.0, 
        bottom: float = 1.0, 
        left: float = 1.0, 
        right: float = 1.0
    ) -> "MarginConfig":
        """
        Crea márgenes a partir de pulgadas.
        
        Args:
            top: Margen superior en pulgadas
            bottom: Margen inferior en pulgadas
            left: Margen izquierdo en pulgadas
            right: Margen derecho en pulgadas
        """
        return cls(
            top=top * 72,
            bottom=bottom * 72,
            left=left * 72,
            right=right * 72,
        )
    
    @classmethod
    def from_cm(
        cls, 
        top: float = 2.54, 
        bottom: float = 2.54, 
        left: float = 2.54, 
        right: float = 2.54
    ) -> "MarginConfig":
        """
        Crea márgenes a partir de centímetros.
        
        Args:
            top: Margen superior en cm
            bottom: Margen inferior en cm
            left: Margen izquierdo en cm
            right: Margen derecho en cm
        """
        return cls(
            top=top * 28.35,
            bottom=bottom * 28.35,
            left=left * 28.35,
            right=right * 28.35,
        )


@dataclass(frozen=True)
class PDFStyle:
    """
    Value Object principal que agrupa toda la configuración de estilo.
    
    Combina colores, fuentes y márgenes en un solo objeto inmutable.
    
    Atributos:
        colors: Configuración de colores
        fonts: Configuración de fuentes
        margins: Configuración de márgenes
    
    Ejemplo:
        >>> style = PDFStyle(
        ...     colors=ColorConfig(primary="#ff5722"),
        ...     fonts=FontConfig(size_body=11),
        ...     margins=MarginConfig.from_cm(2, 2, 2.5, 2.5)
        ... )
    """
    
    colors: ColorConfig = None  # type: ignore
    fonts: FontConfig = None    # type: ignore
    margins: MarginConfig = None  # type: ignore
    
    def __post_init__(self) -> None:
        """Inicializa valores por defecto si no se proporcionan."""
        # Usamos object.__setattr__ porque el dataclass es frozen
        if self.colors is None:
            object.__setattr__(self, "colors", ColorConfig())
        if self.fonts is None:
            object.__setattr__(self, "fonts", FontConfig())
        if self.margins is None:
            object.__setattr__(self, "margins", MarginConfig())
    
    @classmethod
    def default(cls) -> "PDFStyle":
        """Retorna un estilo con valores por defecto."""
        return cls(
            colors=ColorConfig(),
            fonts=FontConfig(),
            margins=MarginConfig(),
        )
    
    @classmethod
    def minimal(cls) -> "PDFStyle":
        """Retorna un estilo minimalista con márgenes pequeños."""
        return cls(
            colors=ColorConfig(
                primary="#000000",
                secondary="#666666",
                text="#000000",
            ),
            fonts=FontConfig(
                size_body=9,
                size_heading=12,
            ),
            margins=MarginConfig.from_cm(1.5, 1.5, 1.5, 1.5),
        )
    
    @classmethod
    def professional(cls) -> "PDFStyle":
        """Retorna un estilo profesional/corporativo."""
        return cls(
            colors=ColorConfig(
                primary="#2c3e50",
                secondary="#7f8c8d",
                text="#2c3e50",
                accent="#3498db",
            ),
            fonts=FontConfig(
                family=FontFamily.TIMES,
                size_body=11,
                size_heading=14,
                size_title=22,
            ),
            margins=MarginConfig.from_inches(1.0, 1.0, 1.25, 1.25),
        )
