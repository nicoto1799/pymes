# Proyecto: Plataforma de Chatbots B2B para PYMEs Colombia

## 🎯 Objetivo del Proyecto

Este proyecto consta de **dos componentes integrados**:

1. **Google Maps Scraper** - Extrae leads B2B de clínicas y PYMEs en Colombia
2. **Plataforma de Chatbots** - Sistema dual de chatbots (WhatsApp para clientes + Chat interno para equipos)

**Modelo de negocio:** Generar MRR (Monthly Recurring Revenue) vendiendo chatbots como servicio SaaS a clínicas, consultorios y PYMEs en Colombia.

**Estado actual:**
- ✅ Scraper funcionando - 569 leads con WhatsApp listos
- 🚧 Chatbot platform - En desarrollo (Fase MVP)
- 🎯 Objetivo 90 días: 10-15 clientes pagando ($2-3K USD/mes MRR)

## Resumen del Proyecto

Scraper web automatizado que extrae información pública de negocios en Google Maps, enfocado en clínicas odontológicas, estéticas, médicas y otros negocios de servicios en Colombia. Genera bases de datos con datos de contacto (especialmente teléfonos de WhatsApp) para prospección comercial de chatbots y automatización.

## Tecnologías Principales

### Scraper (Componente 1)
- **Python 3.12**
- **Selenium** (scraper principal - RECOMENDADO)
- **Playwright** (implementación alternativa - tiene bugs)
- **Pandas** para procesamiento de datos
- **OpenPyXL** para exportación a Excel

### Chatbot Platform (Componente 2)
- **n8n** (orquestación de workflows - NÚCLEO del sistema)
- **OpenAI GPT-4** / **Claude API** (motor de IA)
- **Twilio WhatsApp API** (integración WhatsApp Business)
- **PostgreSQL** (logs de conversaciones + configs)
- **Pinecone** (vector database para knowledge base)
- **Next.js** (interfaz de chat interno + admin dashboard)
- **Docker** (deployment)

## Estructura del Proyecto

```
pymes/
├── 📁 SCRAPER (Componente 1 - Lead Generation)
│   ├── gmaps_scraper_selenium.py           # ⭐ SCRAPER PRINCIPAL (usar este)
│   ├── test_selenium.py                    # Script de prueba rápida (5 resultados)
│   ├── buscar_por_ciudades_selenium.py     # ⭐ Script múltiples ciudades
│   ├── buscar_clinicas.py                  # Script ejemplo (Playwright - obsoleto)
│   ├── gmaps_scraper.py                    # Versión Playwright (NO USAR)
│   ├── requirements.txt                    # Dependencias Python
│   └── resultados/                         # 📁 Extracciones organizadas
│       ├── 2024-12-15_primera_extraccion/  # 133 clínicas
│       └── 2024-12-22_extraccion_ampliada/ # 607 clínicas (569 con WhatsApp)
│
├── 📁 CHATBOT PLATFORM (Componente 2 - Producto a Vender)
│   ├── n8n/                               # 🚧 Workflows n8n
│   │   ├── workflows/                     # Workflows exportados (.json)
│   │   │   ├── whatsapp-client-bot.json   # Bot externo (clientes)
│   │   │   ├── internal-knowledge-chat.json # Chat interno (equipo)
│   │   │   └── knowledge-base-sync.json    # Sincronización de docs
│   │   ├── docker-compose.yml             # Setup n8n + PostgreSQL
│   │   └── .env.example                   # Variables de entorno
│   │
│   ├── web-interface/                     # 🚧 Chat interno (Next.js)
│   │   ├── app/                           # Next.js 14 app router
│   │   ├── components/                    # Componentes UI
│   │   ├── public/                        # Assets
│   │   └── package.json                   # Dependencies
│   │
│   └── knowledge-base/                    # 📚 Documentos para clientes
│       ├── templates/                     # Templates por industria
│       │   ├── clinica-odontologica/      # FAQs clínicas dentales
│       │   ├── clinica-estetica/          # FAQs estética
│       │   └── general/                   # FAQs genéricas
│       └── docs/                          # Documentos compartidos
│
├── 📁 DOCUMENTACIÓN
│   ├── README.md                          # Documentación técnica general
│   ├── CLAUDE.md                          # Este archivo - Contexto para Claude
│   ├── CHATBOT_PLATFORM.md                # 🆕 Arquitectura completa chatbot
│   ├── N8N_SETUP_GUIDE.md                 # 🆕 Guía setup n8n paso a paso
│   ├── GUIA_PROSPECCION_CHATBOTS.md       # Guía de ventas y prospección
│   ├── GUIA_RAPIDA.md                     # Inicio rápido scraper
│   └── INSTRUCCIONES.md                   # Estado del proyecto
│
├── .claude/                               # Comandos y agentes Claude Code
│   ├── commands/                          # Slash commands personalizados
│   └── agents/                            # Agentes especializados
│
└── venv/                                  # Entorno virtual Python (scraper)
```

