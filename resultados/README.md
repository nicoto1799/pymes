# 📊 Resultados de Extracción - Google Maps Scraper

Esta carpeta contiene todas las extracciones de leads organizadas por fecha.

---

## 📁 Estructura

```
resultados/
├── 2024-12-15_primera_extraccion/    # Primera extracción (30 por ciudad)
└── 2024-12-22_extraccion_ampliada/   # Extracción ampliada (120 por ciudad)
```

---

## 📅 2024-12-15: Primera Extracción

**Configuración:**
- Tipo de negocio: Clínicas odontológicas
- Ciudades: Medellín, Bogotá, Cali, Barranquilla, Cartagena
- Max resultados: 30 por ciudad
- Scroll attempts: 10

**Resultados:**
- Total extraído: **133 clínicas**
- Con teléfono: ~106 (80%)
- Archivos generados: 18

**Archivos principales:**
- `LEADS_con_telefono_20251215_111940.xlsx` - Leads listos para contactar
- `CONSOLIDADO_todas_ciudades_20251215_111940.xlsx` - Todos los resultados
- `RESUMEN_por_ciudad_20251215_111940.xlsx` - Estadísticas por ciudad

---

## 📅 2024-12-22: Extracción Ampliada ⭐

**Configuración:**
- Tipo de negocio: Clínicas odontológicas
- Ciudades: Medellín, Bogotá, Cali, Barranquilla, Cartagena
- Max resultados: 500 por ciudad (target)
- Scroll attempts: 60

**Resultados:**
- Total extraído: **607 clínicas**
- Con teléfono: **569 (93.7%)** ✅
- Con website: 357 (59%)
- Con rating: 555 (91%)
- Archivos generados: 16

**Desglose por ciudad:**

| Ciudad | Total | Con WhatsApp | Con Website | Con Rating |
|--------|-------|--------------|-------------|------------|
| Medellín | 122 | 121 (99%) | 79 | 115 |
| Bogotá | 122 | 111 (91%) | 59 | 109 |
| Cali | 120 | 111 (93%) | 87 | 113 |
| Barranquilla | 121 | 113 (93%) | 74 | 110 |
| Cartagena | 122 | 113 (93%) | 58 | 108 |

**Archivos principales:**
- ⭐ `LEADS_con_telefono_20251222_104507.xlsx` - **569 leads con WhatsApp**
- `CONSOLIDADO_todas_ciudades_20251222_104507.xlsx` - Todos los resultados
- `RESUMEN_por_ciudad_20251222_104507.xlsx` - Estadísticas

**Archivos por ciudad:**
- `Medellín_20251222.xlsx/csv`
- `Bogotá_20251222.xlsx/csv`
- `Cali_20251222.xlsx/csv`
- `Barranquilla_20251222.xlsx/csv`
- `Cartagena_20251222.xlsx/csv`

---

## 📊 Datos Extraídos

Cada registro incluye:

| Campo | Descripción | Uso Principal |
|-------|-------------|---------------|
| `name` | Nombre del negocio | Personalización del mensaje |
| `category` | Categoría (ej: "Clínica odontológica") | Segmentación |
| `rating` | Calificación (0-5 estrellas) | Priorización (buscar 4.0-4.5) |
| `reviews_count` | Número de reseñas | Identificar alto volumen |
| `address` | Dirección completa | Localización |
| **`phone`** | ⭐ **Teléfono** | **Contacto por WhatsApp** |
| `website` | Sitio web | Investigación previa |
| `hours` | Horarios de atención | Planificación de contacto |
| `extracted_at` | Fecha/hora de extracción | Trazabilidad |
| `ciudad_busqueda` | Ciudad filtrada | Segmentación geográfica |

---

## 🎯 Uso para Prospección de Chatbots

### Paso 1: Abre el archivo principal
```
resultados/2024-12-22_extraccion_ampliada/LEADS_con_telefono_20251222_104507.xlsx
```

### Paso 2: Filtra y prioriza
1. **Por ciudad** - Empieza con 1 ciudad (ej: Medellín)
2. **Por rating** - 4.0 a 4.5 estrellas (necesitan mejorar)
3. **Por reviews** - 50 a 300 reseñas (alto volumen)
4. **Ordena** - Mayor a menor por `reviews_count`

### Paso 3: Crea tu lista de prospección
- Selecciona top 50 leads
- Guárdalos en un archivo separado
- Investiga cada uno manualmente antes de contactar

### Paso 4: Investiga antes de contactar
Para cada lead:
1. Busca en Google Maps y lee reseñas
2. Identifica quejas sobre atención/respuestas
3. Busca en web/redes sociales
4. Identifica al decisor (Dr./Dra.)

### Paso 5: Contacta personalizado
- 10-15 mensajes por día
- Personaliza SIEMPRE
- Menciona algo específico de su negocio
- Ofrece demo de 15 min

**📖 Ver `GUIA_PROSPECCION_CHATBOTS.md` para el plan completo**

---

## 🔄 Próximas Extracciones

### Cuándo volver a extraer
- ✅ Cada 2-3 meses (negocios nuevos)
- ✅ Cuando expandas a nuevas ciudades
- ✅ Cuando cambies de nicho (ej: clínicas estéticas)

### Otros nichos sugeridos
```python
# Modificar TIPO_NEGOCIO en buscar_por_ciudades_selenium.py

"clínica estética"        # Botox, rellenos
"spa"                     # Masajes, tratamientos
"centro médico"           # Médicos generales
"veterinaria"             # Mascotas
"gimnasio"                # Fitness
"restaurante"             # Reservas
```

### Expandir ciudades
```python
# Agregar a CIUDADES en buscar_por_ciudades_selenium.py

"Bucaramanga"
"Pereira"
"Manizales"
"Cúcuta"
"Santa Marta"
"Ibagué"
```

---

## 📈 Métricas de Calidad

### Tasa de teléfonos (ideal: >85%)
- 2024-12-15: 80% ✅
- 2024-12-22: **93.7%** ✅✅

### Negocios con rating visible (ideal: >90%)
- 2024-12-22: 91% ✅

### Conclusión
Las extracciones tienen **excelente calidad** para prospección B2B.

---

## ⚠️ Notas Importantes

### Limitación de Google Maps
- Google Maps muestra ~120 resultados únicos por búsqueda
- Aunque configuramos 500, solo obtuvimos 120-122 por ciudad
- Esto es normal y esperado

### Duplicados
- Posibles duplicados entre extracciones de diferentes fechas
- Usa campo `phone` para deduplicar
- Excel: Datos → Quitar duplicados → Seleccionar columna "phone"

### Privacidad y Uso Ético
- ✅ Datos públicos de Google Maps
- ✅ Uso para contacto B2B personalizado
- ❌ NO usar para spam masivo
- ❌ NO vender/compartir datos sin permiso
- ✅ Respetar opt-outs de contacto

---

**Generado por:** Google Maps Scraper (Selenium)
**Última extracción:** 2024-12-22
**Total leads disponibles:** 569 con WhatsApp
**Estado:** Listo para prospección
