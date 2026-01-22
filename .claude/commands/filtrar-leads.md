# Filtrar Leads Command

Filtra y prioriza leads de un archivo de resultados según criterios específicos.

## Instrucciones

El usuario te proporcionará:
1. **Archivo de entrada** (CSV o Excel con resultados del scraper)
2. **Criterios de filtrado** (opcional - si no se especifica, pregunta)

## Criterios de filtrado disponibles:

- `rating_min`: Calificación mínima (ej: 4.0, 4.5)
- `con_telefono`: true/false - Solo leads con teléfono
- `con_website`: true/false - Solo leads con sitio web
- `ciudad`: Filtrar por ciudad específica (si el archivo tiene múltiples ciudades)
- `reviews_min`: Número mínimo de reseñas (ej: 10, 20)
- `top_n`: Tomar solo los N mejores por rating

## Pasos a seguir:

1. **Validar archivo de entrada:**
   - Verificar que existe el archivo
   - Validar que es CSV o Excel (.xlsx)
   - Leer el archivo con pandas
   - Mostrar resumen: total de registros, columnas disponibles

2. **Determinar criterios:**
   - Si el usuario no especificó criterios, preguntar qué quiere filtrar
   - Sugerir criterios comunes:
     - "Solo con teléfono y rating > 4.0" (para prospección prioritaria)
     - "Top 20 mejor calificados con teléfono" (para campaña selecta)
     - "Ciudad específica con website" (para análisis web)

3. **Aplicar filtros:**
   - Filtrar según los criterios especificados
   - Ordenar por rating descendente (mejores primero)
   - Si hay empates en rating, ordenar por número de reseñas

4. **Generar archivo filtrado:**
   - Nombre del archivo: `FILTRADO_{nombre_original}_{timestamp}.xlsx`
   - Incluir hoja con estadísticas de filtrado
   - Generar ambos formatos (CSV y Excel)

5. **Calcular y mostrar estadísticas:**
   - Registros originales vs filtrados
   - Porcentaje que pasó el filtro
   - Rating promedio antes y después
   - Distribución por ciudad (si aplica)

6. **Priorización automática:**
   - Agregar columna `prioridad` con valores: ALTA, MEDIA, BAJA
   - Criterios de prioridad:
     - ALTA: rating >= 4.5, reviews >= 50, tiene teléfono
     - MEDIA: rating >= 4.0, reviews >= 10, tiene teléfono
     - BAJA: resto
   - Ordenar por prioridad

## Ejemplo de uso:

Usuario: `/filtrar-leads CONSOLIDADO_todas_ciudades.xlsx`

Claude pregunta:
```
📋 Archivo encontrado: 133 registros

¿Qué filtros quieres aplicar?

Opciones comunes:
1. Solo con teléfono y rating > 4.0 (prospección prioritaria)
2. Top 30 mejor calificados con teléfono (campaña selecta)
3. Ciudad específica
4. Criterios personalizados

Selecciona una opción o especifica tus criterios.
```

Usuario: "Opción 1"

Respuesta esperada:
```
🔍 Aplicando filtros...
✅ Filtrado completado!

📊 Estadísticas:
- Registros originales: 133
- Registros filtrados: 87 (65%)
- Rating promedio: 4.2 → 4.4
- Con teléfono: 100%

🎯 Priorización:
- Alta prioridad: 23 leads
- Media prioridad: 41 leads
- Baja prioridad: 23 leads

💾 Archivo generado:
- FILTRADO_CONSOLIDADO_todas_ciudades_20251222_144520.xlsx
- FILTRADO_CONSOLIDADO_todas_ciudades_20251222_144520.csv

💡 Recomendación:
Comienza contactando los 23 leads de ALTA prioridad.
Son negocios bien calificados con buena validación social.
```

## Script de implementación:

```python
import pandas as pd
from datetime import datetime

def filtrar_leads(archivo, rating_min=None, con_telefono=False,
                  con_website=False, ciudad=None, reviews_min=None, top_n=None):
    # Leer archivo
    if archivo.endswith('.csv'):
        df = pd.read_csv(archivo, encoding='utf-8-sig')
    else:
        df = pd.read_excel(archivo)

    original_count = len(df)

    # Aplicar filtros
    if con_telefono:
        df = df[df['phone'].notna() & (df['phone'] != '')]

    if con_website:
        df = df[df['website'].notna() & (df['website'] != '')]

    if rating_min:
        df = df[df['rating'].astype(float) >= rating_min]

    if ciudad:
        df = df[df['ciudad_busqueda'] == ciudad]

    if reviews_min:
        df = df[df['reviews_count'].astype(int) >= reviews_min]

    # Ordenar por rating y reviews
    df = df.sort_values(['rating', 'reviews_count'], ascending=[False, False])

    # Top N si se especifica
    if top_n:
        df = df.head(top_n)

    # Agregar priorización
    def calcular_prioridad(row):
        rating = float(row['rating']) if pd.notna(row['rating']) else 0
        reviews = int(row['reviews_count']) if pd.notna(row['reviews_count']) else 0
        tiene_tel = pd.notna(row['phone']) and row['phone'] != ''

        if rating >= 4.5 and reviews >= 50 and tiene_tel:
            return 'ALTA'
        elif rating >= 4.0 and reviews >= 10 and tiene_tel:
            return 'MEDIA'
        else:
            return 'BAJA'

    df['prioridad'] = df.apply(calcular_prioridad, axis=1)

    # Ordenar por prioridad
    prioridad_orden = {'ALTA': 0, 'MEDIA': 1, 'BAJA': 2}
    df['_orden'] = df['prioridad'].map(prioridad_orden)
    df = df.sort_values('_orden').drop('_orden', axis=1)

    return df, original_count
```

## Notas importantes:

- Siempre hacer backup del archivo original (no sobreescribir)
- Validar que las columnas existen antes de filtrar
- Si un filtro elimina todos los registros, advertir al usuario
- Sugerir ajustar criterios si el filtro es muy estricto
- Incluir estadísticas descriptivas en el Excel generado