## Archivos Clave

### `gmaps_scraper_selenium.py` (PRINCIPAL)
- **Clase:** `GoogleMapsScraperSelenium`
- **Motor:** Selenium + Chrome WebDriver
- **Estado:** ✅ Funcionando correctamente
- **Uso:** Scraper principal de producción

**Métodos principales:**
- `setup_driver()`: Configura Chrome con opciones anti-detección
- `search_places(query, max_results=50, scroll_attempts=10)`: Búsqueda principal
- `_scroll_results(attempts)`: Hace scroll para cargar más resultados
- `_extract_data(max_results)`: Extrae datos de los lugares
- `_extract_place_details()`: Extrae detalles individuales de cada negocio
- `save_to_excel(filename)`: Exporta a Excel
- `save_to_csv(filename)`: Exporta a CSV
- `save_to_json(filename)`: Exporta a JSON
- `print_summary()`: Muestra resumen de resultados

**Configuración:**
- `headless=False`: Muestra el navegador (útil para debugging)
- `headless=True`: Modo oculto (para producción)

### `test_selenium.py`
- Script de prueba rápida
- Extrae solo 5 resultados
- Útil para validar que todo funciona
- Genera: `test_selenium_resultados.xlsx`

### `buscar_clinicas.py`
- Script ejemplo para búsqueda única
- ⚠️ Usa Playwright (versión obsoleta)
- Incluye filtrado de leads con teléfono

### `buscar_por_ciudades_selenium.py` (RECOMENDADO)
- ⭐ Script para búsquedas múltiples por ciudad con Selenium
- Automatiza búsquedas en 5 ciudades principales
- Genera archivos Excel separados por ciudad
- Genera archivo consolidado y leads con teléfono
- Genera resumen estadístico por ciudad
- Configuración en variables al inicio del archivo

### `test_scraper.py`
- ⚠️ Script de prueba con Playwright (obsoleto)
- Solo usar si necesitas probar Playwright
- Preferir `test_selenium.py` en su lugar

## Datos Extraídos

Cada registro incluye:

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `name` | Nombre del negocio | Identificación |
| `category` | Categoría (ej: "Clínica odontológica") | Segmentación |
| `rating` | Calificación (0-5 estrellas) | Priorización de leads |
| `reviews_count` | Número de reseñas | Validación social |
| `address` | Dirección completa | Geolocalización |
| `phone` | ⭐ Teléfono | Contacto por WhatsApp |
| `website` | Sitio web | Investigación previa |
| `hours` | Horarios de atención | Planificación de contacto |
| `extracted_at` | Fecha/hora de extracción | Trazabilidad |

## Instalación

### Método 1: Script automático (Mac/Linux)
```bash
./setup.sh
source venv/bin/activate
```

### Método 2: Manual
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Uso Básico

### Prueba Rápida (5 resultados)
```bash
source venv/bin/activate
python3 test_selenium.py
```

### Búsqueda Completa (30-50 resultados)
```python
from gmaps_scraper_selenium import GoogleMapsScraperSelenium
from datetime import datetime

scraper = GoogleMapsScraperSelenium(headless=False)

results = scraper.search_places(
    query="clínica odontológica Medellín",
    max_results=30,
    scroll_attempts=5
)

scraper.print_summary()
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
scraper.save_to_csv(f'resultados_{timestamp}.csv')        # CSV automático
scraper.save_to_excel(f'resultados_{timestamp}.xlsx')     # Excel automático
```

## Ejemplos de Búsquedas

### Clínicas Odontológicas
```python
queries = [
    "clínica odontológica Medellín",
    "clínica odontológica Bogotá",
    "clínica odontológica Cali",
]
```

