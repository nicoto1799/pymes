# 🚀 Guía Rápida - Scraper Google Maps

## ⚡ Instalación (5 minutos)

```bash
# 1. Ejecuta el script de instalación
./setup.sh

# 2. Activa el entorno virtual
source venv/bin/activate
```

## 🎯 Uso Inmediato

### Opción 1: Búsqueda simple en una ciudad

```bash
python buscar_clinicas.py
```

**Edita antes de ejecutar:**
- Abre `buscar_clinicas.py`
- Cambia la línea 18: `query = "clínica odontológica Medellín"`
- Por tu búsqueda: `query = "tu búsqueda aquí"`

### Opción 2: Múltiples ciudades automáticamente

```bash
python buscar_por_ciudades.py
```

**Edita antes de ejecutar:**
- Abre `buscar_por_ciudades.py`
- Línea 13: Cambia `TIPO_NEGOCIO = "clínica odontológica"`
- Línea 16-26: Selecciona las ciudades que quieres

## 📊 Resultados

Después de ejecutar, obtendrás archivos Excel con:

- ✅ Nombre del negocio
- ✅ Teléfono (para WhatsApp)
- ✅ Dirección
- ✅ Rating y reseñas
- ✅ Sitio web
- ✅ Categoría

## 💡 Ejemplos de búsquedas

```python
# Clínicas odontológicas
"clínica odontológica Medellín"

# Clínicas estéticas
"clínica estética Bogotá"
"medicina estética Cali"

# Oftalmología
"oftalmología Medellín"
"clínica oftalmológica Bogotá"

# Ortopedia
"ortopedia Medellín"
"traumatología Bogotá"

# Psicología
"consultorio psicológico Medellín"
"psicología privada Bogotá"

# Dermatología
"dermatología Medellín"
"clínica dermatológica Bogotá"
```

## 🎯 Mejores prácticas

### ✅ Hacer

- Buscar ciudad por ciudad
- Máximo 50 resultados por búsqueda
- Revisar manualmente antes de contactar
- Contacto personalizado 1 a 1
- Máximo 10-20 mensajes por día

### ❌ No hacer

- Búsquedas muy amplias ("clínica Colombia")
- Envío masivo automatizado
- Spam
- Más de 100 resultados de una vez

## 📞 Siguiente paso: Contacto

1. **Filtra el Excel**
   - Ordena por rating (mejores primero)
   - Filtra los que tienen teléfono
   - Elimina duplicados

2. **Valida manualmente**
   - Revisa su Instagram/Facebook
   - Verifica que estén activos
   - Mira sus reseñas

3. **Prepara tu mensaje**
   ```
   Hola, ¿hablo con la persona que gestiona las citas en [NOMBRE CLINICA]?

   Trabajo con clínicas ayudándoles a automatizar WhatsApp para
   agendar citas y hacer seguimiento sin perder pacientes.

   ¿Te interesaría ver un ejemplo rápido?
   ```

4. **Contacta**
   - 10-20 por día máximo
   - Personaliza cada mensaje
   - Sé humano, no robot

## 🛠 Troubleshooting

### "No se encontraron resultados"
- ✅ Verifica tu conexión a internet
- ✅ Usa búsquedas más específicas
- ✅ Prueba con otra ciudad

### "Error al instalar Playwright"
```bash
pip install playwright
playwright install chromium
```

### El navegador se cierra muy rápido
- Normal, está configurado en modo headless
- Para ver el navegador: edita `gmaps_scraper.py` línea 55
- Cambia `headless=False` a `headless=True`

### Muy pocos resultados
- Aumenta `scroll_attempts` a 15-20
- Aumenta `max_results` a 50-100
- Prueba búsquedas más amplias

## 📈 Proyecciones realistas

Con este scraper puedes:

- **Por hora:** 50-100 leads
- **Por día:** 200-500 leads
- **Por semana:** 1.000-2.000 leads

**Filtrado (con teléfono):** ~60-70% tendrán teléfono

## 🎯 Estrategia recomendada

### Semana 1: Investigación
- Extrae 100-200 clínicas por ciudad
- Analiza patrones
- Identifica nichos

### Semana 2: Validación
- Contacta 10-20 por día
- Prueba diferentes mensajes
- Ajusta tu pitch

### Semana 3+: Escala
- Contacta 20-30 por día
- Cierra primeros clientes
- Refina el proceso

## 💰 ROI Esperado

**Inversión de tiempo:**
- Setup: 30 min
- Por búsqueda: 5-10 min
- Filtrado: 10-15 min por ciudad

**Retorno:**
- 1 cliente = 400k-1.2M COP/mes
- Con 10 clientes = 4M-12M COP/mes
- ROI: ∞ (costo casi cero)

## ⚖️ Legal

- ✅ Información pública
- ✅ Contacto personalizado
- ❌ Spam masivo
- ❌ Automatización abusiva

---

## 🆘 ¿Necesitas ayuda?

1. Lee el `README.md` completo
2. Revisa los scripts de ejemplo
3. Prueba con búsquedas pequeñas primero

**¡Éxito en tu prospección! 🚀**
