# 🚀 n8n Setup Guide - Paso a Paso

## 📋 Índice

1. [Setup Local MVP (30 minutos)](#setup-local-mvp)
2. [Configuración de Servicios Externos](#configuración-de-servicios-externos)
3. [Crear Primer Workflow](#crear-primer-workflow)
4. [Testing con Twilio Sandbox](#testing-con-twilio-sandbox)
5. [Deploy a Oracle Cloud (Producción)](#deploy-a-oracle-cloud)
6. [Troubleshooting](#troubleshooting)

---

## Setup Local MVP

### Prerrequisitos

```bash
# Verificar que tengas instalado:
docker --version   # Docker 20.10+
docker-compose --version  # 1.29+

# Si no tienes Docker:
# Mac: https://docs.docker.com/desktop/install/mac-install/
# Toma ~5 minutos
```

### Paso 1: Crear Estructura de Directorios

```bash
cd /Users/nico/Documents/pymes

# Crear carpetas para n8n
mkdir -p n8n/workflows
mkdir -p n8n/.n8n
mkdir -p knowledge-base/templates
```

### Paso 2: Crear docker-compose.yml

```bash
# Crear archivo
cd n8n
nano docker-compose.yml
```

**Contenido:**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n_password_change_this
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U n8n']
      interval: 10s
      timeout: 5s
      retries: 5

  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n_password_change_this

      # Basic Auth (cambiar usuario/password)
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=change_this_password

      # Timezone
      - GENERIC_TIMEZONE=America/Bogota
      - TZ=America/Bogota

      # Webhook URL (cambiar cuando uses ngrok)
      - WEBHOOK_URL=http://localhost:5678/

      # Encryption key (generar uno único)
      - N8N_ENCRYPTION_KEY=very_long_random_string_here_min_10_chars

    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/workflows
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  n8n_data:
```

**Guardar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Paso 3: Crear .env (Opcional pero Recomendado)

```bash
nano .env
```

**Contenido:**

```bash
# PostgreSQL
POSTGRES_USER=n8n
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=n8n

# n8n
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_admin_password_here
N8N_ENCRYPTION_KEY=generate_random_string_min_10_chars

# Timezone
TZ=America/Bogota

# Webhook URL (actualizar cuando uses ngrok)
WEBHOOK_URL=http://localhost:5678/
```

**Guardar y cerrar**

### Paso 4: Iniciar n8n

```bash
# Asegúrate de estar en /Users/nico/Documents/pymes/n8n
docker-compose up -d

# Verificar que esté corriendo
docker-compose ps

# Deberías ver:
# Name              State    Ports
# n8n_postgres_1    Up       5432->5432
# n8n_n8n_1         Up       5678->5678

# Ver logs (útil para debugging)
docker-compose logs -f n8n
```

### Paso 5: Acceder a n8n

```bash
# Abrir en navegador
open http://localhost:5678

# O simplemente ir a: http://localhost:5678
```

**Primera vez:**
1. Te pedirá usuario/contraseña (los que pusiste en docker-compose.yml)
2. Login con: `admin` / `your_password`
3. ¡Listo! Ya tienes n8n corriendo

### Paso 6: Instalar ngrok (Para Webhooks Externos)

```bash
# Instalar ngrok
brew install ngrok

# O descargar de: https://ngrok.com/download
```

**Iniciar túnel ngrok:**

```bash
# En una terminal nueva (dejar corriendo)
ngrok http 5678

# Output:
# Forwarding  https://abc123.ngrok.io -> http://localhost:5678
```

**Copiar la URL HTTPS** (ej: `https://abc123.ngrok.io`)

### Paso 7: Actualizar Webhook URL en n8n

1. En n8n, ir a **Settings** (⚙️)
2. Buscar **Webhook URL**
3. Cambiar a: `https://abc123.ngrok.io/` (tu URL de ngrok)
4. **Save**

---

## Configuración de Servicios Externos

### 1. OpenAI API

**Obtener API Key:**

1. Ir a: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click **Create new secret key**
4. Copiar key (empieza con `sk-...`)
5. **IMPORTANTE:** Guardar en lugar seguro, no se puede ver de nuevo

**Agregar a n8n:**

1. En n8n, ir a **Credentials** (🔑)
2. Click **Add Credential**
3. Buscar **OpenAI**
4. Pegar API Key
5. **Save**

**Configurar límites de gasto (IMPORTANTE):**

1. Ir a: https://platform.openai.com/account/billing/limits
2. Set **Monthly budget**: $50 (o tu límite deseado)
3. Enable **Email alerts** al 75% y 90%

### 2. Twilio WhatsApp API

**Setup (Sandbox - Gratis para Testing):**

1. Ir a: https://www.twilio.com/try-twilio
2. Sign up (gratis, te dan $15 crédito)
3. Verificar email y teléfono
4. Ir a **Messaging** → **Try it Out** → **Send a WhatsApp message**

**Configurar WhatsApp Sandbox:**

1. En Twilio Console, ir a: **Messaging** → **Try WhatsApp**
2. Verás un número como: `+1 415 523 8886`
3. Y un código como: `join your-code-here`
4. En tu WhatsApp personal:
   - Agregar el número de Twilio
   - Enviar: `join your-code-here`
   - Recibirás: "You are now connected!"

**Configurar Webhook:**

1. En Twilio Console: **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
2. En **When a message comes in**:
   - URL: `https://abc123.ngrok.io/webhook/whatsapp/test` (tu URL ngrok)
   - Method: **POST**
3. **Save**

**Obtener Credentials:**

1. Ir a: **Account** → **Account Info**
2. Copiar:
   - **Account SID** (empieza con `AC...`)
   - **Auth Token** (click para revelar)

**Agregar a n8n:**

1. En n8n, **Credentials** → **Add Credential**
2. Buscar **Twilio**
3. Pegar:
   - Account SID
   - Auth Token
4. **Save**

### 3. Pinecone (Vector Database)

**Setup (Free Tier):**

1. Ir a: https://www.pinecone.io/
2. Sign up (gratis, no necesita tarjeta)
3. Create new project

**Crear Index:**

1. Click **Create Index**
2. Configurar:
   - **Index name**: `chatbot-knowledge`
   - **Dimensions**: `1536` (para OpenAI embeddings)
   - **Metric**: `cosine`
   - **Pod type**: `starter` (gratis)
3. **Create Index**

**Obtener API Key:**

1. Ir a **API Keys**
2. Copy **API Key**
3. Copy **Environment** (ej: `us-east-1-aws`)

**Agregar a n8n:**

1. n8n → **Credentials** → **HTTP Header Auth**
2. Name: `Pinecone API`
3. Header Name: `Api-Key`
4. Value: `tu-api-key-aqui`
5. **Save**

### 4. Supabase (PostgreSQL Gratis)

**Setup:**

1. Ir a: https://supabase.com/
2. Sign up con GitHub
3. **New Project**:
   - Name: `chatbot-db`
   - Database Password: (generar uno seguro)
   - Region: `East US` (o más cercano)
4. **Create project** (toma ~2 min)

**Obtener Connection String:**

1. Ir a **Settings** → **Database**
2. Copiar **Connection string** (URI mode):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
3. Reemplazar `[YOUR-PASSWORD]` con tu password

**Crear Tablas:**

1. Ir a **SQL Editor**
2. **New Query**
3. Pegar schema:

```sql
-- Clinics
CREATE TABLE clinics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(20) UNIQUE NOT NULL,
  plan VARCHAR(50) DEFAULT 'basic',
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  config JSONB DEFAULT '{}'::jsonb
);

-- Conversations
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clinic_id UUID REFERENCES clinics(id) ON DELETE CASCADE,
  customer_phone VARCHAR(20) NOT NULL,
  customer_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  last_message_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'active',
  UNIQUE(clinic_id, customer_phone)
);

-- Messages
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  direction VARCHAR(10) NOT NULL CHECK (direction IN ('inbound', 'outbound')),
  message_text TEXT NOT NULL,
  intent VARCHAR(100),
  response_time_ms INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB DEFAULT '{}'::jsonb
);

-- Knowledge Documents
CREATE TABLE knowledge_docs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clinic_id UUID REFERENCES clinics(id) ON DELETE CASCADE,
  title VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  doc_type VARCHAR(50),
  pinecone_ids TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_conversations_clinic ON conversations(clinic_id);
CREATE INDEX idx_conversations_phone ON conversations(customer_phone);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);
CREATE INDEX idx_knowledge_clinic ON knowledge_docs(clinic_id);

-- Insert test clinic
INSERT INTO clinics (name, phone, plan, config)
VALUES (
  'Clínica Test',
  '+573001234567',
  'basic',
  '{
    "whatsapp_number": "whatsapp:+14155238886",
    "business_hours": {
      "monday": {"open": "08:00", "close": "18:00"},
      "tuesday": {"open": "08:00", "close": "18:00"},
      "wednesday": {"open": "08:00", "close": "18:00"},
      "thursday": {"open": "08:00", "close": "18:00"},
      "friday": {"open": "08:00", "close": "18:00"},
      "saturday": {"open": "09:00", "close": "14:00"}
    }
  }'::jsonb
);
```

4. **Run** (Ctrl+Enter)

**Agregar a n8n:**

1. n8n → **Credentials** → **Postgres**
2. Pegar connection string
3. **Save**

---

## Crear Primer Workflow

### Workflow 1: WhatsApp Echo Bot (Test Simple)

Este workflow responde a cualquier mensaje con un eco.

**Pasos:**

1. En n8n, click **+ Add Workflow**
2. Nombrar: `whatsapp-echo-bot`

**Nodes:**

#### Node 1: Webhook (Trigger)

1. Agregar node: **Webhook**
2. Configurar:
   - HTTP Method: **POST**
   - Path: `whatsapp/test`
   - Response Mode: **Immediately**
3. **Test URL**: `https://abc123.ngrok.io/webhook/whatsapp/test`
4. Click **Listen for test event**
5. Enviar mensaje WhatsApp a tu sandbox number
6. Deberías ver el payload en n8n

#### Node 2: Extract Data (Code)

1. Agregar node: **Code**
2. Language: **JavaScript**
3. Code:

```javascript
// Extract WhatsApp message data
const from = $json.From.replace('whatsapp:', '');
const body = $json.Body;
const profileName = $json.ProfileName || 'Amigo';

return {
  customer_phone: from,
  customer_name: profileName,
  message: body,
  timestamp: new Date().toISOString()
};
```

4. Connect: Webhook → Code

#### Node 3: Create Response (Set)

1. Agregar node: **Set**
2. Keep Only Set: **✓**
3. Values:
   - Name: `response`
   - Value: `Hola {{ $json.customer_name }}! Recibí tu mensaje: "{{ $json.message }}". Este es un bot de prueba 🤖`
4. Connect: Code → Set

#### Node 4: Send WhatsApp (Twilio)

1. Agregar node: **Twilio**
2. Select Credential: (tu Twilio credential)
3. Resource: **Message**
4. Operation: **Send**
5. Configurar:
   - From: `whatsapp:+14155238886` (Twilio sandbox number)
   - To: `whatsapp:{{ $json.customer_phone }}`
   - Message: `{{ $json.response }}`
6. Connect: Set → Twilio

**Ejecutar Workflow:**

1. Click **Active** (toggle arriba a la derecha)
2. Enviar mensaje WhatsApp a tu sandbox
3. Deberías recibir respuesta!

**Debug si no funciona:**

1. Check n8n logs: **Executions** (panel izquierdo)
2. Click en execution más reciente
3. Ver cada node, qué data pasó

---

### Workflow 2: WhatsApp FAQ Bot (Con OpenAI)

Ahora vamos a crear uno que responde inteligentemente.

**Crear nuevo workflow:**

1. **+ Add Workflow**
2. Nombre: `whatsapp-faq-bot`

**Nodes:**

#### 1. Webhook (igual que antes)

```
Path: whatsapp/faq
```

#### 2. Extract Data (igual que antes)

#### 3. Load Context (Set - Simular knowledge base)

```javascript
// Por ahora, context hardcoded
// Después será Pinecone
const faqs = `
Clínica Odontológica Test
Ubicación: Calle 123, Medellín
Horario: Lun-Vie 8am-6pm, Sáb 9am-2pm
Servicios:
- Limpieza dental: $120,000 COP
- Blanqueamiento: $350,000 COP
- Ortodoncia: desde $2,500,000 COP
Teléfono: +57 300 123 4567
WhatsApp: Mismo número
`;

return {
  ...$ json,
  knowledge_context: faqs
};
```

#### 4. Call OpenAI (OpenAI Chat)

1. Node: **OpenAI Chat Model**
2. Credential: (tu OpenAI credential)
3. Model: **gpt-4o-mini**
4. Messages:
   - **System Message**:
   ```
   Eres el asistente virtual de Clínica Odontológica Test.

   Responde de forma amable, profesional y concisa (máx 3-4 líneas).
   Usa la información del contexto para responder.
   Si no sabes algo, di "Déjame conectarte con nuestro equipo".
   Usa emojis ocasionalmente 😊

   Contexto:
   {{ $json.knowledge_context }}
   ```

   - **User Message**:
   ```
   {{ $json.message }}
   ```

5. Options:
   - Temperature: `0.3`
   - Max Tokens: `150`

#### 5. Save to DB (PostgreSQL)

```sql
-- Upsert conversation
INSERT INTO conversations (clinic_id, customer_phone, customer_name, last_message_at)
VALUES (
  (SELECT id FROM clinics WHERE name = 'Clínica Test'),
  '{{ $json.customer_phone }}',
  '{{ $json.customer_name }}',
  NOW()
)
ON CONFLICT (clinic_id, customer_phone)
DO UPDATE SET last_message_at = NOW()
RETURNING id;
```

Luego otro node PostgreSQL:

```sql
-- Insert message
INSERT INTO messages (conversation_id, direction, message_text)
VALUES (
  '{{ $json.id }}',
  'inbound',
  '{{ $json.message }}'
);
```

#### 6. Send Response (Twilio)

Same as before, pero ahora con la respuesta de OpenAI:

```
Message: {{ $json.output }}
```

**Activar y probar:**

1. **Active** = ON
2. Update Twilio webhook URL: `https://abc123.ngrok.io/webhook/whatsapp/faq`
3. Enviar preguntas:
   - "Cuánto cuesta una limpieza?"
   - "Cuál es el horario?"
   - "Dónde quedan ubicados?"

**Deberías recibir respuestas inteligentes! 🎉**

---

## Testing con Twilio Sandbox

### Casos de Prueba

```bash
# Test 1: FAQ básico
Enviar: "Hola, cuánto cuesta una limpieza dental?"
Esperar: Respuesta con precio ($120,000 COP)

# Test 2: Horarios
Enviar: "Qué horario tienen?"
Esperar: Lun-Vie 8am-6pm, etc

# Test 3: Fuera de knowledge
Enviar: "Hacen cirugía de corazón?"
Esperar: "Déjame conectarte con nuestro equipo" (no debe inventar)

# Test 4: Conversación multi-turn
Enviar: "Hola"
Esperar: Saludo
Enviar: "Cuánto cuesta blanqueamiento?"
Esperar: Precio con contexto de conversación
```

### Debugging

**Si no recibes respuestas:**

1. **Check n8n executions:**
   - Panel izquierdo → **Executions**
   - Ver última ejecución
   - Ver error en qué node falló

2. **Check Twilio logs:**
   - Twilio Console → **Monitor** → **Logs** → **Messaging**
   - Ver si webhook fue llamado
   - Ver HTTP response code

3. **Check ngrok:**
   - En terminal de ngrok, ver requests entrantes
   - Deberían ver `POST /webhook/whatsapp/faq`

**Errores comunes:**

```bash
# Error: "Webhook not found"
→ Verificar URL en Twilio tiene el path correcto
→ Workflow está Active en n8n

# Error: "Invalid API key"
→ Credentials en n8n están correctas
→ Re-authenticate la credential

# Error: "Rate limit exceeded"
→ OpenAI tiene límites en free tier
→ Wait 1 minuto e intenta de nuevo

# Error: "Database connection failed"
→ Supabase connection string correcta
→ Database no está pausada (Supabase free tier pausa después de 1 semana sin uso)
```

---

## Deploy a Oracle Cloud

### ¿Por qué Oracle Cloud?

- ✅ **Gratis PARA SIEMPRE** (no es trial)
- ✅ ARM VM con 1-4 CPUs + 24GB RAM (generoso!)
- ✅ Always-on (no sleep como Render free tier)
- ✅ Public IP incluida
- ✅ 200GB block storage + 10TB transfer/mes

### Paso 1: Crear Cuenta Oracle Cloud

1. Ir a: https://www.oracle.com/cloud/free/
2. **Start for free**
3. Llenar formulario:
   - Nombre, email, país (Colombia)
   - **IMPORTANTE:** Necesita tarjeta de crédito para verificación
   - **NO TE COBRAN** en free tier
4. Verificar email
5. Login a: https://cloud.oracle.com/

### Paso 2: Crear VM Instance

1. En dashboard, click **Create a VM instance**
2. Configurar:
   - **Name**: `n8n-production`
   - **Placement**: Default
   - **Image**: Ubuntu 22.04 (Minimal)
   - **Shape**:
     - Click **Change shape**
     - Select **Ampere** (ARM)
     - OCPUs: `2` (o más si está disponible)
     - Memory: `12 GB`
   - **Networking**:
     - Create new VCN: `n8n-vcn`
     - Assign public IP: **Yes**
   - **SSH Keys**:
     - **Generate SSH key pair**
     - Download private key (.pem file)
     - ⚠️ **GUARDAR EN LUGAR SEGURO**

3. **Create** (toma ~2 min)

4. **Copiar Public IP** (ej: `140.238.123.45`)

### Paso 3: Configurar Security List (Firewall)

1. En tu instancia, click **Subnet** link
2. Click en **Default Security List**
3. **Add Ingress Rule**:

```
# Rule 1: HTTP
Source CIDR: 0.0.0.0/0
IP Protocol: TCP
Destination Port: 80

# Rule 2: HTTPS
Source CIDR: 0.0.0.0/0
IP Protocol: TCP
Destination Port: 443

# Rule 3: n8n (temporal, luego bloquear)
Source CIDR: 0.0.0.0/0
IP Protocol: TCP
Destination Port: 5678
```

4. **Save**

### Paso 4: Conectar vía SSH

```bash
# En tu Mac, mover la key descargada
mv ~/Downloads/ssh-key-*.pem ~/.ssh/oracle-key.pem
chmod 400 ~/.ssh/oracle-key.pem

# Conectar (reemplazar IP con la tuya)
ssh -i ~/.ssh/oracle-key.pem ubuntu@140.238.123.45

# Primera vez dirá: "Are you sure?" → yes
```

**Ahora estás dentro del servidor! 🎉**

### Paso 5: Instalar Docker

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario a grupo docker
sudo usermod -aG docker ubuntu

# Logout y login de nuevo
exit
ssh -i ~/.ssh/oracle-key.pem ubuntu@140.238.123.45

# Verificar
docker --version
```

### Paso 6: Instalar Docker Compose

```bash
# Instalar
sudo apt install docker-compose -y

# Verificar
docker-compose --version
```

### Paso 7: Transferir Config de n8n

**Desde tu Mac:**

```bash
# Comprimir carpeta n8n local
cd /Users/nico/Documents/pymes
tar -czf n8n-config.tar.gz n8n/

# Transferir al servidor
scp -i ~/.ssh/oracle-key.pem n8n-config.tar.gz ubuntu@140.238.123.45:~/
```

**En el servidor:**

```bash
# Descomprimir
tar -xzf n8n-config.tar.gz

# Entrar
cd n8n/

# Editar docker-compose.yml
nano docker-compose.yml
```

**Cambiar WEBHOOK_URL:**

```yaml
- WEBHOOK_URL=http://140.238.123.45:5678/  # Tu IP pública
```

**Guardar: Ctrl+O, Enter, Ctrl+X**

### Paso 8: Iniciar n8n en Producción

```bash
# Iniciar
docker-compose up -d

# Verificar
docker-compose ps

# Ver logs
docker-compose logs -f n8n

# Presionar Ctrl+C para salir de logs (n8n sigue corriendo)
```

### Paso 9: Acceder a n8n

```bash
# Desde tu Mac, abrir navegador:
http://140.238.123.45:5678
```

**Login con tus credentials y listo! 🚀**

### Paso 10: Configurar Dominio (Opcional)

**Si tienes un dominio (ej: `n8n.tuempresa.com`):**

1. En tu proveedor DNS (Namecheap, Cloudflare, etc):
   - Agregar A record:
   - Name: `n8n`
   - Value: `140.238.123.45` (tu IP)
   - TTL: 300

2. En servidor, instalar Caddy (reverse proxy + HTTPS automático):

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy -y
```

3. Configurar Caddy:

```bash
sudo nano /etc/caddy/Caddyfile
```

**Contenido:**

```
n8n.tuempresa.com {
    reverse_proxy localhost:5678
}
```

4. Reiniciar Caddy:

```bash
sudo systemctl restart caddy
```

**Ahora n8n está en: `https://n8n.tuempresa.com` con HTTPS automático! 🔒**

### Paso 11: Actualizar Twilio Webhooks

1. En Twilio Console
2. **Messaging** → **WhatsApp Sandbox Settings**
3. Webhook URL: `https://n8n.tuempresa.com/webhook/whatsapp/faq`
4. **Save**

**Ya no necesitas ngrok! Todo está en producción.**

---

## Troubleshooting

### n8n no inicia

```bash
# Ver logs completos
docker-compose logs n8n

# Errores comunes:

# 1. Puerto ocupado
Error: "bind: address already in use"
→ Cambiar puerto en docker-compose.yml: "5679:5678"

# 2. Database no conecta
Error: "ECONNREFUSED postgres:5432"
→ Wait 30 segundos más (PostgreSQL tarda en iniciar)
→ docker-compose restart n8n

# 3. Out of memory
→ Reducir otros containers corriendo
→ Aumentar RAM de VM en Oracle
```

### Workflows no se ejecutan

```bash
# Check si workflow está Active
→ Toggle debe estar ON (verde)

# Check executions
→ Panel izquierdo → Executions
→ Ver error en node específico

# Reiniciar n8n
docker-compose restart n8n
```

### Twilio no llama webhook

```bash
# 1. Verificar URL es accesible
curl https://n8n.tuempresa.com/webhook/whatsapp/faq
→ Debe responder (aunque sea error, no timeout)

# 2. Check Twilio logs
→ Twilio Console → Monitor → Logs
→ Ver HTTP status code

# 3. Check n8n recibe request
→ n8n → Executions
→ Debe aparecer nueva ejecución cuando envías WhatsApp
```

### Database errors

```bash
# Supabase pausó database (free tier)
→ Ir a Supabase dashboard
→ Click "Restore database"

# Connection string incorrecta
→ Re-check en Supabase → Settings → Database
→ Re-paste en n8n credential
```

### OpenAI rate limits

```bash
Error: "Rate limit exceeded"

→ Wait 60 segundos
→ O upgrade a paid plan en OpenAI
→ O cambiar a GPT-4o-mini (más barato)
```

---

## Comandos Útiles

```bash
# Ver todos los containers corriendo
docker ps

# Ver logs de n8n
docker-compose logs -f n8n

# Ver logs de PostgreSQL
docker-compose logs -f postgres

# Reiniciar un servicio
docker-compose restart n8n

# Detener todo
docker-compose down

# Detener y eliminar volumes (⚠️ PIERDE DATA)
docker-compose down -v

# Backup de workflows
cd n8n/
tar -czf backup-$(date +%Y%m%d).tar.gz workflows/

# Restore de workflows
tar -xzf backup-20240115.tar.gz

# Update n8n a latest version
docker-compose pull n8n
docker-compose up -d n8n

# Ver uso de disco
docker system df

# Limpiar images viejas
docker system prune -a
```

---

## Próximos Pasos

Después de tener n8n corriendo en producción:

1. ✅ **Crear workflows avanzados** (Ver CHATBOT_PLATFORM.md)
2. ✅ **Ingest knowledge base a Pinecone** (Ver workflow knowledge-base-sync)
3. ✅ **Build internal chat UI** (Next.js app)
4. ✅ **Onboard primer cliente** (Duplicar workflows con su config)
5. ✅ **Monitor y optimizar** (Review executions, tiempos de respuesta)

---

**Última actualización:** 2026-01-02
**Autor:** Nico
**¿Necesitas ayuda?** Revisa Executions en n8n para ver errores específicos
