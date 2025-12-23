# 🚀 Guía Rápida: Comandos Claude Code

## ✅ ¿Qué se instaló?

Se crearon **4 comandos slash** y **1 agente especializado** para automatizar tu flujo de trabajo.

### 📂 Estructura creada:

```
.claude/
├── commands/
│   ├── documentar.md          ✅ Actualizar docs automáticamente
│   ├── scrape-ciudad.md       ✅ Búsqueda rápida por ciudad
│   ├── filtrar-leads.md       ✅ Filtrado inteligente
│   └── analizar-mercado.md    ✅ Análisis competitivo
├── agents/
│   └── lead-researcher.md     ✅ Investigación profunda
└── README.md                  📖 Documentación completa
```

---

## 🎯 Cómo Usar (Copy-Paste)

### 0. Mantener Documentación (NUEVO)

```
/documentar "Descripción de tu cambio"
```

**Uso:** Cada vez que modifiques código, agregues features, o corrijas bugs

---

### 1. Extraer Leads de una Ciudad

```
/scrape-ciudad Medellín "clínica odontológica" 30
```

**Resultado:** Archivos CSV + Excel con 30 clínicas

---

### 2. Filtrar los Mejores Leads

```
/filtrar-leads CONSOLIDADO_todas_ciudades.xlsx
```

Luego selecciona: "Solo con teléfono y rating > 4.0"

**Resultado:** Archivo filtrado con priorización automática

---

### 3. Analizar el Mercado

```
/analizar-mercado LEADS_con_telefono.xlsx
```

**Resultado:**
- Reporte completo en MD
- Excel con análisis
- Estrategia recomendada

---

### 4. Investigar Leads en Profundidad

```
Investiga los top 10 leads de FILTRADO_leads.xlsx
```

**Resultado:**
- Fichas completas de investigación
- Mensajes personalizados
- Score de oportunidad
- Plan de contacto

---

## 💡 Flujo Completo (30 minutos)

### Objetivo: Conseguir 10 leads listos para contactar HOY

```bash
# 1. Extrae leads (5 min)
/scrape-ciudad Medellín "clínica odontológica" 30

# 2. Filtra los mejores (2 min)
/filtrar-leads Medellín_20251222.xlsx
# Selecciona: "Top 20 con teléfono"

# 3. Investiga los top 10 (20 min)
Investiga los top 10 de FILTRADO_Medellín.xlsx

# 4. LISTO!
# Tienes 10 leads con mensajes personalizados
```

**Output:**
- `INVESTIGACION_leads_20251222.xlsx` con todo listo
- Mensajes personalizados para copiar y pegar
- Score de oportunidad para priorizar

---

## 📊 Comando Más Útil: `/analizar-mercado`

Este comando te da inteligencia de mercado ANTES de contactar:

```
/analizar-mercado CONSOLIDADO_todas_ciudades.xlsx
```

**Te dice:**
- ✅ Qué ciudad tiene mejores leads
- ✅ Qué segmento atacar primero (Líderes/Medio/Vulnerables)
- ✅ Tasa de conversión esperada
- ✅ Cuántos contactos hacer por día
- ✅ Estrategia semana por semana

**Usa esto PRIMERO** antes de empezar a contactar.

---

## 🤖 Agente Más Poderoso: Lead Researcher

Convierte un lead frío en prospecto caliente:

**ANTES (sin investigación):**
```
"Hola, ofrezco automatización de WhatsApp para tu clínica"
→ IGNORADO
```

**DESPUÉS (con Lead Researcher):**
```
"Dr. Pérez, vi que varios pacientes mencionan en Google
que a veces tardan en recibir respuesta por WhatsApp.

Trabajo con Clínica Dental X en Laureles automatizando
el agendamiento - los pacientes reservan 24/7 sin esperar.

¿Le interesa ver cómo funciona? (demo de 10 min)"
→ RESPUESTA
```

**Diferencia:**
- Investigación = personalización = respuesta
- Generic pitch = spam = ignorado

---

## 🎯 Casos de Uso Rápidos

### Caso 1: "Necesito 5 clientes esta semana"

```
1. /scrape-ciudad Medellín "clínica odontológica" 50
2. /analizar-mercado Medellín_fecha.xlsx
3. /filtrar-leads Medellín_fecha.xlsx → "Rating < 4.0"
   (Negocios vulnerables = mayor necesidad)
4. Investiga los top 20 de FILTRADO_Medellín.xlsx
5. Contacta 15 por día con mensajes personalizados
```

**Tasa de conversión esperada:** 15-25% en leads vulnerables
**20 contactos × 20% = 4 reuniones = 1-2 cierres**

---

### Caso 2: "Quiero clientes premium"

```
1. python3 buscar_por_ciudades_selenium.py
2. /analizar-mercado CONSOLIDADO_todas_ciudades.xlsx
3. /filtrar-leads CONSOLIDADO → "Top 30 rating > 4.5"
4. Investiga todos los 30 leads
5. Contacta 10 por día (súper personalizados)
```

**Tasa de conversión esperada:** 5-10% en líderes
**30 contactos × 7% = 2-3 reuniones = 1 cierre premium**

