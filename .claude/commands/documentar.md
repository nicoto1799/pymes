# Documentar Command

Actualiza automáticamente la documentación del proyecto cuando hagas cambios.

## Propósito

Mantener sincronizados todos los archivos de documentación (CLAUDE.md, README.md, GUIA_RAPIDA.md, etc.) cuando agregas features, corriges bugs, o modificas el código.

## Uso

```bash
/documentar
```

O con contexto específico:

```bash
/documentar "Agregué validación de teléfonos colombianos en el scraper"
```

## ¿Qué hace este comando?

### 1. Detecta Cambios Automáticamente

Analiza:
- ✅ Archivos Python modificados recientemente
- ✅ Nuevos archivos creados
- ✅ Archivos eliminados
- ✅ Cambios en dependencias (requirements.txt)
- ✅ Nuevos comandos o agentes

### 2. Identifica Qué Documentar

Determina qué archivos de documentación necesitan actualización:
- `claude.md` - Para cambios en el proyecto general
- `README.md` - Para instrucciones de usuario
- `GUIA_RAPIDA.md` - Para flujos de trabajo
- `GUIA_COMANDOS_CLAUDE.md` - Para nuevos comandos/agentes
- `.claude/README.md` - Para comandos slash internos

### 3. Pregunta Qué Cambió

Si no proporcionaste contexto, te pregunta:

```
📝 ¿Qué cambios realizaste?

Archivos modificados detectados:
- gmaps_scraper_selenium.py (modificado hace 5 min)
- requirements.txt (modificado hace 2 min)

Opciones:
1. Nuevo feature (ej: agregué filtro de teléfonos)
2. Bug fix (ej: corregí error en scroll)
3. Mejora de rendimiento
4. Refactoring
5. Actualización de dependencias
6. Nuevo comando/agente
7. Otro (especificar)

Selecciona una opción o describe el cambio:
```

### 4. Actualiza Documentación Relevante

Según el tipo de cambio, actualiza:

#### Para NUEVO FEATURE:
- ✅ Agrega sección en `claude.md` → "Notas para Claude / Features"
- ✅ Actualiza ejemplos en `README.md`
- ✅ Actualiza "Estado del Proyecto"
- ✅ Incrementa versión si aplica

#### Para BUG FIX:
- ✅ Actualiza "Solución de Problemas" en `claude.md`
- ✅ Agrega nota en changelog (si existe)
- ✅ Actualiza fecha de última modificación

#### Para NUEVA DEPENDENCIA:
- ✅ Actualiza sección "Dependencias" en `claude.md`
- ✅ Actualiza instrucciones de instalación
- ✅ Verifica `requirements.txt` esté documentado

#### Para NUEVO COMANDO/AGENTE:
- ✅ Agrega a lista de comandos en `claude.md`
- ✅ Actualiza `.claude/README.md`
- ✅ Actualiza `GUIA_COMANDOS_CLAUDE.md`
- ✅ Incrementa contador de comandos/agentes

### 5. Genera Resumen de Cambios

Muestra qué se actualizó:

```
✅ Documentación actualizada!

Archivos modificados:
- claude.md
  → Agregada sección "Validación de Teléfonos"
  → Actualizado "Estado del Proyecto"
  → Fecha actualizada: 2025-12-22

- README.md
  → Agregado ejemplo de uso de validación
  → Actualizada sección "Uso Básico"

- GUIA_RAPIDA.md
  → Agregado paso de validación en flujo

Resumen del cambio:
"Agregué validación de teléfonos colombianos que verifica
formato +57 XXX XXX XXXX y detecta números inválidos"

¿Todo correcto? (si/no)
```

## Flujo Interactivo

### Caso 1: Sin contexto (detección automática)

```
Usuario: /documentar

Claude:
📝 Detecté cambios recientes en:
- gmaps_scraper_selenium.py (hace 10 min)

¿Qué tipo de cambio hiciste?
1. Nuevo feature
2. Bug fix
3. Mejora de rendimiento
4. Refactoring
5. Otro

Usuario: 1

Claude:
🎯 ¿Qué feature agregaste?
Describe brevemente (1-2 frases):

Usuario: Agregué filtro para validar teléfonos colombianos

Claude:
✅ Entendido. Voy a actualizar la documentación...

[Actualiza archivos]

✅ Listo! Documentación actualizada en 3 archivos.
```

