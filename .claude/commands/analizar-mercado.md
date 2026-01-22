# Analizar Mercado Command

Genera un análisis estadístico completo de un archivo de leads para entender el mercado y la competencia.

## Instrucciones

El usuario te proporcionará:
1. **Archivo de entrada** (CSV o Excel con resultados del scraper)

## Análisis a realizar:

### 1. Resumen General
- Total de negocios analizados
- Distribución por ciudad (si aplica)
- Cobertura de datos (% con teléfono, website, etc.)

### 2. Análisis de Calificaciones
- Rating promedio general
- Distribución de ratings (5 estrellas, 4-5, 3-4, etc.)
- Top 10 mejor calificados
- Identificar outliers (muy alto o muy bajo)

### 3. Análisis de Reseñas
- Promedio de reseñas por negocio
- Distribución de reseñas
- Negocios con más validación social (más reseñas)
- Negocios con poca/ninguna reseña (oportunidad)

### 4. Análisis de Contactabilidad
- % con teléfono (WhatsApp disponible)
- % con website
- % con ambos
- % sin contacto (oportunidad perdida)

### 5. Análisis Competitivo
- Segmentación por nivel de competencia:
  - **Líderes:** Rating > 4.5, Reviews > 50
  - **Competencia Media:** Rating 4.0-4.5, Reviews 10-50
  - **Vulnerables:** Rating < 4.0 o Reviews < 10
- Identificar nichos desatendidos

### 6. Oportunidades de Prospección
- Leads prioritarios (alto rating + contacto)
- Leads de oportunidad (bajo rating = necesitan mejorar)
- Leads nuevos (pocas reseñas = recién abiertos)

### 7. Proyecciones
- Tasa de conversión esperada (basada en promedios)
- Número de contactos recomendados por día
- Timeline estimado de campaña

## Pasos a seguir:

1. **Cargar y validar datos:**
   - Leer archivo CSV o Excel
   - Validar columnas necesarias
   - Limpiar datos faltantes

2. **Calcular estadísticas:**
   - Usar pandas para análisis descriptivo
   - Generar gráficos de distribución (si es posible)
   - Calcular percentiles y cuartiles

3. **Generar reporte:**
   - Crear archivo Markdown con el análisis
   - Crear archivo Excel con tablas dinámicas
   - Incluir recomendaciones accionables

4. **Segmentación estratégica:**
   - Clasificar leads en categorías
   - Sugerir approach de contacto por categoría
   - Priorizar según objetivos de negocio

5. **Visualización:**
   - Tablas resumen en el terminal
   - Archivo Excel con hojas separadas por análisis
   - Archivo de reporte en Markdown

## Ejemplo de uso:

Usuario: `/analizar-mercado LEADS_con_telefono_20251215_111940.xlsx`