### Clínicas Estéticas
```python
queries = [
    "clínica estética Medellín",
    "medicina estética Bogotá",
    "cirugía estética Cali",
]
```

### Otras Especialidades
```python
queries = [
    "oftalmología Medellín",
    "ortopedia Bogotá",
    "dermatología Cali",
    "consultorio psicológico Medellín",
]
```

## Filtrado de Resultados

### Leads con teléfono (WhatsApp)
```python
# Filtrar solo negocios con teléfono
with_phone = [r for r in scraper.results if r.get('phone')]
print(f"Leads con teléfono: {len(with_phone)}")

# Guardar filtrado
import pandas as pd
df = pd.DataFrame(with_phone)
df.to_csv('leads_con_telefono.csv', index=False, encoding='utf-8-sig')
df.to_excel('leads_con_telefono.xlsx', index=False)
```

### Ordenar por rating
```python
# Mejores calificaciones primero
leads_sorted = sorted(
    scraper.results,
    key=lambda x: float(x.get('rating') or 0),
    reverse=True
)
```

## Parámetros de Configuración

### `search_places()`

| Parámetro | Descripción | Default | Recomendado |
|-----------|-------------|---------|-------------|
| `query` | Término de búsqueda | - | "clínica odontológica [Ciudad]" |
| `max_results` | Máximo de resultados | 50 | 20-50 |
| `scroll_attempts` | Intentos de scroll | 10 | 5-15 |

**Relación scroll_attempts / resultados:**
- 5 scrolls: ~20-30 resultados
- 10 scrolls: ~40-60 resultados
- 15 scrolls: ~60-100 resultados

## Mejores Prácticas

### ✅ Hacer
- Búsquedas específicas por ciudad
- Una ciudad a la vez
- Máximo 50 resultados por búsqueda
- Revisar manualmente antes de contactar
- Contacto personalizado 1 a 1
- Máximo 10-20 mensajes por día
- Respetar tiempos entre búsquedas (5-10 seg)

### ❌ NO Hacer
- Búsquedas muy amplias ("clínica Colombia")
- Spam masivo automatizado
- Más de 100 resultados de una vez
- Scraping intensivo sin pausas
- Violación de Habeas Data / GDPR

## Aspectos Técnicos

### Selenium - Configuración Anti-Detección
```python
# Ocultar webdriver
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# User agent real
chrome_options.add_argument('user-agent=Mozilla/5.0 ...')

# JavaScript para ocultar webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```

### Selectores CSS Utilizados

| Elemento | Selector | Observaciones |
|----------|----------|---------------|
| Lista resultados | `div[role="feed"]` | Contenedor scrollable |
| Enlaces lugares | `a[href*="/maps/place/"]` | Todos los lugares |
| Nombre | `h1` | Título principal |
| Rating | `div[role="img"][aria-label*="estrellas"]` | Aria-label con rating |
| Categoría | `button[jsaction*="category"]` | Botón de categoría |
| Dirección | `button[data-item-id="address"]` | Data-item-id específico |
| Teléfono | `button[data-item-id*="phone"]` | Buscar por data-item-id |
| Sitio web | `a[data-item-id="authority"]` | Link autoridad |
| Horarios | `button[data-item-id*="oh"]` | "oh" = opening hours |

### Limpieza de Datos

```python
# Teléfonos
def clean_phone(phone):
    # Elimina todo excepto dígitos y +
    return re.sub(r'[^\d+]', '', phone)

# Texto general
def clean_text(text):
    # Elimina espacios múltiples y saltos de línea
    return " ".join(text.split())
```

## 🎯 Caso de Uso Principal: Venta de Chatbots

### Objetivo Comercial
Generar **MRR (Monthly Recurring Revenue)** vendiendo chatbots de WhatsApp a clínicas y PYMEs en Colombia.

### Flujo de Trabajo

1. **Extracción** → Ejecutar scraper por ciudad/nicho
2. **Filtrado** → Seleccionar leads con teléfono + buen rating
3. **Investigación** → Revisar reseñas buscando quejas de atención
4. **Prospección** → Contacto personalizado vía WhatsApp (10-15/día)
5. **Demo** → Mostrar chatbot funcionando (15 min)
6. **Cierre** → Venta del servicio mensual
7. **Escala** → Repetir en más ciudades/nichos

