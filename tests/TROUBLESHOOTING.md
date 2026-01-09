# Guía de Testing - Solución de Problemas

## ✅ Solución al Error "ModuleNotFoundError: No module named 'src'"

### Causa
Python no puede encontrar el módulo `src` porque el directorio raíz del proyecto no está en el PYTHONPATH.

### Solución 1: Usar run_tests.sh (Recomendado)

El script ya configura automáticamente el PYTHONPATH:

```bash
# Desde el directorio raíz del proyecto
./run_tests.sh install  # Instalar dependencias
./run_tests.sh unit     # Ejecutar tests
```

### Solución 2: Configurar PYTHONPATH manualmente

```bash
# En cada sesión de terminal
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Luego ejecutar tests
pytest tests/unit tests/integration -v
```

### Solución 3: Agregar al .bashrc o .zshrc (Permanente)

```bash
# Agregar a ~/.bashrc o ~/.zshrc
export PYTHONPATH="/mnt/h/microservicio PDF/Microservicio-PDF:${PYTHONPATH}"
```

---

## 🔧 Comandos Corregidos

### Navegación correcta
```bash
# IMPORTANTE: Estar en el directorio RAÍZ del proyecto
cd "/mnt/h/microservicio PDF/Microservicio-PDF"

# Verificar que estás en el lugar correcto
ls -la  # Debe mostrar requirements.txt, src/, tests/
```

### Instalar Dependencias
```bash
# Primero instalar las dependencias de testing
pip install -r requirements-test.txt
```

### Ejecutar Tests
```bash
# Opción A: Usar el script helper
./run_tests.sh unit

# Opción B: Manual con PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"
pytest tests/unit tests/integration -v
```

### Load Testing
```bash
# Primero asegurarse de que locust esté instalado
pip install locust

# Ejecutar Locust
./run_tests.sh load

# O manual:
locust -f tests/load/locustfile.py --host http://localhost:8001
```

### Benchmark
```bash
./run_tests.sh benchmark

# O manual:
python tests/benchmark/benchmark.py
```

---

## 📝 Checklist Antes de Ejecutar Tests

- [ ] Estás en el directorio raíz del proyecto (`/mnt/h/microservicio PDF/Microservicio-PDF`)
- [ ] El virtual environment está activado (`(venv)` al inicio del prompt)
- [ ] Instalaste las dependencias de testing (`pip install -r requirements-test.txt`)
- [ ] El servicio Docker está corriendo si vas a hacer load tests
- [ ] Configuraste PYTHONPATH o usas `run_tests.sh`

---

## 🐛 Otros Errores Comunes

### Error: "pytest: command not found"
```bash
pip install pytest pytest-asyncio
```

### Error: "locust: command not found"
```bash
pip install locust
```

### Error: "No module named 'httpx'"
```bash
pip install httpx
```

### Warning: "Unknown config option: asyncio_mode"
Ignorar este warning, no afecta la ejecución de los tests.

---

## ✅ Verificación Rápida

```bash
# 1. Navegar al directorio correcto
cd "/mnt/h/microservicio PDF/Microservicio-PDF"

# 2. Verificar ubicación
pwd
# Debe mostrar: /mnt/h/microservicio PDF/Microservicio-PDF

# 3. Instalar dependencias (solo una vez)
pip install -r requirements-test.txt

# 4. Ejecutar un test simple
export PYTHONPATH="${PWD}:${PYTHONPATH}"
pytest tests/unit/test_date_cache.py -v

# Si funciona, ejecutar todos:
pytest tests/unit tests/integration -v
```