### Caso 2: Con contexto (directo)

```
Usuario: /documentar "Agregué exportación a formato JSON además de CSV/Excel"

Claude:
📝 Cambio detectado: Nuevo feature de exportación

Voy a actualizar:
- claude.md (método save_to_json en gmaps_scraper_selenium.py)
- README.md (ejemplo de uso)
- Sección "Datos Extraídos"

[Actualiza archivos]

✅ Listo! 3 archivos actualizados.

Resumen:
- Agregado método save_to_json() en documentación
- Actualizado ejemplo de uso con las 3 opciones de exportación
- Estado del proyecto: JSON exportación funcional
```

### Caso 3: Nuevo comando creado

```
Usuario: /documentar "Creé comando /generar-mensaje para crear mensajes WhatsApp"

Claude:
📝 Nuevo comando detectado!

Verificando:
- ✅ Archivo .claude/commands/generar-mensaje.md existe
- ✅ Comando documentado internamente

Actualizando:
- claude.md → Lista de comandos disponibles
- .claude/README.md → Agregar /generar-mensaje
- GUIA_COMANDOS_CLAUDE.md → Sección nueva

[Actualiza archivos]

✅ Comando documentado!

Nuevo contador:
- Comandos disponibles: 4 (antes: 3)
- Agentes disponibles: 1
```

## Características Inteligentes

### Auto-detección de Cambios

```python
# Detecta archivos modificados en últimos 60 minutos
git diff --name-status HEAD~1  # Si es repo git

# O usa timestamps de archivos
find . -mmin -60 -type f -name "*.py"
```

### Validación de Consistencia

Verifica que:
- ✅ Todos los archivos .py mencionados existen
- ✅ Todos los comandos en .claude/commands/ están documentados
- ✅ Fechas están actualizadas
- ✅ Contadores son correctos
- ✅ No hay referencias a archivos obsoletos

### Sugerencias Inteligentes

Si detecta:
- Nuevo método en clase → Sugiere documentarlo en "Métodos principales"
- Nueva dependencia → Sugiere actualizar requirements.txt
- Cambio en selectores CSS → Sugiere actualizar tabla de selectores
- Nuevo archivo de ejemplo → Sugiere agregarlo a "Archivos de Ejemplo"

## Plantillas de Actualización

### Template: Nuevo Feature

```markdown
## [NOMBRE_FEATURE] ← Se agrega en sección apropiada

### Descripción
[Descripción del feature]

### Uso
```python
[Ejemplo de código]
```

### Parámetros
- `param1`: Descripción
- `param2`: Descripción

### Ejemplo
[Ejemplo práctico]

**Agregado:** 2025-12-22
```

### Template: Bug Fix

```markdown
### [TÍTULO DEL BUG] ← En "Solución de Problemas"

**Síntoma:**
[Descripción del error]

**Causa:**
[Por qué ocurría]

**Solución:**
```python
[Código o pasos para resolver]
```

**Corregido:** 2025-12-22
```

### Template: Nueva Dependencia

```markdown
## Dependencias (requirements.txt)

```txt
[Dependencias existentes...]
nueva-libreria==1.2.3  # ← Se agrega
```

### [nombre-libreria]
**Propósito:** [Para qué se usa]
**Instalación:** `pip install nombre-libreria`
**Documentación:** [URL oficial]

**Agregado:** 2025-12-22
```

## Comandos de Actualización Específicos

### Solo fecha
```bash
/documentar fecha
```
→ Actualiza solo "Última actualización" en todos los archivos

### Solo estado
```bash
/documentar estado
```
→ Actualiza solo "Estado del Proyecto"

### Solo contadores
```bash
/documentar contadores
```
→ Actualiza contadores de comandos/agentes

### Verificar consistencia
```bash
/documentar verificar
```
→ Solo verifica, no modifica nada

## Ejemplo Completo de Uso

### Escenario: Agregaste validación de teléfonos

