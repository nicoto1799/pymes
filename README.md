# 🎯 Google Maps Scraper para PYMEs Colombia

Herramienta para extraer información pública de negocios en Google Maps. Ideal para prospección B2B de clínicas, consultorios y PYMEs en Colombia.

## ✨ Características

- ✅ Extrae información pública de Google Maps
- ✅ Exporta a Excel, CSV y JSON
- ✅ Limpia y formatea datos automáticamente
- ✅ Filtra por ciudad, tipo de negocio, etc.
- ✅ Incluye teléfonos, direcciones, sitios web
- ✅ Respetuoso con rate limits

## 📋 Datos que extrae

- Nombre del negocio
- Categoría
- Rating y número de reseñas
- Dirección completa
- Teléfono
- Sitio web
- Horarios
- Fecha de extracción

## 🚀 Instalación

### 1. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar navegadores de Playwright

```bash
playwright install chromium
```

## 💻 Uso básico

### Opción 1: Ejecutar el script de ejemplo

```bash
python gmaps_scraper.py
```

Esto buscará "clínica odontológica Medellín" y guardará los resultados.

### Opción 2: Usar en tu propio código

```python
import asyncio
from gmaps_scraper import GoogleMapsScraper

async def buscar():
    scraper = GoogleMapsScraper()

    # Buscar lugares
    results = await scraper.search_places(
        query="clínica estética Bogotá",
        max_results=30,
        scroll_attempts=5
    )

    # Guardar resultados
    scraper.save_to_excel('clinicas_bogota.xlsx')
    scraper.print_summary()

asyncio.run(buscar())
```

## 🎯 Ejemplos de búsquedas

### Para clínicas odontológicas

```python
queries = [
    "clínica odontológica Medellín",
    "odontología Bogotá",
    "dentista Cali",
]
```

### Para clínicas estéticas

```python
queries = [
    "clínica estética Medellín",
    "cirugía estética Bogotá",
    "medicina estética Cali",
]
```

### Para consultorios especializados

```python
queries = [
    "oftalmología Medellín",
    "ortopedia Bogotá",
    "dermatología Cali",
]
```

## ⚙️ Parámetros de configuración

### `search_places()`

- **query**: Término de búsqueda (ej: "clínica odontológica Medellín")
- **max_results**: Máximo de resultados a extraer (default: 50)
- **scroll_attempts**: Intentos de scroll para cargar más (default: 10)

### Ejemplo avanzado

```python
results = await scraper.search_places(
    query="clínica odontológica Medellín",
    max_results=100,      # Extraer hasta 100 lugares
    scroll_attempts=15    # Más scrolls = más resultados
)
```

## 📊 Formatos de exportación

### Excel (recomendado para análisis)
```python
scraper.save_to_excel('resultados.xlsx')
```

### CSV (compatible con CRM)
```python
scraper.save_to_csv('resultados.csv')
```

### JSON (para desarrollo)
```python
scraper.save_to_json('resultados.json')
```

## 🔍 Filtrar resultados con WhatsApp

Después de extraer, puedes filtrar solo los que tienen teléfono:

```python
# Filtrar resultados con teléfono
with_phone = [r for r in scraper.results if r.get('phone')]

# Ver cuántos tienen WhatsApp potencial (Colombia usa mucho WhatsApp)
print(f"Negocios con teléfono: {len(with_phone)}")

# Guardar solo esos
import pandas as pd
df = pd.DataFrame(with_phone)
df.to_excel('leads_con_telefono.xlsx', index=False)
```

## ⚖️ Consideraciones legales

- ✅ Extrae solo información **pública** de Google Maps
- ✅ No hace scraping masivo ni abusivo
- ✅ Respeta rate limits y tiempos de espera
- ❌ **NO** envíes spam masivo con esta información
- ✅ Úsala para contacto **personalizado** uno a uno

### Uso correcto

- Contacto individual y personalizado
- Mensajes relevantes al negocio
- Respetar si piden no ser contactados

### ❌ Uso incorrecto

- Envío masivo automatizado
- Spam
- Violación de Habeas Data

## 🛠 Troubleshooting

### Error: "playwright not found"

```bash
pip install playwright
playwright install chromium
```

### Error: "No results found"

- Verifica tu conexión a internet
- Prueba con una búsqueda más específica
- Aumenta el timeout en el código

### El navegador no se abre

- Verifica que Chromium esté instalado: `playwright install chromium`
- Prueba con `headless=False` para ver qué pasa

### Pocos resultados

- Aumenta `scroll_attempts` a 15-20
- Aumenta `max_results`
- Prueba búsquedas más amplias

## 📈 Tips para mejores resultados

### 1. Búsquedas específicas funcionan mejor

✅ "clínica odontológica Medellín"
❌ "clínica Colombia"

### 2. Una ciudad a la vez

```python
cities = ["Medellín", "Bogotá", "Cali", "Barranquilla"]
for city in cities:
    results = await scraper.search_places(
        query=f"clínica odontológica {city}",
        max_results=50
    )
    scraper.save_to_excel(f'clinicas_{city}.xlsx')
```

### 3. Combina categorías

```python
categories = ["odontológica", "estética", "oftalmología"]
city = "Medellín"

for cat in categories:
    results = await scraper.search_places(
        query=f"clínica {cat} {city}",
        max_results=30
    )
```

## 🎯 Siguiente paso: Contacto

Una vez tengas los datos:

1. **Filtra** los que tienen teléfono
2. **Revisa manualmente** que sean negocios activos
3. **Prepara tu mensaje** personalizado
4. **Contacta 10-20 por día** máximo
5. **Lleva registro** de respuestas

### Ejemplo de flujo completo

```python
# 1. Extraer
results = await scraper.search_places("clínica odontológica Medellín", max_results=50)

# 2. Filtrar
leads = [r for r in results if r.get('phone') and r.get('rating')]

# 3. Ordenar por rating (los mejores primero)
leads_sorted = sorted(leads, key=lambda x: float(x['rating'] or 0), reverse=True)

# 4. Guardar
import pandas as pd
df = pd.DataFrame(leads_sorted)
df.to_excel('leads_prioritarios.xlsx', index=False)

print(f"✅ {len(leads_sorted)} leads listos para contactar")
```

## 📞 Soporte

Si tienes dudas o problemas:
1. Revisa este README
2. Verifica que las dependencias estén instaladas
3. Prueba con búsquedas simples primero

## 📝 Licencia

Uso personal y comercial. Usa con responsabilidad y respeta las leyes de protección de datos.