### Perfil del Cliente Ideal (ICP)
- **Sector:** Clínicas odontológicas, estéticas, médicas
- **Indicadores:**
  - ✅ 50-300 reseñas (alto volumen de clientes)
  - ✅ Rating 4.0-4.5 (tienen demanda pero pueden mejorar)
  - ✅ Teléfono visible (usan WhatsApp activamente)
  - ⚠️ Quejas sobre "no responden" o "difícil agendar"

### Métricas Esperadas
- **Tasa de respuesta:** 15-25% (con mensajes personalizados)
- **Demos agendadas:** 3-5 por semana
- **Tasa de conversión:** 20-30% (de demo a venta)
- **Meta 90 días:** 10-15 clientes pagando ($2-3K USD/mes MRR)

**📖 Ver `GUIA_PROSPECCION_CHATBOTS.md` para el plan completo paso a paso**

---

## Otros Casos de Uso

### 2. Análisis de Mercado
- Extraer competidores por ciudad
- Comparar ratings y reviews
- Identificar gaps de mercado

### 3. Expansión a Otros Nichos
- Clínicas estéticas (botox, rellenos)
- Spas y centros de belleza
- Veterinarias
- Gimnasios
- Restaurantes (reservas)

Todos necesitan: agendar citas + responder consultas = **chatbot**

## Solución de Problemas

### Error: "playwright not found"
```bash
pip install playwright
playwright install chromium
```

### Error: "Chrome driver not found"
```bash
pip install webdriver-manager
# Se instala automáticamente al ejecutar
```

### Pocos resultados
- Aumentar `scroll_attempts` a 15-20
- Verificar conexión a internet
- Usar búsquedas más amplias

### Navegador se cierra solo
- Normal si terminó la búsqueda
- Revisar archivo Excel generado
- Verificar errores en consola

### Rate limiting / Bloqueos
- Reducir velocidad de scroll
- Aumentar tiempos de espera
- Cambiar IP si es necesario

## Consideraciones Legales

### ✅ Legal
- Extrae información **pública** de Google Maps
- Uso para contacto **personalizado** y relevante
- Respeta rate limits y robots.txt
- Respeta opt-outs de contacto

### ⚠️ Zona Gris
- Scraping intensivo puede violar TOS de Google
- Usar con moderación

### ❌ Ilegal
- Envío masivo de spam
- Violación de Habeas Data (Colombia) / GDPR (Europa)
- Venta de datos personales sin consentimiento
- Automatización abusiva

## Roadmap Sugerido

### Semana 1: Validación
- Extraer 100-200 leads
- Contactar 10-15 por día
- Probar mensajes diferentes
- Ajustar pitch

### Semana 2-3: Escala
- 20-30 contactos diarios
- Cerrar primeros clientes
- Recopilar testimoniales

### Mes 2+: Crecimiento
- Contratar comercial/socio
- Automatizar workflow
- Expandir a otras ciudades

## Proyecciones Realistas

### Extracción
- **Por hora:** 50-100 leads
- **Por día:** 200-500 leads
- **Con teléfono:** ~60-70% del total

### Conversión Esperada
- 100 contactos → 15 respuestas → 5 reuniones → 1-2 clientes

### ROI
- Inversión: ~30 min setup + 5-10 min/búsqueda
- Retorno: 1 cliente = 400k-1.2M COP/mes
- Con 10 clientes = 4M-12M COP/mes

## Dependencias (requirements.txt)

```txt
playwright==1.40.0
pandas==2.1.4
python-dotenv==1.0.0
openpyxl==3.1.2
selenium==4.16.0
webdriver-manager==4.0.1
```

## Estado Actual del Proyecto

### ✅ Funcionalidades Completas
- ✅ Selenium scraper funcionando correctamente
- ✅ Extracción masiva: 607 clínicas en 5 ciudades (2024-12-22)
- ✅ Tasa de éxito: **93.7% con teléfono** (569/607 leads)
- ✅ Exportación a Excel/CSV/JSON funcional
- ✅ Script multi-ciudad con consolidación automática
- ✅ Organización automática en carpetas por fecha
- ✅ Comandos slash y agentes de Claude Code implementados
- ✅ Guía completa de prospección y ventas
- ✅ Fix de permisos chromedriver automático