---

### Caso 3: "No sé qué nicho atacar"

```
1. /scrape-ciudad Medellín "clínica odontológica" 30
2. /scrape-ciudad Medellín "clínica estética" 30
3. /scrape-ciudad Medellín "consultorio psicológico" 30

4. /analizar-mercado Medellín_odontologica.xlsx
5. /analizar-mercado Medellín_estetica.xlsx
6. /analizar-mercado Medellín_psicologico.xlsx

7. Compara los 3 análisis
8. Elige el que tenga:
   - Más leads con teléfono
   - Más pain points detectables
   - Menos competencia automatizada
```

**Tiempo:** 2 horas
**Output:** Decisión informada de nicho

---

## 📈 Métricas a Trackear

Crea un Google Sheet simple:

| Fecha | Leads Extraídos | Leads Filtrados | Leads Investigados | Contactados | Respuestas | Reuniones | Cierres |
|-------|-----------------|-----------------|-------------------|-------------|------------|-----------|---------|
| 22-Dic | 30 | 20 | 10 | 10 | 3 | 1 | 0 |
| 23-Dic | - | - | 10 | 15 | 5 | 2 | 1 |

**KPIs importantes:**
- **Tasa de respuesta:** Respuestas / Contactados (objetivo: >20%)
- **Tasa de reunión:** Reuniones / Respuestas (objetivo: >30%)
- **Tasa de cierre:** Cierres / Reuniones (objetivo: >30%)

---

## 🚨 Errores Que Debes Evitar

### ❌ Error #1: Extraer masivamente sin plan
```
Usuario: /scrape-ciudad Bogotá "clínica" 200
```
**Problema:** 200 leads genéricos = basura
**Solución:** Búsquedas específicas de 20-30 leads

---

### ❌ Error #2: No filtrar antes de contactar
```
Usuario: Contacto los 133 leads del archivo
```
**Problema:** Pierdes tiempo en leads malos
**Solución:** SIEMPRE filtrar primero

---

### ❌ Error #3: Mensajes genéricos
```
"Hola, ofrezco automatización de WhatsApp"
```
**Problema:** Parece spam
**Solución:** Usa Lead Researcher para personalizar

---

### ❌ Error #4: Contacto masivo en un día
```
Usuario: Envié 50 mensajes hoy
```
**Problema:** Bloqueo de WhatsApp + baja calidad
**Solución:** 10-15 mensajes BIEN HECHOS por día

---

## 💰 ROI Esperado

### Inversión de Tiempo:
- Setup inicial: 30 min (primera vez)
- Por campaña: 2-3 horas (extracción + análisis + investigación)
- Por contacto: 5 min (personalizado)

### Retorno Esperado (conservador):
- 30 leads investigados
- 20 contactados efectivamente
- 4 respuestas (20% tasa)
- 2 reuniones (50% de respuestas)
- 1 cierre (50% de reuniones)

**1 cliente = 800k COP/mes = 9.6M COP/año**

**ROI:** 1 cliente por cada 4 horas invertidas

---

## 🔥 Pro Tips

### Tip #1: Usa el análisis de mercado SIEMPRE
No adivines, deja que los datos te digan qué hacer.

### Tip #2: Investiga solo a los filtrados
No pierdas tiempo investigando leads malos.

### Tip #3: Lee las reseñas de Google
Los pain points están ahí, gratis.

### Tip #4: Contacta Martes-Jueves, 2-4pm
Mejor momento para clínicas (fuera de horas pico).

### Tip #5: Trackea TODO
Si no lo mides, no lo puedes mejorar.

---

## 📚 Documentación Adicional

- **Documentación completa:** `.claude/README.md`
- **Proyecto general:** `CLAUDE.md`
- **Guía rápida scraper:** `GUIA_RAPIDA.md`

---

## ✅ Checklist de Inicio

Hoy mismo puedes:

- [ ] Extraer 30 leads de tu ciudad
  ```
  /scrape-ciudad [TuCiudad] "clínica odontológica" 30
  ```

- [ ] Analizar el mercado
  ```
  /analizar-mercado [archivo.xlsx]
  ```

- [ ] Filtrar los mejores 20
  ```
  /filtrar-leads [archivo.xlsx]
  ```

- [ ] Investigar top 10
  ```
  Investiga los top 10 de [archivo.xlsx]
  ```

- [ ] Contactar 5 leads HOY
  - Usa mensajes personalizados
  - Entre 2-4pm
  - Por WhatsApp

**Tiempo total:** 2-3 horas
**Output:** Primeras conversaciones iniciadas

---

## 🎯 Próximo Paso

**AHORA MISMO:**

```
/scrape-ciudad Medellín "clínica odontológica" 30
```

Presiona Enter y en 5 minutos tienes tus primeros leads.

Luego pregúntame: "¿Qué hago con estos leads?"

---

**Creado:** 2025-12-22
**Comandos:** 4 (/documentar, /scrape-ciudad, /filtrar-leads, /analizar-mercado)
**Agentes:** 1 (Lead Researcher)
**Estado:** ✅ Listo para usar
**Tu primer lead:** A 5 minutos de distancia 🚀
