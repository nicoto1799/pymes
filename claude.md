# Proyecto: Google Maps Scraper para Prospección de Clientes - Venta de Chatbots

## 🎯 Objetivo del Proyecto

Este proyecto automatiza la **extracción de leads B2B** desde Google Maps para **prospectar clientes potenciales** interesados en **chatbots de WhatsApp** y soluciones de automatización de atención al cliente.

**Modelo de negocio:** Generar MRR (Monthly Recurring Revenue) vendiendo chatbots a clínicas, consultorios y PYMEs en Colombia.

## Resumen del Proyecto

Scraper web automatizado que extrae información pública de negocios en Google Maps, enfocado en clínicas odontológicas, estéticas, médicas y otros negocios de servicios en Colombia. Genera bases de datos con datos de contacto (especialmente teléfonos de WhatsApp) para prospección comercial de chatbots y automatización.

## Tecnologías Principales

- **Python 3.12**
- **Selenium** (scraper principal - RECOMENDADO)
- **Playwright** (implementación alternativa - tiene bugs)
- **Pandas** para procesamiento de datos
- **OpenPyXL** para exportación a Excel

## Estructura del Proyecto

```
pymes/
├── gmaps_scraper_selenium.py           # ⭐ SCRAPER PRINCIPAL (usar este)
├── test_selenium.py                    # Script de prueba rápida (5 resultados)
├── buscar_clinicas.py                  # Script ejemplo búsqueda única (Playwright)
├── buscar_por_ciudades_selenium.py     # ⭐ Script múltiples ciudades (RECOMENDADO)
├── buscar_por_ciudades.py              # Script múltiples ciudades (Playwright - obsoleto)
├── gmaps_scraper.py                    # Versión Playwright (NO USAR - tiene bugs)
├── test_scraper.py                     # Test Playwright (obsoleto)
├── requirements.txt                    # Dependencias Python
├── setup.sh                            # Script de instalación automática
├── README.md                           # Documentación técnica completa
├── GUIA_RAPIDA.md                     # Guía de inicio rápido
├── GUIA_PROSPECCION_CHATBOTS.md       # 🎯 GUÍA DE VENTAS Y PROSPECCIÓN
├── INSTRUCCIONES.md                   # Estado del proyecto e instrucciones
├── CLAUDE.md                          # Este archivo - Contexto para Claude
├── .claude/                           # Comandos y agentes de Claude Code
│   ├── commands/                      # Comandos slash personalizados
│   └── agents/                        # Agentes especializados
├── resultados/                        # 📁 Carpeta de extracciones organizadas
│   ├── 2024-12-15_primera_extraccion/    # 133 clínicas (30 por ciudad)
│   └── 2024-12-22_extraccion_ampliada/   # 607 clínicas (120 por ciudad)
└── venv/                              # Entorno virtual Python
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

**Última actualización:** 2024-12-22
**Estado del proyecto:** ✅ Producción - 607 leads extraídos
**Objetivo:** Venta de chatbots (MRR)
**Scraper recomendado:** `gmaps_scraper_selenium.py`
**Leads disponibles:** 569 con WhatsApp (93.7%)
**Próximo paso:** Prospección - Ver `GUIA_PROSPECCION_CHATBOTS.md`
