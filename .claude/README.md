# Comandos y Agentes de Claude Code

Esta carpeta contiene comandos slash personalizados y agentes especializados para optimizar el flujo de trabajo del Google Maps Scraper.

## 📂 Estructura

```
.claude/
├── commands/           # Comandos slash (/)
│   ├── scrape-ciudad.md
│   ├── filtrar-leads.md
│   └── analizar-mercado.md
├── agents/            # Agentes especializados
│   └── lead-researcher.md
└── README.md          # Este archivo
```

## 🚀 Comandos Slash Disponibles

### `/documentar` - Actualizar documentación fácilmente

Mantén la documentación sincronizada cuando hagas cambios al proyecto.

**Uso:**
```
/documentar "Agregué validación de teléfonos colombianos"
```

O simplemente:
```
/documentar
```

**Funcionalidad:**
- Auto-detecta archivos modificados
- Pregunta qué tipo de cambio hiciste
- Actualiza todos los archivos relevantes automáticamente
- Verifica consistencia
- Actualiza fechas y contadores

**Casos de uso:**
- Nuevo feature → Actualiza claude.md, README.md
- Bug fix → Actualiza "Solución de Problemas"
- Nuevo comando → Actualiza todas las guías
- Nueva dependencia → Actualiza requirements.txt docs

**Ahorro de tiempo:** 90% (de 20 min a 2 min)

---

### `/scrape-ciudad` - Búsqueda rápida en una ciudad

Ejecuta scraping en una ciudad específica sin escribir código.

**Uso:**
```
/scrape-ciudad Medellín "clínica odontológica" 30
```

**Parámetros:**
- Ciudad (ej: Medellín, Bogotá, Cali)
- Tipo de negocio (entre comillas)
- Cantidad de resultados (opcional, default: 30)

**Output:**
- `{Ciudad}_{Fecha}.csv`
- `{Ciudad}_{Fecha}.xlsx`
- Resumen en consola

---

### `/filtrar-leads` - Filtrado inteligente de resultados

Filtra y prioriza leads según criterios específicos.

**Uso:**
```
/filtrar-leads CONSOLIDADO_todas_ciudades.xlsx
```

**Criterios disponibles:**
- Rating mínimo (ej: 4.0)
- Solo con teléfono
- Solo con website
- Ciudad específica
- Reviews mínimas
- Top N mejores

**Output:**
- `FILTRADO_{archivo}_{timestamp}.xlsx`
- `FILTRADO_{archivo}_{timestamp}.csv`
- Estadísticas de filtrado
- Priorización automática (ALTA/MEDIA/BAJA)

**Ejemplo interactivo:**
```
Usuario: /filtrar-leads CONSOLIDADO_todas_ciudades.xlsx

Claude: 📋 Archivo encontrado: 133 registros

¿Qué filtros quieres aplicar?

1. Solo con teléfono y rating > 4.0 (prospección prioritaria)
2. Top 30 mejor calificados con teléfono (campaña selecta)
3. Ciudad específica
4. Criterios personalizados

Usuario: 1

Claude: [Ejecuta filtrado y genera archivo...]
```

---

### `/analizar-mercado` - Análisis de competencia

Genera análisis estadístico completo de un archivo de leads.

**Uso:**
```
/analizar-mercado LEADS_con_telefono.xlsx
```

**Análisis incluidos:**
- Resumen general y cobertura
- Distribución de ratings
- Análisis de reseñas
- Segmentación competitiva (Líderes/Medio/Vulnerables)
- Oportunidades de prospección
- Proyecciones de conversión
- Estrategia recomendada

**Output:**
- `ANALISIS_mercado_{timestamp}.md` (reporte completo)
- `ANALISIS_mercado_{timestamp}.xlsx` (tablas y gráficos)
- `LEADS_PRIORIZADOS_{timestamp}.xlsx` (listo para campaña)

**Ventaja:** Convierte datos en estrategia accionable.

---

## 🤖 Agentes Especializados

### Lead Researcher Agent

Investiga leads en profundidad antes de contactarlos.

**Uso:**
```
Investiga el lead: Clínica Dental Sonrisas - Medellín
```

