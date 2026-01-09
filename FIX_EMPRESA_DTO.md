# 🔧 FIX URGENTE - Error 500 en Endpoint de Contrato

## ❌ Problema
```
TypeError: EmpresaDTO.__init__() got an unexpected keyword argument 'correo'
```

## 🎯 Solución

### 1. Agregar campo `correo` a `EmpresaDTO`

**Archivo**: `src/application/dto/negocio_global_dtos.py`

**Línea 86** - Agregar DESPUÉS de `codigo: Optional[int] = None`:
```python
correo: Optional[str] = None  # Added to match EmpresaSchema
```

El DTO `EmpresaDTO` debería quedar así:

```python
@dataclass
class EmpresaDTO:
    """
    DTO con los datos de la empresa.
    
    Campos requeridos: nombre
    Campos opcionales: direccion, codigo_postal, telefono, codigo, correo
    """
    nombre: str
    direccion: Optional[str] = None
    codigo_postal: Optional[int] = None
    telefono: Optional[str] = None
    codigo: Optional[int] = None
    correo: Optional[str] = None  # <-- AGREGAR ESTA LÍNEA
```

---

## ✅ Payload Correcto para Contrato

Este payload ahora funcionará:

```json
{
  "estudiante": {
    "nombre": "María",
    "apellido": "González",
    "dni": "42856123",
    "email": "maria.gonzalez@gmail.com"
  },
  "universidad": {
    "nombre": "Universidad Nacional de Córdoba",
    "direccion": "Av. Haya de la Torre s/n, Ciudad Universitaria",
    "codigo_postal": 5000,
    "correo": "pasantias@unc.edu.ar",
    "telefono": "+543514334000"
  },
  "carrera": {
    "nombre": "Ingeniería en Sistemas de Información",
    "codigo": "ISI-2020",
    "plan_estudios": "Plan 2020"
  },
  "empresa": {
    "nombre": "TechnoSoft Argentina S.A.",
    "direccion": "Av. Colón 500, Piso 8",
    "codigo_postal": 5000,
    "telefono": "+543514238900",
    "codigo": 15847,
    "correo": "rrhh@technosoft.com.ar"
  },
  "proyecto": {
    "nombre": "Sistema de Gestión de Recursos Humanos",
    "fecha_inicio": "2026-02-01",
    "descripcion": "Desarrollo de un sistema integral",
    "numero": 2026001,
    "estado": "Activo",
    "fecha_fin": "2026-08-01"
  },
  "puesto": {
    "nombre": "Desarrollador Backend Junior",
    "descripcion": "Desarrollo de APIs REST con Python/FastAPI",
    "codigo": 1025,
    "horas_dedicadas": 30
  },
  "postulacion": {
    "numero": 450123,
    "fecha": "2025-12-15T10:30:00-03:00",
    "cantidad_materias_aprobadas": 28,
    "cantidad_materias_regulares": 3,
    "estado": "Aprobada"
  },
  "contrato": {
    "numero": 550234,
    "fecha_inicio": "2026-02-01",
    "fecha_fin": "2026-08-01",
    "fecha_emision": "2026-01-07",
    "estado": "Activo"
  }
}
```

### ⚠️ Nota Importante sobre Tipos

- `codigo_postal`: **integer** (5000, no "5000")
- `codigo` (empresa): **integer** (15847)
- `numero` (proyecto): **integer** (2026001)
- `codigo` (puesto): **integer** (1025)
- `numero` (postulacion): **integer** (450123)
- `numero` (contrato): **integer** (550234)

Pydantic convierte strings a integers automáticamente, pero es mejor enviar el tipo correcto.

---

## 🔄 Reiniciar Docker Después del Fix

```bash
# Reconstruir container con los cambios
docker compose down
docker compose up --build -d

# Ver logs
docker compose logs pdf-service -f
```

---

## ✅ Verificar que Funciona

```bash
curl -X POST http://localhost:8001/api/v1/pdf/generate/comprobante_contrato \
  -H "Content-Type: application/json" \
  -d @payload_contrato.json \
  --output test_contrato.pdf
```

Debería retornar HTTP 200 y generar un PDF.
