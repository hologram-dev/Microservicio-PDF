# PDF Export Microservice

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![ReportLab](https://img.shields.io/badge/ReportLab-4.0+-orange.svg)](https://www.reportlab.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Microservicio de exportación de PDFs construido con **FastAPI** y **ReportLab**, siguiendo los principios de **Clean Architecture**.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Documentación](#-documentación)
- [Testing](#-testing)
- [Docker](#-docker)
- [Contribución](#-contribución)

---

## 📖 Descripción

Este microservicio proporciona una API REST para la generación dinámica de documentos PDF. Está diseñado para integrarse con otros sistemas que necesiten exportar información en formato PDF.

### ¿Por qué ReportLab?

| Criterio | ReportLab | WeasyPrint |
|----------|-----------|------------|
| **Dependencias** | Mínimas, puro Python | Requiere Cairo, Pango, GDK-PixBuf |
| **Rendimiento** | Excelente para generación programática | Optimizado para conversión HTML→PDF |
| **Control** | Pixel-perfect, control total | Depende del CSS y rendering |
| **Caso de uso ideal** | Sin frontend existente ✅ | Cuando ya existe HTML/CSS |
| **Curva de aprendizaje** | Moderada | Baja si sabes CSS |

**Decisión técnica**: Se eligió ReportLab porque:
1. **No existe frontend** para extraer HTML/CSS
2. Ofrece **generación programática óptima** de PDFs
3. **Mayor control** sobre el diseño sin dependencias de rendering web
4. **Menor footprint** en contenedores Docker

---

## 🏗️ Arquitectura

Este proyecto implementa **Clean Architecture** (también conocida como Arquitectura Hexagonal o Ports & Adapters), propuesta por Robert C. Martin (Uncle Bob).

### ¿Qué es Clean Architecture?

Clean Architecture es un patrón de diseño de software que organiza el código en capas concéntricas, donde las **dependencias siempre apuntan hacia adentro** (hacia el dominio). Esto logra:

- **Independencia de frameworks**: El core de negocio no depende de FastAPI ni ReportLab
- **Testabilidad**: Cada capa se puede testear de forma aislada
- **Independencia de la UI**: Podríamos cambiar de REST a GraphQL sin tocar el dominio
- **Independencia de la BD**: El dominio no sabe cómo se persisten los datos
- **Independencia de agentes externos**: Las reglas de negocio no conocen el mundo exterior

### Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│              (FastAPI, Controllers, Schemas)                 │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 APPLICATION LAYER                    │    │
│  │           (Use Cases, DTOs, Services)                │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │              DOMAIN LAYER                    │    │    │
│  │  │    (Entities, Value Objects, Interfaces)     │    │    │
│  │  │                                              │    │    │
│  │  │          ⚡ REGLAS DE NEGOCIO ⚡              │    │    │
│  │  │                                              │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Implementa
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                        │
│        (ReportLab Implementation, Config, Persistence)       │
└─────────────────────────────────────────────────────────────┘
```

### Regla de Dependencia

> **Las dependencias solo pueden apuntar hacia adentro.** Nada en un círculo interno puede saber algo sobre algo en un círculo externo.

```
Presentation → Application → Domain ← Infrastructure
                    ↓
            Domain (Interfaces)
                    ↑
            Infrastructure (Implementaciones)
```

---

## 📁 Estructura del Proyecto

```
Microservicio-PDF/
│
├── src/                              # Código fuente principal
│   ├── main.py                       # Punto de entrada FastAPI
│   │
│   ├── domain/                       # 🔵 CAPA DE DOMINIO
│   │   │                             # El corazón de la aplicación
│   │   │                             # NO depende de NADA externo
│   │   │
│   │   ├── entities/                 # Entidades del dominio
│   │   │   └── pdf_document.py       # Representa un documento PDF
│   │   │
│   │   ├── value_objects/            # Objetos de valor (inmutables)
│   │   │   └── pdf_style.py          # Estilos: márgenes, fuentes, etc.
│   │   │
│   │   ├── exceptions/               # Excepciones del dominio
│   │   │   └── domain_exceptions.py  # Errores de reglas de negocio
│   │   │
│   │   └── interfaces/               # Puertos (Contratos/Interfaces)
│   │       └── pdf_generator_interface.py  # Contrato para generar PDFs
│   │
│   ├── application/                  # 🟢 CAPA DE APLICACIÓN
│   │   │                             # Orquesta los casos de uso
│   │   │                             # Depende SOLO del dominio
│   │   │
│   │   ├── use_cases/                # Casos de uso del sistema
│   │   │   └── generate_pdf.py       # Lógica para generar un PDF
│   │   │
│   │   ├── dto/                      # Data Transfer Objects
│   │   │   └── pdf_request_dto.py    # Datos de entrada/salida
│   │   │
│   │   └── services/                 # Servicios de aplicación
│   │       └── pdf_service.py        # Coordina múltiples casos de uso
│   │
│   ├── infrastructure/               # 🟠 CAPA DE INFRAESTRUCTURA
│   │   │                             # Implementaciones concretas
│   │   │                             # Adapters que implementan los Ports
│   │   │
│   │   ├── pdf/                      # Implementación del generador
│   │   │   └── reportlab_generator.py # Implementa la interfaz con ReportLab
│   │   │
│   │   ├── persistence/              # Repositorios (si se necesitan)
│   │   │   └── __init__.py
│   │   │
│   │   └── config/                   # Configuración de la app
│   │       └── settings.py           # Settings con Pydantic
│   │
│   └── presentation/                 # 🟣 CAPA DE PRESENTACIÓN
│       │                             # Interfaz con el mundo exterior
│       │                             # FastAPI vive aquí
│       │
│       ├── api/                      # Endpoints de la API
│       │   └── v1/                   # Versionado de API
│       │       ├── __init__.py
│       │       └── router.py         # Router principal v1
│       │
│       ├── schemas/                  # Schemas Pydantic
│       │   └── pdf_schemas.py        # Validación de requests/responses
│       │
│       └── dependencies/             # Inyección de dependencias
│           └── container.py          # Contenedor DI
│
├── docs/                             # 📚 Documentación
│   ├── architecture.md               # Explicación de la arquitectura
│   ├── api_design.md                 # Diseño de la API
│   └── development_guide.md          # Guía para desarrolladores
│
├── tests/                            # 🧪 Tests
│   ├── unit/                         # Tests unitarios
│   │   └── __init__.py
│   ├── integration/                  # Tests de integración
│   │   └── __init__.py
│   └── conftest.py                   # Fixtures de pytest
│
├── .env.example                      # Variables de entorno ejemplo
├── .gitignore                        # Archivos ignorados por Git
├── Dockerfile                        # Imagen Docker
├── docker-compose.yml                # Orquestación local
├── pyproject.toml                    # Configuración del proyecto
├── requirements.txt                  # Dependencias pip
└── README.md                         # Este archivo
```

### Explicación de Cada Capa

#### 🔵 Domain Layer (Capa de Dominio)
**Propósito**: Contiene la lógica de negocio pura y las reglas del dominio.

| Directorio | Propósito | Ejemplo |
|------------|-----------|---------|
| `entities/` | Objetos con identidad única | Un documento PDF con ID |
| `value_objects/` | Objetos inmutables sin identidad | Estilos de PDF |
| `exceptions/` | Errores de reglas de negocio | "El tamaño de página no es válido" |
| `interfaces/` | Contratos (Ports) | "Necesito algo que genere PDFs" |

**Regla clave**: Esta capa NO importa NADA de las otras capas.

#### 🟢 Application Layer (Capa de Aplicación)
**Propósito**: Orquesta el flujo de la aplicación y los casos de uso.

| Directorio | Propósito | Ejemplo |
|------------|-----------|---------|
| `use_cases/` | Acciones del sistema | "Generar un PDF de reporte" |
| `dto/` | Objetos de transferencia | Request con datos del PDF |
| `services/` | Coordinadores | Servicio que usa múltiples use cases |

**Regla clave**: Solo depende del dominio. No sabe de FastAPI ni ReportLab.

#### 🟠 Infrastructure Layer (Capa de Infraestructura)
**Propósito**: Implementa los contratos definidos en el dominio.

| Directorio | Propósito | Ejemplo |
|------------|-----------|---------|
| `pdf/` | Generador concreto | ReportLab implementando la interfaz |
| `persistence/` | Repositorios | Guardar PDFs en disco/S3 |
| `config/` | Configuración | Variables de entorno, settings |

**Regla clave**: Implementa las interfaces del dominio (inversión de dependencias).

#### 🟣 Presentation Layer (Capa de Presentación)
**Propósito**: Expone la aplicación al mundo exterior.

| Directorio | Propósito | Ejemplo |
|------------|-----------|---------|
| `api/` | Endpoints REST | POST /api/v1/pdf/generate |
| `schemas/` | Validación | Schemas Pydantic para requests |
| `dependencies/` | Inyección DI | Contenedor de dependencias |

**Regla clave**: Esta capa traduce HTTP ↔ DTOs de aplicación.

---

## 🛠️ Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.11+ | Lenguaje principal |
| FastAPI | 0.109+ | Framework web async |
| ReportLab | 4.0+ | Generación de PDFs |
| Pydantic | 2.0+ | Validación de datos |
| Uvicorn | 0.27+ | Servidor ASGI |
| pytest | 8.0+ | Testing |
| Docker | 24.0+ | Containerización |

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.11+
- pip o poetry
- Docker (opcional)

### Instalación Local

```bash
# Clonar el repositorio
git clone <repository-url>
cd Microservicio-PDF

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env
```

### Instalación con Docker

```bash
# Construir imagen
docker-compose build

# Iniciar servicio
docker-compose up -d
```

---

## 📖 Uso

### Iniciar el Servidor

```bash
# Desarrollo
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acceder a la Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📚 Documentación

Documentación detallada disponible en el directorio `/docs`:

| Documento | Descripción |
|-----------|-------------|
| [architecture.md](docs/architecture.md) | Explicación detallada de Clean Architecture |
| [api_design.md](docs/api_design.md) | Diseño y especificación de la API |
| [development_guide.md](docs/development_guide.md) | Guía para desarrolladores |

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Solo tests unitarios
pytest tests/unit/

# Solo tests de integración
pytest tests/integration/
```

---

## 🐳 Docker

### Comandos Útiles

```bash
# Construir imagen
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reconstruir y reiniciar
docker-compose up -d --build
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 📞 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.