O para múltiples leads:
```
Investiga los 10 leads con mejor rating de FILTRADO_leads.xlsx
```

**Proceso de investigación:**

1. **Validación básica**
   - Verifica que el negocio siga activo
   - Confirma datos de contacto

2. **Análisis de website**
   - Tecnologías que usan
   - Chatbot existente
   - Sistema de automatización actual

3. **Análisis de redes sociales**
   - Presencia en Instagram/Facebook
   - Velocidad de respuesta
   - Engagement

4. **Análisis de reseñas**
   - Pain points recurrentes
   - Fortalezas mencionadas
   - Oportunidades de mejora

5. **Búsqueda de decisor**
   - Nombre del propietario/gerente
   - Contacto en LinkedIn
   - Quién toma decisiones

6. **Generación de inteligencia**
   - Score de oportunidad (1-5 ⭐)
   - Mensaje personalizado
   - Objeciones probables + respuestas
   - Mejor momento de contacto

**Output:**

Para cada lead:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 CLÍNICA DENTAL SONRISAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Medellín, El Poblado
⭐ 4.7 (127 reseñas)
📞 +57 300 123 4567

👤 DECISOR: Dr. Juan Pérez - Director

🎯 OPORTUNIDAD: ⭐⭐⭐⭐⭐ ALTO

Pain points detectados:
• Tardan en responder WhatsApp (3 menciones)
• Difícil agendar cita (2 menciones)

💬 MENSAJE PERSONALIZADO:
[Mensaje listo para copiar y enviar]

📅 CONTACTAR: Mar-Jue, 2-4pm
📱 CANAL: WhatsApp
```

Archivo Excel con todos los leads investigados.

---

## 🎯 Flujo de Trabajo Recomendado

### 1. Extracción de Leads

```bash
# Opción A: Una ciudad específica
/scrape-ciudad Medellín "clínica odontológica" 30

# Opción B: Múltiples ciudades (usar script existente)
python3 buscar_por_ciudades_selenium.py
```

**Resultado:** Archivos CSV/Excel con leads crudos

---

### 2. Análisis de Mercado

```bash
/analizar-mercado CONSOLIDADO_todas_ciudades.xlsx
```

**Resultado:**
- Entiendes el mercado
- Identificas segmentos
- Tienes estrategia clara

---

### 3. Filtrado y Priorización

```bash
/filtrar-leads CONSOLIDADO_todas_ciudades.xlsx
```

Seleccionar criterios según tu objetivo:
- **Campaña agresiva:** Solo rating > 4.0 con teléfono
- **Campaña premium:** Top 20 mejor calificados
- **Oportunidades:** Rating < 4.0 (necesitan mejorar)

**Resultado:** Archivo filtrado y priorizado

---

### 4. Investigación en Profundidad

```bash
Investiga los 15 leads de ALTA prioridad de LEADS_PRIORIZADOS.xlsx
```

**Resultado:**
- Fichas de investigación completas
- Mensajes personalizados listos
- Estrategia de contacto por lead

---

### 5. Ejecución de Campaña

Con los archivos generados:
1. Abre `INVESTIGACION_leads_{timestamp}.xlsx`
2. Ordena por `oportunidad_score` (5 → 1)
3. Copia el `mensaje_personalizado`
4. Contacta en el `mejor_horario_contacto`
5. Usa las `respuestas_preparadas` para objeciones

**Ritmo recomendado:** 10-15 contactos por día

---

## 💡 Casos de Uso

### Caso 1: Campaña Rápida (1 día)

```bash
# 1. Extrae leads de una ciudad
/scrape-ciudad Medellín "clínica odontológica" 30

# 2. Filtra los mejores
/filtrar-leads Medellín_20251222.xlsx
# Seleccionar: "Top 20 con teléfono"

# 3. Investiga top 10
Investiga los top 10 de FILTRADO_Medellín.xlsx

# 4. Contacta
# Usa mensajes personalizados generados
```

**Tiempo total:** 3-4 horas
**Output:** 10 leads investigados listos para contacto

---

### Caso 2: Campaña Multi-Ciudad (3 días)

```bash
# Día 1: Extracción
python3 buscar_por_ciudades_selenium.py

