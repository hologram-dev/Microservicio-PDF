# 🚀 Guía Rápida: Locust Load Testing

## ✅ Locust Ya Está Corriendo!

Según tu terminal, **Locust ya está activo** en:
```
http://0.0.0.0:8089
```

## 🌐 Cómo Accesar Locust

### Opción 1: Desde WSL (recomendado)
```bash
# Abrir desde Windows
start http://localhost:8089
```

### Opción 2: Desde Navegador Directamente
1. Abre tu navegador (Chrome, Firefox, Edge)
2. Ve a: `http://localhost:8089`

---

## 📝 Configurar el Test en la UI de Locust

Una vez en `http://localhost:8089`, verás la interfaz de Locust. Configura:

### Para Test Moderado (recomendado para empezar)
- **Number of users**: `20`
- **Spawn rate**: `5` (usuarios por segundo)
- **Host**: `http://localhost:8001` (si tu servicio corre en 8001)

### Para Test Agresivo
- **Number of users**: `50`
- **Spawn rate**: `10`
- **Host**: `http://localhost:8001`

### Para Stress Test Extremo
- **Number of users**: `100`
- **Spawn rate**: `20`
- **Host**: `http://localhost:8001`

---

## 🎯 Qué Hace Locust

El script `locustfile.py` simula 2 tipos de usuarios:

### `PDFUser` (Usuario Normal)
- **Peso 3**: Genera PDFs de postulación
- **Peso 2**: Genera PDFs de contrato
- **Peso 1**: Verifica health endpoint
- Espera 1-3 segundos entre requests

### `HeavyLoadUser` (Carga Pesada)
- Genera PDFs en ráfaga rápida
- Espera solo 0.1-0.5 segundos
- Para stress testing extremo

---

## 📊 Métricas que Verás

En la interfaz de Locust verás:

| Métrica | Descripción |
|---------|-------------|
| **RPS** | Requests por segundo actual |
| **Failures** | Número de errores (HTTP 4xx/5xx) |
| **Response Time** | P50, P95, P99 en ms |
| **Users** | Usuarios simulados activos |

---

## 🚦 Cómo Interpretar Resultados

### ✅ Buenas señales
- RPS estable > 50
- Failures < 1%
- P95 < 2000ms

### ⚠️ Señales de advertencia
- RPS decreciente con más usuarios
- Failures > 5%
- P95 > 5000ms

### 🔴 Problemas críticos
- RPS colapsa
- Failures > 20%
- P99 > 30000ms (30s)

---

## 🛑 Cómo Detener Locust

```bash
# En la terminal de WSL donde corre Locust
Ctrl + C
```

O simplemente cierra la terminal.

---

## 📈 Comandos Útiles

### Ejecutar Test Headless (sin UI)
```bash
# Test de 2 minutos, 30 usuarios
locust -f tests/load/locustfile.py --host http://localhost:8001 \
       -u 30 -r 5 --run-time 2m --headless
```

### Ver Estadísticas en Tiempo Real
```bash
# Agregar --print-stats para ver stats cada 2 segundos
locust -f tests/load/locustfile.py --host http://localhost:8001 \
       -u 30 -r 5 --run-time 2m --headless --print-stats
```

### Exportar Results a CSV
```bash
locust -f tests/load/locustfile.py --host http://localhost:8001 \
       -u 50 -r 10 --run-time 5m --headless \
       --csv=results/locust_test
```

---

## 🎓 Escenarios de Testing Recomendados

### 1. Test de Baseline (entender capacidad)
```
Users: 10
Spawn rate: 2
Duration: 2 minutos
```

### 2. Test de Carga Normal (uso típico)
```
Users: 30
Spawn rate: 5
Duration: 5 minutos
```

### 3. Stress Test (encontrar límites)
```
Users: 100
Spawn rate: 20
Duration: 10 minutos
```

### 4. Spike Test (pico repentino)
```
Users: 200
Spawn rate: 50  # Spawn rápido para simular pico
Duration: 1 minuto
```

---

## 🔍 Verificar que el Servicio Esté Corriendo

Antes de ejecutar Locust, asegúrate de que el servicio PDF esté up:

```bash
curl http://localhost:8001/api/v1/pdf/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "pdf-generator",
  "version": "1.0.0"
}
```

---

## 💡 Tips Pro

1. **Empezar pequeño**: Siempre empieza con pocos usuarios (10-20) y aumenta gradualmente
2. **Monitoring**: Observa el uso de CPU/RAM del Docker container mientras corres tests
3. **Rate Limiting**: Recuerda que tienes 100 req/min por IP, así que con muchos usuarios verás HTTP 429
4. **Warmup**: Los primeros requests pueden ser más lentos (cold start), deja correr 30s antes de medir

---

## 🐋 Ver Recursos del Container Durante Test

```bash
# En otra terminal
docker stats pdf-export-service
```

Esto te muestra CPU%, MEM usage en tiempo real mientras Locust corre.

---

¿Quieres que te ayude a interpretar los resultados una vez que ejecutes el test?
