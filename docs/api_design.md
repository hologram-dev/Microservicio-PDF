# Diseño de la API REST

## Visión General

Esta API proporciona endpoints para generar documentos PDF de forma programática.

### Base URL

```
http://localhost:8000/api/v1
```

### Formato de Respuestas

Todas las respuestas están en formato JSON (excepto la descarga de PDFs que es binario).

---

## Endpoints

### Health Check

#### `GET /api/v1/pdf/health`

Verifica el estado del servicio de PDF.

**Response 200:**
```json
{
  "status": "healthy",
  "service": "pdf-generator",
  "version": "1.0.0"
}
```

---

### Generar PDF (Futuro)

#### `POST /api/v1/pdf/generate`

Genera un documento PDF a partir de datos JSON.

**Request Body:**
```json
{
  "title": "Reporte Mensual",
  "sections": [
    {
      "title": "Resumen Ejecutivo",
      "content": "Este mes hemos logrado...",
      "level": 1
    },
    {
      "title": "Datos de Ventas",
      "level": 1,
      "tables": [
        {
          "headers": ["Producto", "Cantidad", "Ingresos"],
          "rows": [
            ["Widget A", "100", "$10,000"],
            ["Widget B", "50", "$5,000"]
          ],
          "title": "Ventas por Producto"
        }
      ]
    }
  ],
  "author": "Sistema de Reportes",
  "page_size": "A4",
  "orientation": "portrait",
  "style": {
    "primary_color": "#1a73e8",
    "font_size": 11
  }
}
```

**Response 200:**
```json
{
  "success": true,
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "Reporte_Mensual_550e8400.pdf",
  "message": "PDF generado exitosamente"
}
```

**Response 400 (Error de validación):**
```json
{
  "success": false,
  "error": "INVALID_DOCUMENT",
  "message": "El documento debe tener al menos una sección",
  "details": {
    "section_count": 0
  }
}
```

---

### Generar PDF y Descargar (Futuro)

#### `POST /api/v1/pdf/generate/download`

Genera un PDF y lo retorna directamente como descarga.

**Request:** Igual que `/generate`

**Response 200:** Archivo PDF binario

**Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="Reporte_Mensual.pdf"
```

---

## Schemas de Datos

### PDFSection

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `title` | string | ✅ | Título de la sección |
| `content` | string | ❌ | Contenido de texto |
| `level` | integer (1-6) | ❌ | Nivel del encabezado |
| `tables` | PDFTable[] | ❌ | Tablas en la sección |

### PDFTable

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `headers` | string[] | ✅ | Encabezados de columnas |
| `rows` | string[][] | ❌ | Filas de datos |
| `title` | string | ❌ | Título de la tabla |

### PDFStyle

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `primary_color` | string (#RRGGBB) | ❌ | Color primario |
| `text_color` | string (#RRGGBB) | ❌ | Color del texto |
| `font_family` | enum | ❌ | Helvetica, Times-Roman, Courier |
| `font_size` | number (6-72) | ❌ | Tamaño de fuente |
| `margin_top` | number | ❌ | Margen superior (puntos) |
| `margin_bottom` | number | ❌ | Margen inferior (puntos) |
| `margin_left` | number | ❌ | Margen izquierdo (puntos) |
| `margin_right` | number | ❌ | Margen derecho (puntos) |

---

## Códigos de Error

| Código | HTTP Status | Descripción |
|--------|-------------|-------------|
| `INVALID_DOCUMENT` | 400 | Documento mal formado |
| `INVALID_STYLE` | 400 | Estilos inválidos |
| `PDF_GENERATION_ERROR` | 500 | Error al generar PDF |
| `DOCUMENT_NOT_FOUND` | 404 | Documento no encontrado |

---

## Ejemplos de Uso

### Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/pdf/generate/download"
payload = {
    "title": "Mi Reporte",
    "sections": [
        {"title": "Introducción", "content": "Hola mundo"}
    ]
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    with open("reporte.pdf", "wb") as f:
        f.write(response.content)
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/pdf/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Document",
    "sections": [
      {"title": "Section 1", "content": "Hello world"}
    ]
  }'
```

### JavaScript (fetch)

```javascript
const response = await fetch('http://localhost:8000/api/v1/pdf/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Mi Documento',
    sections: [
      { title: 'Sección 1', content: 'Contenido...' }
    ]
  })
});

const result = await response.json();
console.log(result);
```

---

## Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