### ⚠️ Limitaciones Conocidas
- ❌ Playwright scraper tiene bugs (usar Selenium)
- ⚠️ Google Maps limita ~120 resultados únicos por búsqueda/ciudad
- ⚠️ Scraping intensivo puede provocar bloqueos temporales (usar pausas)

### 📊 Datos Actuales Disponibles
- **2024-12-15:** 133 clínicas (primera extracción, ~30/ciudad)
- **2024-12-22:** 607 clínicas (extracción ampliada, ~120/ciudad)
- **Total único:** ~650 leads con teléfono listos para prospección

## 📁 Estructura de Resultados

Todos los archivos están organizados en carpetas por fecha:

```
resultados/
├── 2024-12-15_primera_extraccion/
│   ├── Medellín_20251215.xlsx/csv (30 clínicas)
│   ├── Bogotá_20251215.xlsx/csv (20 clínicas)
│   ├── Cali_20251215.xlsx/csv (25 clínicas)
│   ├── Barranquilla_20251215.xlsx/csv (28 clínicas)
│   ├── Cartagena_20251215.xlsx/csv (30 clínicas)
│   ├── CONSOLIDADO_todas_ciudades_*.xlsx/csv (133 total)
│   ├── LEADS_con_telefono_*.xlsx/csv (solo con WhatsApp)
│   └── RESUMEN_por_ciudad_*.xlsx/csv (estadísticas)
│
└── 2024-12-22_extraccion_ampliada/
    ├── Medellín_20251222.xlsx/csv (122 clínicas)
    ├── Bogotá_20251222.xlsx/csv (122 clínicas)
    ├── Cali_20251222.xlsx/csv (120 clínicas)
    ├── Barranquilla_20251222.xlsx/csv (121 clínicas)
    ├── Cartagena_20251222.xlsx/csv (122 clínicas)
    ├── CONSOLIDADO_todas_ciudades_*.xlsx/csv (607 total)
    ├── LEADS_con_telefono_*.xlsx/csv (569 con WhatsApp) ⭐
    └── RESUMEN_por_ciudad_*.xlsx/csv (estadísticas)
```

**Archivo principal para prospección:**
`resultados/2024-12-22_extraccion_ampliada/LEADS_con_telefono_20251222_104507.xlsx`

## Comandos Rápidos

```bash
# Activar entorno
source venv/bin/activate

# Prueba rápida
python3 test_selenium.py

# Búsqueda completa
python3 gmaps_scraper_selenium.py

# Desactivar entorno
deactivate
```

## Notas para Claude

### Cuando modifiques código:
1. SIEMPRE usar `gmaps_scraper_selenium.py` como base
2. NO usar `gmaps_scraper.py` (Playwright - tiene bugs)
3. Respetar la estructura de selectores CSS existente
4. Mantener funciones de limpieza de datos
5. Preservar tiempos de espera (anti-detección)

### Cuando agregues features:
1. ✅ ~~Exportación a otros formatos~~ (CSV + Excel implementado)
2. Filtros avanzados (por rating, reviews, etc)
3. Detección de duplicados
4. Validación de teléfonos colombianos
5. Enriquecimiento con APIs externas

### Cuando debuggees:
1. Usar `headless=False` para ver el navegador
2. Aumentar tiempos de espera si hay errores
3. Verificar selectores CSS con DevTools
4. Revisar aria-labels de elementos dinámicos

---

## Comandos Slash Disponibles

Claude Code incluye comandos personalizados para facilitar el uso del scraper:

### `/documentar` - Actualizar documentación
Mantén la documentación sincronizada automáticamente.
```bash
/documentar "Descripción del cambio"
```

### `/scrape-ciudad` - Búsqueda rápida en una ciudad
Ejecuta una búsqueda en una ciudad específica.
```bash
/scrape-ciudad Medellín "clínica odontológica" 30
```

### `/filtrar-leads` - Filtrado inteligente de resultados
Filtra y prioriza leads según criterios.
```bash
/filtrar-leads CONSOLIDADO_todas_ciudades.xlsx
```

### `/analizar-mercado` - Análisis de competencia
Genera reporte estadístico de un archivo de resultados.
```bash
/analizar-mercado LEADS_con_telefono.xlsx
```

## Agentes Especializados