# Día 2: Análisis y filtrado
/analizar-mercado CONSOLIDADO_todas_ciudades.xlsx
/filtrar-leads CONSOLIDADO_todas_ciudades.xlsx

# Día 3: Investigación
Investiga los 30 leads de ALTA prioridad de LEADS_PRIORIZADOS.xlsx

# Días 4-5: Contacto
# 15 leads por día
```

**Tiempo total:** 5 días
**Output:** 30 leads premium investigados

---

### Caso 3: Análisis de Nicho

```bash
# 1. Extrae varias verticales
/scrape-ciudad Medellín "clínica odontológica" 30
/scrape-ciudad Medellín "clínica estética" 30
/scrape-ciudad Medellín "consultorio psicológico" 30

# 2. Analiza cada vertical
/analizar-mercado Medellín_odontologica.xlsx
/analizar-mercado Medellín_estetica.xlsx
/analizar-mercado Medellín_psicologico.xlsx

# 3. Elige el nicho con mejor oportunidad
# (Menor competencia, más pain points, etc.)
```

**Tiempo total:** 1 día
**Output:** Identificación del nicho más prometedor

---

## 📈 Métricas de Éxito

Trackea estos indicadores:

### En Extracción:
- Leads extraídos
- % con teléfono
- % con website
- Rating promedio

### En Filtrado:
- Leads ALTA prioridad
- Leads MEDIA prioridad
- % descartados

### En Investigación:
- Leads investigados
- Score promedio de oportunidad
- Pain points identificados

### En Campaña:
- Mensajes enviados
- Tasa de respuesta
- Reuniones agendadas
- Cierres

---

## 🛠️ Tips y Mejores Prácticas

### Para `/scrape-ciudad`:
- Usa búsquedas específicas: "clínica odontológica" mejor que "clínica"
- 20-30 resultados es ideal (calidad > cantidad)
- Una ciudad a la vez para mejor control

### Para `/filtrar-leads`:
- Comienza con filtros amplios, luego refina
- Siempre incluye "con teléfono" (sin teléfono = no contactable)
- Rating > 4.0 es sweet spot (necesitan mejorar pero son serios)

### Para `/analizar-mercado`:
- Úsalo ANTES de filtrar para entender el panorama
- Presta atención a la segmentación competitiva
- Sigue las recomendaciones de estrategia

### Para Lead Researcher:
- Investiga SOLO leads ya filtrados (no pierdas tiempo)
- Lee los pain points de las reseñas (oro puro)
- Personaliza cada mensaje (no copies y pegues)
- Contacta en el horario sugerido

---

## 🚨 Errores Comunes

### ❌ Scraping masivo sin análisis
- Extraes 500 leads pero no sabes qué hacer con ellos
- **Solución:** Analiza primero, extrae después

### ❌ Filtros muy restrictivos
- Solo quedan 3 leads después de filtrar
- **Solución:** Balancea criterios, 20-30 leads es ideal

### ❌ No investigar antes de contactar
- Mensaje genérico = ignorado
- **Solución:** Usa Lead Researcher al menos para top 20

### ❌ Contacto masivo despersonalizado
- Spam = bloqueo + mala reputación
- **Solución:** 10-15 mensajes PERSONALIZADOS por día

---

## 🔄 Actualizaciones

**2025-12-22:**
- ✅ Comandos slash iniciales creados
- ✅ Lead Researcher agent implementado
- ✅ Comando /documentar agregado
- 🔄 Próximamente: Más agentes especializados

**Roadmap:**
- Data Validator Agent (validar teléfonos, URLs)
- Campaign Generator Agent (crear flujos de seguimiento)
- Export Optimizer Agent (integrar con CRMs)

---

## 📞 Soporte

Si encuentras bugs o tienes sugerencias:
1. Revisa este README primero
2. Consulta el CLAUDE.md principal
3. Experimenta con los comandos (no rompes nada)

---

**Última actualización:** 2025-12-22
**Comandos disponibles:** 4 (/documentar, /scrape-ciudad, /filtrar-leads, /analizar-mercado)
**Agentes disponibles:** 1 (Lead Researcher)
**Estado:** ✅ Producción
