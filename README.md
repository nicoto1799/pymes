# 🤖 Plataforma de Chatbots B2B - PYMEs Colombia

Sistema completo para generar MRR vendiendo chatbots a clínicas y PYMEs en Colombia.

## 📦 Componentes del Proyecto

### 1. 🔍 Google Maps Scraper
Extrae leads B2B de clínicas con datos de contacto (WhatsApp, teléfono, dirección).

### 2. 🤖 Chatbot Platform (n8n-based)
Sistema dual de chatbots SaaS:
- **WhatsApp Bot** - Atiende clientes finales 24/7
- **Internal Chat** - Ayuda al equipo con knowledge base

**Estado:** 569 leads listos + MVP chatbot en desarrollo

---

## 📊 Estado Actual

### Scraper (Componente 1) - ✅ Producción
- **569 leads con WhatsApp** (93.7% tasa de éxito)
- 607 clínicas extraídas en 5 ciudades
- Listo para prospección inmediata

### Chatbot Platform (Componente 2) - 🚧 En Desarrollo
- Arquitectura diseñada (n8n + OpenAI + Twilio)
- Stack definido (ver CHATBOT_PLATFORM.md)
- **Siguiente paso:** Setup n8n local (Semana 1)

### Objetivo 90 Días
- 10-15 clientes pagando
- $2,000-3,000 USD/mes MRR
- 70-80% profit margin

---

## 🚀 Quick Start

### Opción A: Usar Scraper (Generar Más Leads)

```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Prueba rápida (5 resultados)
python3 test_selenium.py

# 3. Búsqueda completa (30-50 resultados)
python3 gmaps_scraper_selenium.py
```

**Resultado:** Archivo Excel con leads listos para prospección

### Opción B: Setup Chatbot Platform (Construir Producto)

```bash
# 1. Setup n8n con Docker
cd n8n
docker-compose up -d

# 2. Acceder a n8n
open http://localhost:5678

# 3. Importar workflows
# Ver: N8N_SETUP_GUIDE.md (paso a paso completo)
```

**Resultado:** Chatbot funcional listo para demos

---

## 📚 Documentación

### Para Prospección (Ventas)
- **GUIA_PROSPECCION_CHATBOTS.md** - Estrategia completa de ventas
- **INSTRUCCIONES.md** - Estado del proyecto y próximos pasos
- **GUIA_RAPIDA.md** - Inicio rápido del scraper

### Para Desarrollo (Técnico)
- **CHATBOT_PLATFORM.md** - Arquitectura completa, workflows, prompts
- **N8N_SETUP_GUIDE.md** - Setup n8n local + Oracle Cloud
- **CLAUDE.md** - Contexto completo para Claude Code

---

## 🔍 Componente 1: Google Maps Scraper

### Características

- ✅ Extrae información pública de Google Maps
- ✅ Exporta a Excel, CSV y JSON
- ✅ Filtra por ciudad, tipo de negocio
- ✅ Incluye teléfonos (WhatsApp), direcciones, sitios web
- ✅ 93.7% de leads incluyen WhatsApp
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

---

## 🤖 Componente 2: Chatbot Platform

### Stack Tecnológico

**Core:**
- **n8n** - Orquestación de workflows (NÚCLEO del sistema)
- **OpenAI GPT-4** - Motor de IA para respuestas
- **Twilio WhatsApp API** - Integración WhatsApp Business
- **PostgreSQL** - Logs de conversaciones + configs
- **Pinecone** - Vector database (knowledge base)
- **Next.js** - Chat interno + Admin dashboard

**Hosting:**
- MVP: Docker local + ngrok ($0-8/mes)
- Producción: Oracle Cloud Free Tier ($0/mes GRATIS FOREVER)

### Arquitectura

```
WhatsApp (Clients) → Twilio → n8n Webhooks
                                  ↓
                           [ n8n Engine ]
                                  ↓
            ┌─────────────────────┼─────────────────────┐
            ↓                     ↓                     ↓
       OpenAI/Claude         Pinecone              PostgreSQL
       (Responses)        (Knowledge Base)      (Conversation Logs)
```

### Workflows Principales (n8n)

1. **whatsapp-client-bot** - Atiende clientes por WhatsApp
   - Clasifica intención (OpenAI)
   - Busca en knowledge base (Pinecone)
   - Genera respuesta personalizada
   - Escala a humano si es necesario

