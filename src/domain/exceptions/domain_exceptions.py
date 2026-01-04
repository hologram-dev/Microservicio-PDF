"""
Domain Exceptions
=================

Excepciones personalizadas del dominio.

Las excepciones del dominio:
- Representan violaciones de reglas de negocio
- Son independientes de la infraestructura
- Contienen información útil para debugging
- Pueden ser traducidas a errores HTTP en la capa de presentación

Jerarquía de excepciones:
    DomainException (base)
    ├── PDFGenerationError
    ├── InvalidDocumentError
    ├── InvalidStyleError
    └── DocumentNotFoundError
"""


class DomainException(Exception):
    """
    Excepción base para errores del dominio.
    
    Todas las excepciones del dominio heredan de esta clase,
    lo que permite capturar cualquier error de negocio de forma genérica.
    
    Atributos:
        message: Descripción del error
        code: Código de error para identificación programática
        details: Información adicional del error
    """
    
    def __init__(
        self, 
        message: str, 
        code: str = "DOMAIN_ERROR",
        details: dict | None = None
    ) -> None:
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """Convierte la excepción a un diccionario para serialización."""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details,
        }


class PDFGenerationError(DomainException):
    """
    Error durante la generación del PDF.
    
    Se lanza cuando hay un problema técnico al generar el PDF,
    como errores de I/O, problemas de memoria, etc.
    
    Ejemplo:
        >>> raise PDFGenerationError(
        ...     "Error al escribir el archivo",
        ...     details={"path": "/tmp/output.pdf"}
        ... )
    """
    
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            message=message,
            code="PDF_GENERATION_ERROR",
            details=details or {},
        )


class InvalidDocumentError(DomainException):
    """
    Error de documento inválido.
    
    Se lanza cuando el documento no cumple con las reglas de negocio,
    como título vacío, secciones mal formadas, etc.
    
    Ejemplo:
        >>> raise InvalidDocumentError(
        ...     "El documento debe tener al menos una sección",
        ...     details={"section_count": 0}
        ... )
    """
    
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            message=message,
            code="INVALID_DOCUMENT",
            details=details or {},
        )


class InvalidStyleError(DomainException):
    """
    Error de estilo inválido.
    
    Se lanza cuando la configuración de estilo no es válida,
    como colores mal formateados, márgenes negativos, etc.
    
    Ejemplo:
        >>> raise InvalidStyleError(
        ...     "Color primario inválido",
        ...     details={"color": "not-a-color"}
        ... )
    """
    
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            message=message,
            code="INVALID_STYLE",
            details=details or {},
        )


class DocumentNotFoundError(DomainException):
    """
    Error de documento no encontrado.
    
    Se lanza cuando se intenta acceder a un documento que no existe.
    
    Ejemplo:
        >>> raise DocumentNotFoundError(
        ...     details={"document_id": "123e4567-e89b-12d3-a456-426614174000"}
        ... )
    """
    
    def __init__(
        self, 
        message: str = "Documento no encontrado",
        details: dict | None = None
    ) -> None:
        super().__init__(
            message=message,
            code="DOCUMENT_NOT_FOUND",
            details=details or {},
        )
