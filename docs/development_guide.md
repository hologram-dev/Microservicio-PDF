# Guía de Desarrollo

## Requisitos Previos

- **Python 3.11+**
- **pip** o **poetry**
- **Docker** (opcional, para desarrollo con contenedores)
- **Git**

---

## Configuración del Entorno

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd Microservicio-PDF
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
# Dependencias de producción
pip install -r requirements.txt

# Dependencias de desarrollo (opcional)
pip install -e ".[dev]"
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar según necesidad
# nano .env  (Linux/Mac)
# notepad .env  (Windows)
```

---

## Ejecutar la Aplicación

### Modo Desarrollo (con hot reload)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Modo Producción

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Con Docker

```bash
# Desarrollo
docker-compose --profile dev up

# Producción
docker-compose up -d
```

---

## Estructura del Código

```
src/
├── domain/           # 🔵 Lógica de negocio pura
│   ├── entities/     #    Objetos con identidad
│   ├── value_objects/#    Objetos inmutables
│   ├── exceptions/   #    Errores del dominio
│   └── interfaces/   #    Contratos (Ports)
│
├── application/      # 🟢 Casos de uso
│   ├── use_cases/    #    Acciones del sistema
│   ├── dto/          #    Data Transfer Objects
│   └── services/     #    Servicios de aplicación
│
├── infrastructure/   # 🟠 Implementaciones
│   ├── pdf/          #    ReportLab generator
│   ├── config/       #    Settings
│   └── persistence/  #    Repositorios (futuro)
│
├── presentation/     # 🟣 API REST
│   ├── api/v1/       #    Endpoints versionados
│   ├── schemas/      #    Validación Pydantic
│   └── dependencies/ #    Inyección de dependencias
│
└── main.py          # Punto de entrada FastAPI
```

---

## Flujo de Trabajo de Desarrollo

### Agregar una Nueva Característica

1. **Domain First**: Definir entidades y reglas de negocio
2. **Use Case**: Crear el caso de uso en application
3. **Infrastructure**: Implementar si es necesario
4. **Presentation**: Crear endpoint y schemas
5. **Tests**: Escribir tests unitarios e integración

### Ejemplo: Agregar Soporte para Imágenes

```python
# 1. Domain: Nueva entidad
# src/domain/entities/pdf_image.py
@dataclass
class PDFImage:
    path: str
    width: float
    height: float

# 2. Application: Nuevo DTO
# src/application/dto/pdf_request_dto.py
@dataclass
class PDFImageDTO:
    path: str
    width: float
    height: float

# 3. Infrastructure: Actualizar generator
# src/infrastructure/pdf/reportlab_generator.py
def _build_image(self, image: PDFImage) -> Image:
    return Image(image.path, width=image.width, height=image.height)

# 4. Presentation: Actualizar schema
# src/presentation/schemas/pdf_schemas.py
class PDFImageSchema(BaseModel):
    path: str
    width: float
    height: float

# 5. Tests
# tests/unit/test_pdf_image.py
def test_image_creation():
    ...
```

---

## Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Solo unitarios
pytest tests/unit/

# Solo integración
pytest tests/integration/

# Test específico
pytest tests/unit/test_entities.py -v
```

### Estructura de Tests

```
tests/
├── conftest.py          # Fixtures compartidas
├── unit/                # Tests unitarios
│   ├── test_entities.py
│   ├── test_value_objects.py
│   └── test_use_cases.py
└── integration/         # Tests de integración
    └── test_api.py
```

---

## Linting y Formateo

### Ruff (Linter)

```bash
# Verificar
ruff check src/

# Corregir automáticamente
ruff check src/ --fix
```

### MyPy (Type Checking)

```bash
mypy src/
```

### Pre-commit (opcional)

```bash
# Instalar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

---

## Docker

### Desarrollo

```bash
# Construir y ejecutar con hot reload
docker-compose --profile dev up --build
```

### Producción

```bash
# Construir imagen
docker build -t pdf-microservice .

# Ejecutar
docker run -p 8000:8000 pdf-microservice
```

### Comandos Útiles

```bash
# Ver logs
docker-compose logs -f pdf-service

# Entrar al contenedor
docker-compose exec pdf-service bash

# Reconstruir
docker-compose up -d --build
```

---

## Debugging

### VS Code

Archivo `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["src.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

### PyCharm

1. Run → Edit Configurations
2. Add → Python
3. Script: module `uvicorn`
4. Parameters: `src.main:app --reload`

---

## Convenciones de Código

### Nombrado

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| Clases | PascalCase | `PDFDocument` |
| Funciones | snake_case | `generate_pdf` |
| Variables | snake_case | `page_size` |
| Constantes | UPPER_SNAKE | `DEFAULT_MARGIN` |
| Privados | _prefijo | `_validate()` |

### Importaciones

```python
# Orden: stdlib → third-party → local
import os
from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel

from src.domain.entities import PDFDocument
```

### Docstrings

```python
def generate_pdf(document: PDFDocument) -> bytes:
    """
    Genera un PDF a partir de un documento.
    
    Args:
        document: El documento a convertir
        
    Returns:
        Contenido del PDF como bytes
        
    Raises:
        PDFGenerationError: Si falla la generación
    """
```

---

## Troubleshooting

### Error: ModuleNotFoundError

```bash
# Asegurarse de que PYTHONPATH incluye src/
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# O instalar en modo editable
pip install -e .
```

### Error: ReportLab fonts

```bash
# En Linux, instalar fuentes
apt-get install fonts-liberation fonts-dejavu-core
```

### Error: Puerto en uso

```bash
# Encontrar proceso
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Matar proceso
kill -9 <PID>
```

---

## Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
