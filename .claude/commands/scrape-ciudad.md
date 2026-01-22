# Scrape Ciudad Command

Ejecuta una búsqueda de Google Maps en una ciudad específica usando el scraper de Selenium.

## Instrucciones

El usuario te proporcionará:
1. **Ciudad** (ej: "Medellín", "Bogotá", "Cali")
2. **Tipo de negocio** (ej: "clínica odontológica", "consultorio psicológico", "clínica estética")
3. **Cantidad de resultados** (opcional, default: 30)

## Pasos a seguir:

1. **Validar parámetros:**
   - Si faltan parámetros, pregunta al usuario
   - Sugerir cantidad entre 20-50 resultados
   - Confirmar la búsqueda antes de ejecutar

2. **Crear script temporal:**
   - Crea un archivo Python temporal llamado `scrape_temp.py`
   - Usa `GoogleMapsScraperSelenium` de `gmaps_scraper_selenium.py`
   - Configura el scraper con `headless=True` para producción
   - Query format: `"{tipo_negocio} {ciudad}"`

3. **Configuración recomendada:**
   - Para 20-30 resultados: `scroll_attempts=10`
   - Para 30-50 resultados: `scroll_attempts=15`
   - Pausa de 2 segundos entre scrolls

4. **Ejecutar scraping:**
   - Activar el entorno virtual primero: `source venv/bin/activate`
   - Ejecutar el script temporal
   - Mostrar progreso al usuario

5. **Generar archivos de salida:**
   - Formato de nombre: `{Ciudad}_{Fecha}.csv` y `.xlsx`
   - Fecha en formato: `YYYYMMDD_HHMMSS`
   - Generar ambos formatos (CSV y Excel)

6. **Mostrar resumen:**
   - Total de resultados encontrados
   - Cantidad con teléfono
   - Cantidad con website
   - Promedio de rating
   - Rutas de archivos generados

7. **Limpiar:**
   - Eliminar el script temporal
   - Desactivar entorno virtual

## Ejemplo de uso:

Usuario: `/scrape-ciudad Medellín "clínica odontológica" 30`

Respuesta esperada:
```
🔍 Iniciando búsqueda en Google Maps...
📍 Ciudad: Medellín
🏢 Tipo: clínica odontológica
📊 Resultados objetivo: 30

[Ejecuta scraping...]

✅ Búsqueda completada!
📊 Resultados: 28 negocios encontrados
📞 Con teléfono: 23 (82%)
🌐 Con website: 18 (64%)
⭐ Rating promedio: 4.3

💾 Archivos generados:
- Medellín_20251222_143052.csv
- Medellín_20251222_143052.xlsx
```

## Notas importantes:

- Siempre usar `gmaps_scraper_selenium.py` (NO la versión Playwright)
- No olvides activar el entorno virtual antes de ejecutar
- Si hay errores, muestra el mensaje de error completo al usuario
- Sugiere al usuario revisar manualmente los resultados antes de contactar
