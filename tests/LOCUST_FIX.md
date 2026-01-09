# 🔧 Solución Rápida: Errores de Locust

## ❌ Problema Identificado

Los errores que ves:
```
CatchResponseError('Got unexpected status 0')
Health check failed with 0
```

Significan que **Locust no puede conectarse al servicio** porque está usando el puerto incorrecto.

---

## ✅ Solución

### Opción 1: Cambiar el Host en la UI de Locust (MÁS FÁCIL)

1. **Detén el test actual** en Locust (click en "STOP")
2. Click en "EDIT"
3. Cambia el **Host** a: `http://localhost:9000` (o el puerto correcto de tu Docker)
4. Click "NEW" para iniciar con el puerto correcto

### Opción 2: Actualizar locustfile.py (PERMANENTE)

Ya actualicé los archivos para usar `http://localhost:9000` por defecto. Reinicia Locust:

```bash
# Detener Locust actual (Ctrl+C)
# Reiniciar con el puerto correcto
./run_tests.sh load
```

---

## 🔍 Verificar Puerto Correcto

### Ver puertos de Docker
```bash
docker ps
```

Busca la línea `pdf-export-service` y verás algo como:
```
0.0.0.0:9000->8000/tcp
```

Esto significa:
- **Puerto host** (tu máquina): `9000`
- **Puerto container**: `8000`

Usa `http://localhost:9000` en Locust.

### Probar conectividad
```bash
# Verificar que el servicio responde
curl http://localhost:9000/api/v1/pdf/health

# Debería retornar:
# {"status":"healthy","service":"pdf-generator","version":"1.0.0"}
```

---

## 📋 Comandos Corregidos

### Locust con puerto correcto
```bash
# UI web
locust -f tests/load/locustfile.py --host http://localhost:9000

# Headless
locust -f tests/load/locustfile.py --host http://localhost:9000 -u 20 -r 5 --run-time 2m --headless
```

### Benchmark con puerto correcto
```bash
# El script benchmark.py ya fue actualizado
python tests/benchmark/benchmark.py
```

---

## 🎯 Siguiente Paso

1. **Detén Locust actual** (Ctrl+C en la terminal WSL)
2. **Reinicia Locust** con:
   ```bash
   ./run_tests.sh load
   ```
3. En la UI web, **verifica que el Host sea `http://localhost:9000`**
4. Click "Start swarming"

Deberías ver ahora **requests exitosos** en vez de failures.

---

## 💡 Configuración según tu setup

### Si usas Docker (docker-compose up)
```
Host: http://localhost:9000
```

### Si ejecutas local (python -m uvicorn)
```
Host: http://localhost:8000
```

### Si cambiaste el puerto en docker-compose.yml
Verifica la línea `ports:` en docker-compose.yml:
```yaml
ports:
  - "XXXX:8000"  # XXXX es el puerto que debes usar
```