2. **internal-knowledge-chat** - Asiste al equipo
   - Responde preguntas sobre políticas/docs
   - Genera drafts de respuestas para clientes
   - Resume conversaciones

3. **knowledge-base-sync** - Mantiene docs actualizados
   - Ingesta documentos (PDFs, Google Docs)
   - Genera embeddings (OpenAI)
   - Sincroniza con Pinecone

### Costos Operacionales

**MVP (Semanas 1-3):**
- n8n: $0 (local) o $20 (cloud)
- OpenAI API: ~$20-50
- Twilio: ~$20-30 (sandbox testing)
- **Total: $40-100/mes**

**Producción (10 clientes):**
- Infrastructure: $0 (Oracle Free Tier)
- OpenAI API: ~$100-200
- Twilio: ~$100-150
- **Total: $200-350/mes**
- **Revenue: $1,200/mes** (10 clientes × $120)
- **Profit: ~70-80%** 🎯

### Setup Rápido

```bash
# 1. Instalar Docker (si no tienes)
# Mac: https://docs.docker.com/desktop/install/mac-install/

# 2. Crear estructura
cd /Users/nico/Documents/pymes
mkdir -p n8n/workflows

# 3. Seguir guía completa
# Ver: N8N_SETUP_GUIDE.md (30 minutos setup)
```

### Próximos Pasos (Semana 1)

- [ ] Setup n8n local con Docker
- [ ] Configurar Twilio WhatsApp sandbox
- [ ] Crear primer workflow (echo bot)
- [ ] Integrar OpenAI
- [ ] Test end-to-end

**Ver N8N_SETUP_GUIDE.md para instrucciones detalladas paso a paso**

---

## 🎯 Plan de Acción Integrado

### Fase 1: MVP (Semanas 1-3)
1. Setup n8n local ✓ (N8N_SETUP_GUIDE.md)
2. Crear workflows básicos ✓ (CHATBOT_PLATFORM.md)
3. Test con Twilio sandbox
4. Build internal chat UI (Next.js)

### Fase 2: Primeros Clientes (Semanas 4-8)
1. Priorizar 50 mejores leads de los 569 ✓ (ya disponibles)
2. Outreach personalizado (10-15/día)
3. Demos (mostrar chatbot funcionando)
4. Cerrar 2-3 clientes
5. **Meta: $500-800 USD/mes MRR**

### Fase 3: Escala (Semanas 9-16)
1. Migrar a Oracle Cloud (gratis)
2. Multi-tenancy (1 workflow → muchos clientes)
3. Admin dashboard (Retool)
4. 10-15 clientes
5. **Meta: $2,000-3,000 USD/mes MRR**

---

## 📞 Soporte y Recursos

### Documentación
- **README.md** (este archivo) - Overview general
- **CHATBOT_PLATFORM.md** - Arquitectura técnica completa
- **N8N_SETUP_GUIDE.md** - Setup paso a paso
- **GUIA_PROSPECCION_CHATBOTS.md** - Estrategia de ventas
- **CLAUDE.md** - Contexto para Claude Code

### Si tienes problemas:
1. **Scraper:** Ver GUIA_RAPIDA.md
2. **Chatbot:** Ver N8N_SETUP_GUIDE.md sección Troubleshooting
3. **Ventas:** Ver GUIA_PROSPECCION_CHATBOTS.md

### Comandos Rápidos

```bash
# Scraper
source venv/bin/activate
python3 test_selenium.py

# Chatbot Platform
cd n8n
docker-compose up -d  # Iniciar
docker-compose logs -f n8n  # Ver logs
docker-compose down  # Detener
```

---

## 📝 Licencia y Compliance

**Uso:** Personal y comercial permitido

**IMPORTANTE - Aspectos Legales:**
- ✅ Scraper extrae solo información **pública** de Google Maps
- ✅ Para contacto, obtener **consent explícito** (cumplir Habeas Data Colombia)
- ✅ Permitir **opt-out** en cualquier momento
- ❌ NO spam masivo automatizado
- ❌ NO venta de datos personales sin consentimiento

**Cumplimiento:**
- GDPR (Europa) / Habeas Data (Colombia)
- Términos de Servicio de Twilio/WhatsApp
- Rate limits de APIs

---

**Última actualización:** 2026-01-02
**Autor:** Nico
**Proyecto:** Plataforma B2B SaaS - Chatbots para PYMEs Colombia
**Estado:** Scraper en producción (569 leads) + Chatbot MVP en desarrollo