### Lead Researcher Agent
Investiga leads en detalle antes de contactar:
- Busca información adicional en web
- Valida que el negocio siga activo
- Encuentra nombre del decisor
- Detecta si ya usan automatización

---

---

## 🤖 CHATBOT PLATFORM - Arquitectura y Stack

### Componente Central: n8n

**n8n** es el núcleo de orquestación de toda la plataforma. Todos los workflows pasan por n8n.

```
┌─────────────────────────────────────────────────────────────┐
│              DUAL-PURPOSE CHATBOT PLATFORM                   │
│                    (n8n Orchestration)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📱 WhatsApp        🖥️ Internal Chat     🌐 Web Dashboard   │
│  (Clients)          (Team Members)       (Admin)            │
│       │                    │                    │           │
│       └────────────────────┼────────────────────┘           │
│                            │                                │
│                            ▼                                │
│              ┌─────────────────────────┐                    │
│              │   n8n WORKFLOW ENGINE   │                    │
│              │  (Core Orchestration)   │                    │
│              └─────────────────────────┘                    │
│                            │                                │
│         ┌──────────────────┼──────────────────┐            │
│         ▼                  ▼                  ▼            │
│    ┌─────────┐      ┌──────────┐      ┌──────────┐        │
│    │ OpenAI  │      │ Pinecone │      │PostgreSQL│        │
│    │ Claude  │      │ (Vectors)│      │ (History)│        │
│    └─────────┘      └──────────┘      └──────────┘        │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                    Knowledge Base                           │
└─────────────────────────────────────────────────────────────┘
```

### Stack Tecnológico Completo

**Orquestación:**
- n8n (Docker self-hosted o n8n Cloud)
- PostgreSQL para n8n + conversation logs

**AI/LLM:**
- OpenAI GPT-4o-mini (FAQs rápidos, clasificación)
- Claude 3.5 Sonnet (generación compleja, drafts)
- OpenAI Embeddings (vectorización de docs)

**WhatsApp:**
- Twilio WhatsApp API (MVP - $0.005/msg)
- Meta WhatsApp Business API (escala - menor costo)

**Knowledge Base:**
- Pinecone (vector DB - free tier 100k vectors)
- Alternativa: Supabase pgvector (PostgreSQL extension)

**Internal Chat:**
- Next.js 14 (App Router)
- Shadcn/ui components
- Webhooks to n8n
- Deploy: Vercel free tier

**Database:**
- PostgreSQL (Supabase free tier)
  - conversation_logs
  - clinic_configs
  - user_data
  - knowledge_documents

**Hosting:**
- **MVP (Gratis):** n8n Docker local + ngrok ($0-8/month)
- **Producción (Gratis):** Oracle Cloud Free Tier Forever ($0/month)
- **Alternativa:** Digital Ocean ($12/month) o Railway ($10-15/month)

### Costos Operacionales

**MVP (Semanas 1-3):**
```
n8n:              $0 (local) o $20 (cloud)
PostgreSQL:       $0 (Supabase free tier)
OpenAI API:       ~$20-50/mes (testing)
Twilio WhatsApp:  ~$20-30/mes (sandbox)
Pinecone:         $0 (free tier)
ngrok:            $0-8/mes (opcional)
─────────────────────────────────
Total MVP:        $40-128/mes
```

**Producción (5-10 clientes):**
```
n8n:              $0 (Oracle) o $12 (DO)
PostgreSQL:       $0 (Supabase free tier)
OpenAI API:       ~$100-200/mes
Twilio WhatsApp:  ~$100-150/mes (500-1000 msgs/cliente)
Pinecone:         $0 (free tier suficiente)
Domain:           $12/year (~$1/mes)
─────────────────────────────────
Total:            $201-363/mes

Revenue (10 clientes x $120 USD): $1,200/mes
Profit margin:    70-83%
```

### n8n Workflows Principales

1. **whatsapp-client-bot** (~15-20 nodes)
   - Webhook trigger (Twilio)
   - Clasificación de intención (OpenAI)
   - Búsqueda knowledge base (Pinecone)
   - Generación de respuesta (GPT-4)
   - Escalación a humano (si necesario)
   - Log conversation (PostgreSQL)
   - Envío respuesta (Twilio)

