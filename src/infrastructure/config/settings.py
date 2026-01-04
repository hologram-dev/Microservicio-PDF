"""
Application Settings
====================

Configuración centralizada usando Pydantic Settings.

Pydantic Settings proporciona:
- Lectura automática de variables de entorno
- Validación de tipos
- Valores por defecto
- Documentación automática

La configuración se carga una sola vez (singleton) usando lru_cache.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    
    Los valores se cargan de:
    1. Variables de entorno
    2. Archivo .env
    3. Valores por defecto
    
    Ejemplo de uso:
        >>> settings = get_settings()
        >>> print(settings.app_name)
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # ================================
    # Application Settings
    # ================================
    app_name: str = Field(
        default="PDF Export Microservice",
        description="Nombre de la aplicación",
    )
    app_version: str = Field(
        default="1.0.0",
        description="Versión de la aplicación",
    )
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Entorno de ejecución",
    )
    debug: bool = Field(
        default=False,
        description="Modo debug",
    )
    
    # ================================
    # Server Settings
    # ================================
    host: str = Field(
        default="0.0.0.0",
        description="Host del servidor",
    )
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Puerto del servidor",
    )
    workers: int = Field(
        default=1,
        ge=1,
        description="Número de workers",
    )
    
    # ================================
    # CORS Settings
    # ================================
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Orígenes permitidos (separados por coma)",
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Retorna la lista de orígenes CORS."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # ================================
    # PDF Settings
    # ================================
    pdf_default_page_size: str = Field(
        default="A4",
        description="Tamaño de página por defecto",
    )
    pdf_default_margin: float = Field(
        default=72.0,
        description="Margen por defecto (puntos)",
    )
    pdf_temp_dir: str = Field(
        default="/tmp/pdf_exports",
        description="Directorio temporal para PDFs",
    )
    
    # ================================
    # Logging Settings
    # ================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Nivel de logging",
    )
    log_format: Literal["json", "text"] = Field(
        default="json",
        description="Formato de logs",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene la instancia de configuración (singleton).
    
    Usa lru_cache para cachear la instancia y evitar
    leer las variables de entorno múltiples veces.
    
    Returns:
        Instancia de Settings
    """
    return Settings()