Respuesta esperada:
```
📊 ANÁLISIS DE MERCADO
══════════════════════════════════════════

📁 Archivo: LEADS_con_telefono_20251215_111940.xlsx
📍 Registros analizados: 107 negocios

─────────────────────────────────────────
1️⃣ RESUMEN GENERAL
─────────────────────────────────────────
Distribución por ciudad:
  • Medellín:      28 (26%)
  • Cartagena:     27 (25%)
  • Barranquilla:  26 (24%)
  • Cali:          16 (15%)
  • Bogotá:        10 (9%)

Cobertura de datos:
  📞 Con teléfono:   107 (100%)
  🌐 Con website:     71 (66%)
  📍 Con dirección:  107 (100%)

─────────────────────────────────────────
2️⃣ ANÁLISIS DE CALIFICACIONES
─────────────────────────────────────────
Rating promedio: 4.2 ⭐

Distribución:
  ⭐⭐⭐⭐⭐ (5.0):        23 negocios (21%)
  ⭐⭐⭐⭐  (4.0-4.9):   67 negocios (63%)
  ⭐⭐⭐   (3.0-3.9):   15 negocios (14%)
  ⭐⭐    (2.0-2.9):    2 negocios (2%)

🏆 Top 5 mejor calificados:
  1. Clínica Dental Sonrisas - 5.0 (127 reseñas)
  2. Odontología Avanzada - 5.0 (89 reseñas)
  3. Centro Dental Elite - 4.9 (156 reseñas)
  4. Clínica Oral Premium - 4.9 (98 reseñas)
  5. Dental Care Plus - 4.8 (203 reseñas)

─────────────────────────────────────────
3️⃣ ANÁLISIS DE RESEÑAS
─────────────────────────────────────────
Promedio de reseñas: 47.3 por negocio

Distribución:
  • 100+ reseñas:    18 negocios (validación fuerte)
  • 50-99 reseñas:   32 negocios (validación media)
  • 10-49 reseñas:   41 negocios (validación baja)
  • < 10 reseñas:    16 negocios (negocios nuevos)

─────────────────────────────────────────
4️⃣ SEGMENTACIÓN COMPETITIVA
─────────────────────────────────────────

🥇 LÍDERES (Rating > 4.5, Reviews > 50)
   • Cantidad: 28 negocios
   • Approach: Difícil convencer, pero alto prestigio
   • Mensaje: "Mejore aún más su servicio 5 estrellas"

🥈 COMPETENCIA MEDIA (Rating 4.0-4.5, Reviews 10-50)
   • Cantidad: 51 negocios
   • Approach: Balance perfecto - necesitan mejorar
   • Mensaje: "Alcance el nivel de los líderes"

🥉 VULNERABLES (Rating < 4.0 o Reviews < 10)
   • Cantidad: 28 negocios
   • Approach: Mayor necesidad, más receptivos
   • Mensaje: "Recupere la confianza de sus pacientes"

─────────────────────────────────────────
5️⃣ OPORTUNIDADES DE PROSPECCIÓN
─────────────────────────────────────────

✅ PRIORIDAD ALTA (28 leads)
   • Criterio: Rating > 4.5, >50 reviews, tiene teléfono
   • Potencial: Alto valor, difícil cierre
   • Tasa conversión esperada: 5-10%

🎯 PRIORIDAD MEDIA (51 leads)
   • Criterio: Rating 4.0-4.5, tiene teléfono
   • Potencial: Mejor balance esfuerzo/retorno
   • Tasa conversión esperada: 10-15%

🔥 OPORTUNIDAD (28 leads)
   • Criterio: Rating < 4.0 o pocas reseñas
   • Potencial: Mayor necesidad = mayor interés
   • Tasa conversión esperada: 15-25%

─────────────────────────────────────────
6️⃣ PROYECCIONES Y RECOMENDACIONES
─────────────────────────────────────────

📊 Proyección de campaña:
   • Leads totales: 107
   • Contacto diario recomendado: 15-20 leads
   • Duración campaña: 5-7 días

   Conversión esperada (promedio 12%):
   • Respuestas esperadas: 12-13 negocios
   • Reuniones esperadas: 5-6 negocios
   • Cierres esperados: 1-2 clientes

💰 ROI Proyectado:
   • Con 2 clientes @ 800k COP/mes: 1.6M COP/mes
   • Inversión de tiempo: ~10 horas
   • ROI: 160k COP por hora invertida

🎯 ESTRATEGIA RECOMENDADA:

Semana 1: Probar con segmento VULNERABLE
  → Contactar 20 leads de baja calificación
  → Mensaje: "Mejore su reputación online"
  → Ajustar pitch según respuestas

Semana 2: Escalar a segmento MEDIO
  → Contactar 30-40 leads competencia media
  → Mensaje refinado según aprendizajes
  → Objetivo: 2-3 reuniones agendadas

Semana 3: Atacar segmento LÍDER (opcional)
  → Solo si pitch está perfecto
  → Contactar 15-20 líderes selectos
  → Mensaje premium, casos de éxito

─────────────────────────────────────────
💾 ARCHIVOS GENERADOS
─────────────────────────────────────────

✅ ANALISIS_mercado_20251222_150234.md
   → Reporte completo en Markdown

✅ ANALISIS_mercado_20251222_150234.xlsx
   → Excel con hojas separadas:
     - Resumen General
     - Top Performers
     - Segmentación
     - Leads Priorizados

✅ LEADS_PRIORIZADOS_20251222_150234.xlsx
   → Archivo listo para campaña con columnas:
     - prioridad (ALTA/MEDIA/BAJA)
     - segmento (LIDER/MEDIO/VULNERABLE)
     - mensaje_sugerido
     - orden_contacto

─────────────────────────────────────────
💡 PRÓXIMO PASO
─────────────────────────────────────────

Abre el archivo LEADS_PRIORIZADOS_*.xlsx y comienza
contactando en el orden sugerido.

¿Quieres que genere plantillas de mensajes
personalizadas para cada segmento?
```

## Script de implementación:

```python
import pandas as pd
import numpy as np
from datetime import datetime

def analizar_mercado(archivo):
    # Leer datos
    if archivo.endswith('.csv'):
        df = pd.read_csv(archivo, encoding='utf-8-sig')
    else:
        df = pd.read_excel(archivo)

    # Análisis completo...
    # (Ver código completo en el comando)

    # Generar reportes
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Reporte MD
    with open(f'ANALISIS_mercado_{timestamp}.md', 'w') as f:
        f.write(reporte_markdown)

    # Excel con análisis
    with pd.ExcelWriter(f'ANALISIS_mercado_{timestamp}.xlsx') as writer:
        resumen.to_excel(writer, sheet_name='Resumen', index=False)
        top_performers.to_excel(writer, sheet_name='Top Performers', index=False)
        segmentacion.to_excel(writer, sheet_name='Segmentación', index=False)

    # Leads priorizados
    df_priorizado.to_excel(f'LEADS_PRIORIZADOS_{timestamp}.xlsx', index=False)

    return estadisticas
```

## Notas importantes:

- El análisis debe ser accionable, no solo descriptivo
- Incluir siempre recomendaciones específicas
- Adaptar el mensaje según el segmento identificado
- Considerar el contexto colombiano (ciudades, cultura)
- Sugerir siguiente paso concreto al finalizar
