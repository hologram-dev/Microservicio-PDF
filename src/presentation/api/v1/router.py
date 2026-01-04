"""
API v1 Router
=============

Router principal para la versión 1 de la API.

Este archivo define los endpoints de la API.
Los endpoints están vacíos por ahora - se implementarán
en la siguiente fase del desarrollo.

Estructura típica de un endpoint:
1. Recibe request HTTP
2. Valida con Pydantic schemas
3. Convierte a DTOs
4. Llama al servicio de aplicación
5. Convierte respuesta a schema
6. Retorna response HTTP
"""

from fastapi import APIRouter

router = APIRouter(prefix="/pdf", tags=["PDF"])


# ================================
# Endpoints (a implementar)
# ================================

# POST /api/v1/pdf/generate
# Genera un PDF a partir de un request JSON

# POST /api/v1/pdf/generate/stream
# Genera un PDF y lo retorna como stream

# GET /api/v1/pdf/templates
# Lista las plantillas disponibles

# GET /api/v1/pdf/health
# Health check del servicio


@router.get("/health")
async def health_check():
    """
    Health check del servicio de PDF.
    
    Returns:
        Estado del servicio
    """
    return {
        "status": "healthy",
        "service": "pdf-generator",
        "version": "1.0.0",
    }