```bash
Usuario: /documentar "Agregué validación de formato de teléfonos colombianos"

Claude:
📝 Analizando cambio: Validación de teléfonos

Archivos modificados detectados:
- gmaps_scraper_selenium.py (método validate_phone agregado)

Documentando en:
- claude.md
- README.md
- GUIA_RAPIDA.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 claude.md
  → Sección "Limpieza de Datos"
    ✅ Agregado método validate_phone()
    ✅ Ejemplo de uso

  → Sección "Features"
    ✅ Agregado "Validación de teléfonos colombianos"

  → Sección "Estado del Proyecto"
    ✅ Marcado: "✅ Validación de teléfonos colombianos"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 README.md
  → Sección "Filtrado de Resultados"
    ✅ Agregado ejemplo: Filtrar teléfonos válidos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 GUIA_RAPIDA.md
  → Sección "Mejores Prácticas"
    ✅ Agregado tip: Validar teléfonos antes de contactar

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Documentación actualizada!

Archivos modificados: 3
Líneas agregadas: 42
Fecha actualizada: 2025-12-22

¿Quieres generar un commit con estos cambios? (si/no)
```

## Integración con Git (Opcional)

Si el proyecto es un repo git, ofrece:

```bash
¿Crear commit con documentación actualizada? (si/no)

Si usuario dice "si":

git add claude.md README.md GUIA_RAPIDA.md
git commit -m "docs: Agregada validación de teléfonos colombianos

- Documentado método validate_phone()
- Agregados ejemplos de uso
- Actualizado estado del proyecto

🤖 Generated with Claude Code"
```

## Checklist de Verificación

Antes de finalizar, verifica:

- [ ] Fecha actualizada en todos los archivos modificados
- [ ] Estado del proyecto refleja los cambios
- [ ] Ejemplos de código son correctos
- [ ] Referencias a archivos/métodos existen
- [ ] Contadores actualizados (si aplica)
- [ ] Sin typos en nombres de archivos/métodos
- [ ] Formato Markdown correcto
- [ ] Enlaces funcionan (si hay)

## Notas Importantes

### Archivos que SIEMPRE se actualizan:
- `claude.md` - Fecha de última actualización

### Archivos que dependen del cambio:
- `README.md` - Si afecta al usuario final
- `GUIA_RAPIDA.md` - Si cambia el flujo de trabajo
- `.claude/README.md` - Si afecta comandos/agentes
- `GUIA_COMANDOS_CLAUDE.md` - Si hay nuevos comandos

### Archivos que NUNCA se modifican automáticamente:
- `requirements.txt` - Solo sugerir, no modificar
- Archivos `.py` - Solo documentar, no cambiar código
- Archivos de resultados (CSV/Excel)

## Prompts de Ayuda

Si el usuario no sabe qué cambió:

```
No estoy seguro qué cambié exactamente

Claude responde:
📝 No te preocupes, voy a ayudarte a identificarlo.

Archivos modificados recientemente:
1. gmaps_scraper_selenium.py (hace 15 min)
   - Línea 234: Agregada función clean_phone()
   - Línea 456: Modificado método _extract_data()

2. requirements.txt (hace 5 min)
   - Agregada: phonenumbers==8.13.0

¿Alguno de estos cambios es importante documentar?
```

## Tips para el Usuario

### ✅ Usa /documentar cuando:
- Agregas un feature nuevo
- Corriges un bug importante
- Actualizas dependencias
- Creas comandos/agentes nuevos
- Cambias el flujo de trabajo

### ⏭️ No necesitas /documentar para:
- Typos menores en comentarios
- Cambios experimentales temporales
- Debugging (console.logs, prints)
- Archivos de prueba

### 🎯 Best Practice:
```bash
# Después de completar un feature
1. Prueba que funcione
2. /documentar "Descripción del cambio"
3. Revisa los archivos actualizados
4. Commit (si usas git)
```

## Salida Final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DOCUMENTACIÓN ACTUALIZADA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Resumen del cambio:
"[Descripción del cambio]"

📄 Archivos actualizados: [N]
- [archivo1.md] ([N] cambios)
- [archivo2.md] ([N] cambios)

📅 Fecha: 2025-12-22

🔍 Verificación:
- ✅ Consistencia de referencias
- ✅ Formato Markdown correcto
- ✅ Ejemplos de código válidos
- ✅ Fechas actualizadas

💡 Próximo paso:
[Sugerencia contextual basada en el cambio]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Creado:** 2025-12-22
**Versión:** 1.0
**Tipo:** Comando de mantenimiento
**Uso:** Cada vez que hagas cambios al proyecto