2. **internal-knowledge-chat** (~10-12 nodes)
   - Webhook trigger (Next.js app)
   - Autenticación usuario
   - Vector search (Pinecone)
   - Generación respuesta (Claude)
   - Draft generation (contexto específico)
   - Return JSON

3. **knowledge-base-sync** (~8-10 nodes)
   - Schedule trigger (daily) o Manual
   - Fetch docs (Google Drive / local)
   - Split chunks (1000 tokens)
   - Generate embeddings (OpenAI)
   - Upsert Pinecone
   - Log success

4. **multi-tenant-router** (Fase 2)
   - Extract clinic_id from webhook
   - Load clinic config from PostgreSQL
   - Route to clinic-specific namespace (Pinecone)
   - Use clinic-specific prompts

### Multi-Tenancy: Database Setup

**Implementación:** Database Lookup Pattern (RECOMENDADO para escala 10-100+ clientes)

El sistema usa PostgreSQL para almacenar configuraciones de múltiples clientes. Un solo workflow de n8n sirve a todos los clientes, identificando dinámicamente cuál cliente está escribiendo y cargando su configuración personalizada.

**Estructura de Base de Datos:**

Archivo: `n8n/db_schema.sql` (ejecutado en PostgreSQL)

```sql
-- Tabla principal: clientes
CREATE TABLE clients (
    id UUID PRIMARY KEY,
    business_name VARCHAR(255),
    whatsapp_number VARCHAR(20) UNIQUE,  -- Identificador único por cliente
    industry VARCHAR(100),                -- dental_clinic, beauty_salon, etc.
    services JSONB,                       -- Lista de servicios y precios
    business_hours TEXT,
    location TEXT,
    system_prompt TEXT,                   -- Prompt personalizado por cliente
    subscription_plan VARCHAR(50),
    monthly_fee DECIMAL(10,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de conversaciones (tracking y analytics)
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    client_id UUID REFERENCES clients(id),
    customer_phone VARCHAR(20),
    message_text TEXT,
    response_text TEXT,
    intent_detected VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de knowledge base (documentos por cliente)
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY,
    client_id UUID REFERENCES clients(id),
    document_title VARCHAR(255),
    content TEXT,
    embedding_id VARCHAR(100),  -- ID en Pinecone
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Clientes de Prueba Insertados:**

```sql
-- Cliente 1: Clínica Dental Medellín
INSERT INTO clients VALUES (
    gen_random_uuid(),
    'Clínica Dental Medellín',
    '+573001111111',
    'dental_clinic',
    '{"limpieza": 80000, "blanqueamiento": 150000, "ortodoncia": 3500000}',
    'Lun-Vie: 8AM-6PM, Sáb: 9AM-1PM',
    'Calle 50 #45-30, Medellín',
    'Eres un asistente virtual amable para Clínica Dental Medellín...',
    'premium',
    400000,
    true
);

-- Cliente 2: Centro Estético Bogotá
-- Cliente 3: Restaurante La Parrilla Cali
-- (Ver n8n/db_schema.sql para datos completos)
```

**Flujo Multi-Tenant en n8n:**

```
1. WhatsApp Message → Extraer número de teléfono
2. PostgreSQL Query → SELECT * FROM clients WHERE whatsapp_number = '{{ $json.From }}'
3. Load Config → Cargar system_prompt, services, hours del cliente
4. AI Agent → Usar prompt dinámico: {{ $node["PostgreSQL"].json["system_prompt"] }}
5. Generate Response → Respuesta personalizada para ese cliente
6. Log Conversation → INSERT INTO conversations (...)
7. Send Reply → Respuesta vía Twilio
```

**Ventajas:**
- ✅ Un solo workflow sirve infinitos clientes
- ✅ Onboarding nuevo cliente = agregar 1 fila a DB (2 minutos)
- ✅ Actualizar todos los clientes = 1 cambio en workflow
- ✅ Analytics por cliente en una sola tabla
- ✅ Escalable a 100+ clientes sin cambios

**Comandos PostgreSQL Útiles:**

```bash
# Conectar a la base de datos
docker exec -it n8n-postgres-1 psql -U n8n -d n8n

# Ver clientes activos
SELECT business_name, whatsapp_number, monthly_fee FROM clients WHERE is_active = true;

# Ver conversaciones de un cliente
SELECT * FROM conversations WHERE client_id = 'uuid-del-cliente' ORDER BY created_at DESC;

