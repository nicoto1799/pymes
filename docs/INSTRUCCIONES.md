# 🎯 Scraper de Google Maps - FUNCIONANDO ✅

## ✅ Estado: TODO INSTALADO Y PROBADO

El scraper **YA ESTÁ FUNCIONANDO** y ha sido probado exitosamente.

**Prueba realizada:**
- ✅ 5 clínicas odontológicas extraídas de Medellín
- ✅ 80% con teléfono (para WhatsApp)
- ✅ Datos guardados en Excel

---

## 🚀 Cómo usar (AHORA MISMO)

### Opción 1: Prueba rápida (5 resultados)

```bash
source venv/bin/activate
python3 test_selenium.py
```

Esto te dará 5 clínicas de prueba en 1-2 minutos.

### Opción 2: Búsqueda completa (30-50 resultados)

Edita el archivo `gmaps_scraper_selenium.py` al final donde dice:

```python
query = "clínica odontológica Medellín"
```

Cambia por tu búsqueda, luego ejecuta:

```bash
source venv/bin/activate
python3 gmaps_scraper_selenium.py
```

---

## 📋 Búsquedas recomendadas

### Para clínicas odontológicas:
```python
"clínica odontológica Medellín"
"clínica odontológica Bogotá"
"clínica odontológica Cali"
```

### Para clínicas estéticas:
```python
"clínica estética Medellín"
"medicina estética Bogotá"
"cirugía estética Cali"
```

### Para otras especialidades:
```python
"clínica oftalmología Medellín"
"clínica ortopedia Bogotá"
"consultorio psicológico Medellín"
"clínica dermatología Cali"
```

---

## 📊 Qué datos obtienes

Cada resultado incluye:

- ✅ Nombre del negocio
- ✅ **Teléfono** (para contacto por WhatsApp)
- ✅ Dirección completa
- ✅ Rating (estrellas)
- ✅ Número de reseñas
- ✅ Categoría
- ✅ Sitio web
- ✅ Horarios
- ✅ Fecha de extracción

---

## 🎯 Workflow recomendado

### Día 1-2: Extracción
```bash
# Activa el entorno
source venv/bin/activate

# Ejecuta para tu ciudad
python3 gmaps_scraper_selenium.py
```

Esto te generará un archivo Excel con 20-50 clínicas.

### Día 3: Filtrado
1. Abre el Excel generado
2. Filtra solo los que tienen teléfono
3. Ordena por rating (mejores primero)
4. Elimina duplicados si los hay

### Día 4-30: Contacto
- **10-20 mensajes personalizados por día**
- Usa WhatsApp manualmente (no automatices)
- Mensaje corto y directo
- Sigue el patrón del README

---

## 💰 Proyección realista

Con este scraper en **1 hora** puedes tener:

- **100-200 leads** de clínicas
- **60-70% con teléfono** = 60-140 contactos válidos
- **Meta: 10-20 contactos/día** = 1 semana de prospección

**Tasa de conversión esperada:**
- 100 contactos → 15 respuestas → 5 reuniones → 1-2 clientes

---

## 📁 Archivos principales

| Archivo | Descripción |
|---------|-------------|
| `gmaps_scraper_selenium.py` | **Scraper principal (USA ESTE)** |
| `test_selenium.py` | Prueba rápida (5 resultados) |
| `gmaps_scraper.py` | Versión Playwright (tiene bugs, no usar) |
| `requirements.txt` | Dependencias Python |
| `README.md` | Documentación completa |

---

## 🔧 Comandos útiles

### Activar entorno virtual
```bash
source venv/bin/activate
```

### Desactivar entorno virtual
```bash
deactivate
```

### Reinstalar dependencias (si hay problemas)
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

---

## ⚠️ Notas importantes

### ✅ Hacer:
- Contacto personalizado 1 a 1
- Máximo 20 mensajes por día
- Revisar manualmente antes de contactar
- Guardar registro de quién respondió

### ❌ NO hacer:
- Spam masivo
- Automatizar envío de mensajes
- Contactar de madrugada
- Copiar/pegar el mismo mensaje
- Más de 50 extracciones por día (para no saturar)

---

## 🎯 Siguiente paso inmediato

### AHORA MISMO puedes:

1. **Extraer tus primeros leads:**
```bash
source venv/bin/activate
python3 test_selenium.py
```

2. **Ver el Excel generado:**
Abre `test_selenium_resultados.xlsx`

3. **Elegir los mejores 5-10**
Los que tengan:
- ✅ Rating > 4.0
- ✅ Teléfono
- ✅ Varias reseñas

4. **Contactar HOY MISMO**
Mensaje ejemplo:
```
Hola, ¿hablo con la persona que gestiona las citas en [NOMBRE CLINICA]?

Trabajo con clínicas ayudándoles a automatizar WhatsApp para
no perder pacientes que escriben fuera de horario.

¿Te interesaría ver cómo funciona en 10 minutos?
```

---

## 📈 Roadmap sugerido

### Semana 1: Validación
- Extrae 50-100 clínicas
- Contacta 10-15 por día
- Prueba diferentes mensajes
- Anota qué funciona

### Semana 2: Optimización
- Usa el mensaje que mejor funcionó
- Aumenta a 15-20 contactos/día
- Refina tu pitch en llamadas

### Semana 3: Cierre
- Primer cliente objetivo
- Testimonial para siguientes
- Escala contactos

### Mes 2+:
- 5-10 clientes = negocio validado
- Contratar comercial o socio
- Automatizar más cosas

---

## 🆘 Problemas comunes

### "No se encontraron resultados"
- Verifica tu internet
- Usa búsquedas más específicas
- Prueba otra ciudad

### "Chrome se cierra solo"
- Es normal si la búsqueda terminó
- Revisa el archivo Excel generado

### "Muy pocos resultados"
- Aumenta `max_results` a 50
- Aumenta `scroll_attempts` a 10-15
- Usa búsquedas más amplias

---

## ✅ Checklist de éxito

- [ ] Entorno virtual activado
- [ ] Prueba exitosa (5 resultados)
- [ ] Excel generado y revisado
- [ ] Primeros 10 leads identificados
- [ ] Mensaje de contacto preparado
- [ ] Primeros 3 contactos enviados
- [ ] Seguimiento organizado (hoja de cálculo)

---

**¡ESTÁS LISTO! Ya tienes todo lo que necesitas para empezar tu prospección.**

La clave ahora es **ACCIÓN**: extraer leads y contactar de forma consistente.

**Meta esta semana:**
- 50 leads extraídos
- 20 contactos enviados
- 3-5 respuestas
- 1 reunión agendada

🚀 **¡Éxito!**