# Agregar nuevo cliente
INSERT INTO clients (business_name, whatsapp_number, ...) VALUES (...);

# Actualizar system_prompt de un cliente
UPDATE clients SET system_prompt = 'Nuevo prompt...' WHERE whatsapp_number = '+573001111111';
```

### Roadmap de Desarrollo

**Semana 1-3: MVP n8n**
- [x] Setup n8n local con Docker
- [x] Setup PostgreSQL multi-tenant database
- [x] Crear schema de clientes (clients, conversations, knowledge_base)
- [ ] Crear workflow WhatsApp básico (FAQ only)
- [ ] Integrar PostgreSQL lookup en workflow
- [ ] Crear workflow interno simple
- [ ] Ingest 20-30 FAQs a Pinecone
- [ ] Test end-to-end con Twilio sandbox
- [ ] Build simple Next.js chat interface

**Semana 4-8: Primeros Clientes**
- [ ] Priorizar 50 mejores leads (del scraper)
- [ ] Outreach personalizado (10-15/día)
- [ ] Cerrar 2-3 clientes MVP
- [ ] Duplicar workflows por cliente (manual)
- [ ] Customizar knowledge base por clínica
- [ ] Collect feedback y iterar

**Semana 9-16: Multi-Tenancy + Scale**
- [ ] Migrar a Oracle Cloud Free (producción)
- [ ] Implementar tenant routing en workflows
- [ ] Build admin dashboard (Retool o custom)
- [ ] Self-service onboarding
- [ ] Add appointment scheduling (Google Cal)
- [ ] 10-15 clientes objetivo

### Ventajas de n8n para Este Proyecto

1. **Visual debugging** - Ver cada paso del workflow
2. **Rapid iteration** - Cambios en minutos, no horas
3. **Built-in integrations** - 400+ nodes nativos
4. **Multi-client ready** - Duplicar o routing dinámico
5. **Cost effective** - Free self-hosted
6. **No backend code** - Solo workflows visuales
7. **Error handling** - Built-in retry y logging
8. **Webhook support** - Unlimited webhooks
9. **Scheduling** - Cron jobs incluidos
10. **MCP ready** - Integración futura con MCP servers

### Métricas de Éxito

**Fase MVP (Semana 3):**
- ✅ Bot responde 10+ FAQs correctamente
- ✅ Tiempo respuesta <3 segundos
- ✅ 0 errores en 100 mensajes test
- ✅ Internal chat busca knowledge base

**Fase First Clients (Semana 8):**
- ✅ 2-3 clientes pagando
- ✅ $500-800 USD/mes MRR
- ✅ <5% error rate
- ✅ >90% customer satisfaction

**Fase Scale (Semana 16):**
- ✅ 10-15 clientes activos
- ✅ $2,000-3,000 USD/mes MRR
- ✅ Multi-tenant system operational
- ✅ <2% churn rate

---

## 📚 Documentación Adicional

Para información detallada sobre cada componente:

- **CHATBOT_PLATFORM.md** - Arquitectura completa, flows, prompts
- **N8N_SETUP_GUIDE.md** - Setup paso a paso n8n local + Oracle Cloud
- **GUIA_PROSPECCION_CHATBOTS.md** - Estrategia de ventas y outreach
- **README.md** - Documentación técnica del scraper

---

**Última actualización:** 2026-01-03
**Estado del proyecto:**
- ✅ Scraper: Producción - 607 leads extraídos
- 🚧 Chatbot Platform: MVP en desarrollo
  - ✅ n8n + PostgreSQL setup completo
  - ✅ Database multi-tenant configurado
  - ✅ 3 clientes de prueba insertados
  - 🚧 Workflow n8n con PostgreSQL lookup (en progreso)
**Objetivo 90 días:** 10-15 clientes pagando ($2-3K USD/mes MRR)
**Scraper recomendado:** `gmaps_scraper_selenium.py`
**Leads disponibles:** 569 con WhatsApp (93.7%)
**Próximos pasos:**
1. ✅ Setup n8n local (Completado)
2. ✅ Setup PostgreSQL multi-tenant (Completado)
3. 🚧 Configurar workflow n8n con database lookup (En progreso)
4. Build MVP WhatsApp bot (Semana 1-3)
5. Prospección primeros clientes (Semana 4-8)
