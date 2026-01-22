# 🤖 Chatbot Platform - Arquitectura Completa

## 📋 Índice

1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Workflows n8n Detallados](#workflows-n8n-detallados)
5. [Prompts y Configuración de IA](#prompts-y-configuración-de-ia)
6. [Base de Datos](#base-de-datos)
7. [Knowledge Base](#knowledge-base)
8. [Interfaz de Usuario](#interfaz-de-usuario)
9. [Seguridad y Compliance](#seguridad-y-compliance)
10. [Deployment](#deployment)
11. [Monitoreo y Analytics](#monitoreo-y-analytics)
12. [Roadmap](#roadmap)

---

## Visión General

### Propósito

Plataforma SaaS de chatbots dual-purpose para PYMEs en Colombia:

1. **Bot Externo (WhatsApp)** - Atiende clientes finales 24/7
2. **Chat Interno** - Ayuda al equipo con knowledge base empresarial

### Ventaja Competitiva

- ✅ Una plataforma, dos casos de uso (mayor valor)
- ✅ No-code/Low-code con n8n (rápida iteración)
- ✅ Multi-tenant desde el inicio
- ✅ Costo operacional ultra-bajo (70-80% profit margin)
- ✅ Leads precalificados (569 con WhatsApp)

### ICP (Ideal Customer Profile)

- **Industria:** Clínicas (odontológicas, estéticas, médicas)
- **Tamaño:** 2-10 empleados
- **Revenue:** $50K-500K USD/año
- **Problema:** Alto volumen de consultas WhatsApp, respuestas lentas
- **Budget:** $100-300 USD/mes para automatización
- **Location:** Colombia (Medellín, Bogotá, Cali, Barranquilla, Cartagena)

---

## Arquitectura del Sistema

### Diagrama de Alto Nivel

```
┌────────────────────────────────────────────────────────────────┐
│                    CHATBOT PLATFORM                             │
│                  (Multi-Tenant SaaS)                            │
└────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
  ┌──────────┐         ┌──────────┐         ┌──────────┐
  │ WhatsApp │         │ Internal │         │   Admin  │
  │  Client  │         │   Chat   │         │Dashboard │
  │  (Twilio)│         │(Next.js) │         │(Retool)  │
  └──────────┘         └──────────┘         └──────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                         Webhooks
                              │
                              ▼
              ┌───────────────────────────┐
              │    n8n WORKFLOW ENGINE    │
              │   (Central Orchestrator)  │
              └───────────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
┌────────────┐         ┌────────────┐        ┌────────────┐
│  OpenAI    │         │  Pinecone  │        │PostgreSQL  │
│  Claude    │         │  (Vectors) │        │   (Data)   │
│   (LLM)    │         │            │        │            │
└────────────┘         └────────────┘        └────────────┘
       │                      │                      │
       └──────────────────────┴──────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  Knowledge Base   │
                    │  (Per Clinic)     │
                    └───────────────────┘
```

### Flujo de Datos - WhatsApp Client Bot

```
1. Cliente envía mensaje WhatsApp
        ↓
2. Twilio recibe → POST a webhook n8n
        ↓
3. n8n: Extract clinic_id, phone, message
        ↓
4. Load clinic config (PostgreSQL)
        ↓
5. Load conversation history (últimos 5 mensajes)
        ↓
6. Classify intent (OpenAI GPT-4o-mini)
        ↓
   ├─ FAQ → Search knowledge base (Pinecone)
   ├─ Appointment → Create ticket + notify team
   └─ Complex → Escalate to human
        ↓
7. Generate response (OpenAI GPT-4)
        ↓
8. Save to conversation_logs (PostgreSQL)
        ↓
9. Send WhatsApp message (Twilio API)
        ↓
10. Log metrics (response time, intent, etc)
```

### Flujo de Datos - Internal Chat

```
1. Team member types question in web chat
        ↓
2. Next.js → POST to n8n webhook
        ↓
3. n8n: Authenticate user (JWT token)
        ↓
4. Determine query type:
   ├─ Knowledge search
   ├─ Draft client response
   └─ Document summarization
        ↓
5. Vector search (Pinecone)
        ↓
6. Generate answer with context (Claude Sonnet)
        ↓
7. Return formatted JSON response
        ↓
8. Next.js displays answer with sources
```

---

## Stack Tecnológico

### Orquestación (Core)

**n8n**
- Versión: Latest (Docker)
- Hosting: Self-hosted (local MVP → Oracle Cloud producción)
- Database: PostgreSQL (compartida con app data)
- Backup: Export workflows as JSON (git repo)

### AI/LLM

**OpenAI**
- GPT-4o-mini: Intent classification, FAQ responses ($0.15/$0.60 per 1M tokens)
- GPT-4: Complex responses cuando needed ($2.50/$10.00 per 1M tokens)
- text-embedding-3-small: Embeddings ($0.02 per 1M tokens)

**Claude (Anthropic)**
- Claude 3.5 Sonnet: Internal chat, draft generation ($3/$15 per 1M tokens)
- Usage: Secondary, cuando OpenAI no es suficiente

**Estimación de costos IA (10 clientes):**
```
- 10 clientes × 500 mensajes/mes = 5,000 mensajes
- Promedio 200 tokens input + 150 tokens output
- GPT-4o-mini: ~$3-5/mes
- Embeddings: ~$1/mes
- Claude (occasional): ~$5-10/mes
Total: $9-16/mes para 10 clientes
```

### WhatsApp Integration

**Twilio WhatsApp API**
- Costo: $0.005 por mensaje (outbound)
- Setup: WhatsApp sandbox (gratis testing) → Production number
- Features: Media messages, templates, interactive messages

**Meta WhatsApp Business API** (Fase 2)
- Costo: ~$0.003 por mensaje (cheaper at scale)
- Requiere: Business verification (2-3 semanas)
- Migration path: Cuando llegues a 20+ clientes

### Vector Database

**Pinecone**
- Plan: Free tier (100K vectors, suficiente para 50-100 clientes)
- Dimensiones: 1536 (OpenAI text-embedding-3-small)
- Namespace strategy: Un namespace por clinic_id
- Alternativa: Supabase pgvector (si quieres todo en PostgreSQL)

### Database

**PostgreSQL (Supabase Free Tier)**
- Storage: 500MB (suficiente para 100K+ conversaciones)
- Bandwidth: Unlimited
- Backups: Daily automated

**Schema principal:**

```sql
-- Clinics
CREATE TABLE clinics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(20) UNIQUE NOT NULL,
  plan VARCHAR(50) DEFAULT 'basic',
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  config JSONB -- Settings específicas por clínica
);

-- Conversations
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clinic_id UUID REFERENCES clinics(id),
  customer_phone VARCHAR(20) NOT NULL,
  customer_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  last_message_at TIMESTAMP DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'active', -- active, resolved, escalated
  assigned_to VARCHAR(100) -- Staff member si escalado
);

-- Messages
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id),
  direction VARCHAR(10) NOT NULL, -- inbound, outbound
  message_text TEXT NOT NULL,
  intent VARCHAR(100), -- Clasificación de OpenAI
  response_time_ms INTEGER, -- Performance metric
  created_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB -- Media, buttons, etc
);

-- Knowledge Documents
CREATE TABLE knowledge_docs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clinic_id UUID REFERENCES clinics(id),
  title VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  doc_type VARCHAR(50), -- faq, policy, service_info
  pinecone_ids TEXT[], -- IDs de vectors en Pinecone
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Users (Internal chat)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clinic_id UUID REFERENCES clinics(id),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'staff', -- admin, staff
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Frontend

**Internal Chat (Next.js 14)**
- Framework: Next.js 14 (App Router)
- UI: Shadcn/ui + Tailwind CSS
- Auth: Clerk o NextAuth
- Deploy: Vercel free tier
- Features:
  - Chat interface (conversational)
  - Document upload para knowledge base
  - Analytics básico
  - User management

**Admin Dashboard (Fase 2)**
- Option A: Retool (rapid prototyping)
- Option B: Custom React app
- Features:
  - Clinic management
  - View conversations
  - Edit knowledge base
  - Analytics & metrics
  - Billing

### Hosting

**MVP (Semanas 1-3):**
- n8n: Docker local en tu Mac
- PostgreSQL: Supabase free tier (cloud)
- Next.js: Vercel free tier
- Expose: ngrok free tier

**Producción (Semanas 4+):**
- n8n: Oracle Cloud Free Tier (ARM VM)
- PostgreSQL: Supabase free tier
- Next.js: Vercel free tier
- Domain: Namecheap ($12/year)
- Total: ~$1/mes

---

## Workflows n8n Detallados

### 1. whatsapp-client-bot.json

**Trigger:** Webhook (POST from Twilio)

**Nodes:**

```
1. Webhook Trigger
   - URL: /webhook/whatsapp/{clinic_id}
   - Method: POST
   - Response: 200 OK (immediate)

2. Extract Data (Code Node)
   ```javascript
   const from = $json.From.replace('whatsapp:', '');
   const body = $json.Body;
   const profileName = $json.ProfileName || 'Cliente';
   const clinicId = $parameter.clinic_id;

   return {
     clinic_id: clinicId,
     customer_phone: from,
     customer_name: profileName,
     message: body,
     timestamp: new Date().toISOString()
   };
   ```

3. Check Business Hours (IF Node)
   ```javascript
   const now = new Date();
   const hour = now.getHours();
   const day = now.getDay();

   // Mon-Fri 8AM-6PM, Sat 9AM-2PM
   const isOpen =
     (day >= 1 && day <= 5 && hour >= 8 && hour < 18) ||
     (day === 6 && hour >= 9 && hour < 14);

   return isOpen;
   ```
   - TRUE → Continue
   - FALSE → Send "Fuera de horario" message + Create ticket

4. Load Clinic Config (PostgreSQL Node)
   ```sql
   SELECT * FROM clinics WHERE id = '{{ $json.clinic_id }}';
   ```

5. Load Conversation History (PostgreSQL Node)
   ```sql
   SELECT m.* FROM messages m
   JOIN conversations c ON m.conversation_id = c.id
   WHERE c.customer_phone = '{{ $json.customer_phone }}'
     AND c.clinic_id = '{{ $json.clinic_id }}'
   ORDER BY m.created_at DESC
   LIMIT 5;
   ```

6. Classify Intent (OpenAI Chat Node)
   - Model: gpt-4o-mini
   - Temperature: 0.1
   - System Prompt:
   ```
   Eres un clasificador de intenciones para una clínica.
   Analiza el mensaje del cliente y clasifica en UNA de estas categorías:

   - faq_pricing: Preguntas sobre precios
   - faq_services: Preguntas sobre servicios ofrecidos
   - faq_location: Preguntas sobre ubicación/dirección
   - appointment_new: Solicitud de nueva cita
   - appointment_change: Cambio/cancelación de cita
   - complaint: Queja o insatisfacción
   - other: Otros temas

   Responde SOLO con la categoría, nada más.
   ```
   - User Message: `{{ $json.message }}`

7. Switch (Route by Intent)
   - FAQ intents → Route A (Knowledge Search)
   - Appointment intents → Route B (Ticket Creation)
   - Complaint → Route C (Immediate Escalation)
   - Other → Route D (Gentle Response + Escalation)

8a. Route A: FAQ Handler
   - Search Pinecone (HTTP Request Node)
   ```javascript
   // Call Pinecone API
   {
     method: 'POST',
     url: 'https://YOUR-INDEX.pinecone.io/query',
     headers: {
       'Api-Key': '{{ $env.PINECONE_API_KEY }}',
       'Content-Type': 'application/json'
     },
     body: {
       namespace: '{{ $json.clinic_id }}',
       topK: 3,
       includeMetadata: true,
       vector: '{{ $json.embedding }}' // From embedding node
     }
   }
   ```

   - Generate Response (OpenAI Chat Node)
   - Model: gpt-4o-mini
   - Temperature: 0.3
   - System Prompt:
   ```
   Eres el asistente virtual de {{ $json.clinic_name }}.

   Instrucciones:
   - Responde de forma amable, profesional y concisa
   - Usa la información del contexto proporcionado
   - Si no sabes algo, NO INVENTES. Di "Déjame conectarte con nuestro equipo"
   - Máximo 3-4 líneas de respuesta
   - Usa emojis ocasionalmente (1-2 por mensaje máximo)
   - Siempre ofrece ayuda adicional al final

   Contexto relevante:
   {{ $json.knowledge_context }}

   Historial reciente:
   {{ $json.conversation_history }}
   ```
   - User Message: `{{ $json.message }}`

8b. Route B: Appointment Handler
   - Create Ticket (PostgreSQL Node)
   - Notify Team (Slack/Email Node)
   - Send Confirmation (Twilio Node)

8c. Route C: Complaint Handler
   - Immediate escalation
   - Send empathy message
   - Create priority ticket
   - Alert manager

9. Save to Database (PostgreSQL Node)
   ```sql
   -- Upsert conversation
   INSERT INTO conversations (clinic_id, customer_phone, customer_name, last_message_at)
   VALUES ('{{ $json.clinic_id }}', '{{ $json.customer_phone }}', '{{ $json.customer_name }}', NOW())
   ON CONFLICT (clinic_id, customer_phone)
   DO UPDATE SET last_message_at = NOW()
   RETURNING id;

   -- Insert message
   INSERT INTO messages (conversation_id, direction, message_text, intent, response_time_ms)
   VALUES (
     '{{ $json.conversation_id }}',
     'inbound',
     '{{ $json.message }}',
     '{{ $json.intent }}',
     '{{ $json.response_time }}'
   );
   ```

10. Send WhatsApp Response (Twilio Node)
   - To: `{{ $json.customer_phone }}`
   - From: `{{ $json.clinic_whatsapp_number }}`
   - Body: `{{ $json.response }}`

11. Log Metrics (Code Node)
   ```javascript
   // Calculate metrics
   const responseTime = Date.now() - new Date($json.timestamp).getTime();
   return {
     clinic_id: $json.clinic_id,
     intent: $json.intent,
     response_time_ms: responseTime,
     success: true
   };
   ```
```

**Estimación:** ~18-22 nodes total

### 2. internal-knowledge-chat.json

**Trigger:** Webhook (POST from Next.js)

**Nodes:**

```
1. Webhook Trigger
   - URL: /webhook/internal-chat
   - Method: POST
   - Authentication: API Key

2. Validate JWT (Code Node)
   ```javascript
   const jwt = require('jsonwebtoken');
   const token = $json.headers.authorization.replace('Bearer ', '');

   try {
     const decoded = jwt.verify(token, process.env.JWT_SECRET);
     return {
       user_id: decoded.user_id,
       clinic_id: decoded.clinic_id,
       question: $json.question
     };
   } catch (err) {
     throw new Error('Invalid token');
   }
   ```

3. Generate Embedding (OpenAI Embeddings Node)
   - Model: text-embedding-3-small
   - Input: `{{ $json.question }}`

4. Search Pinecone (HTTP Request Node)
   - Same as WhatsApp flow
   - Namespace: `{{ $json.clinic_id }}`

5. Load Additional Context (PostgreSQL Node)
   ```sql
   -- Get recent relevant conversations
   SELECT * FROM conversations
   WHERE clinic_id = '{{ $json.clinic_id }}'
   ORDER BY last_message_at DESC
   LIMIT 5;
   ```

6. Generate Answer (Claude Sonnet Node)
   - Model: claude-3-5-sonnet-20241022
   - Temperature: 0.2
   - System Prompt:
   ```
   Eres un asistente interno para el equipo de {{ $json.clinic_name }}.

   Tu rol:
   - Ayudar al equipo a encontrar información rápidamente
   - Generar drafts de respuestas para clientes
   - Resumir conversaciones y documentos

   Instrucciones:
   - Sé preciso y profesional
   - Cita fuentes cuando sea posible
   - Si generas un draft para cliente, usa tono amable
   - Incluye sugerencias adicionales cuando sean útiles

   Contexto disponible:
   {{ $json.knowledge_context }}
   ```
   - User Message: `{{ $json.question }}`

7. Format Response (Code Node)
   ```javascript
   return {
     answer: $json.response,
     sources: $json.sources.map(s => ({
       title: s.metadata.title,
       snippet: s.metadata.text.substring(0, 150) + '...',
       doc_id: s.id
     })),
     suggestions: [
       "¿Necesitas que genere un mensaje para el cliente?",
       "¿Quieres que busque más información sobre esto?"
     ]
   };
   ```

8. Return JSON (Webhook Response Node)
```

**Estimación:** ~10-12 nodes total

### 3. knowledge-base-sync.json

**Trigger:** Manual o Schedule (daily at 2 AM)

**Nodes:**

```
1. Trigger (Schedule/Manual)

2. Get All Clinics (PostgreSQL Node)
   ```sql
   SELECT id, name FROM clinics WHERE active = true;
   ```

3. Loop Over Clinics (Split In Batches Node)

4. Fetch Documents (Per Clinic)
   - Option A: Google Drive API
   - Option B: PostgreSQL (if uploaded via admin panel)

5. Split into Chunks (Code Node)
   ```javascript
   function chunkText(text, maxTokens = 1000) {
     const sentences = text.match(/[^.!?]+[.!?]+/g) || [];
     const chunks = [];
     let currentChunk = '';

     for (const sentence of sentences) {
       if ((currentChunk + sentence).length > maxTokens * 4) {
         chunks.push(currentChunk.trim());
         currentChunk = sentence;
       } else {
         currentChunk += sentence;
       }
     }
     if (currentChunk) chunks.push(currentChunk.trim());
     return chunks;
   }

   const chunks = chunkText($json.content);
   return chunks.map((chunk, i) => ({
     text: chunk,
     doc_id: $json.doc_id,
     chunk_index: i,
     clinic_id: $json.clinic_id
   }));
   ```

6. Generate Embeddings (OpenAI Embeddings Node)
   - Batch process chunks

7. Upsert to Pinecone (HTTP Request Node)
   ```javascript
   {
     method: 'POST',
     url: 'https://YOUR-INDEX.pinecone.io/vectors/upsert',
     body: {
       vectors: $json.chunks.map(chunk => ({
         id: `${chunk.doc_id}_${chunk.chunk_index}`,
         values: chunk.embedding,
         metadata: {
           clinic_id: chunk.clinic_id,
           text: chunk.text,
           doc_id: chunk.doc_id
         }
       })),
       namespace: $json.clinic_id
     }
   }
   ```

8. Update Database (PostgreSQL Node)
   ```sql
   UPDATE knowledge_docs
   SET pinecone_ids = '{{ $json.vector_ids }}'::text[],
       updated_at = NOW()
   WHERE id = '{{ $json.doc_id }}';
   ```

9. Log Success (Code Node)
```

**Estimación:** ~10-12 nodes total

---

## Prompts y Configuración de IA

### WhatsApp Bot - System Prompts por Industria

**Clínica Odontológica:**
```
Eres el asistente virtual de [NOMBRE_CLINICA], una clínica odontológica en [CIUDAD].

PERSONALIDAD:
- Profesional pero amigable
- Empático con pacientes nerviosos
- Claro y directo

CAPABILITIES (lo que SÍ puedes hacer):
- Responder preguntas sobre servicios y precios
- Proporcionar horarios e información de contacto
- Agendar citas (crear ticket para equipo)
- Recordatorios de citas
- Primeros pasos antes/después de procedimientos

LIMITACIONES (lo que NO puedes hacer):
- No das diagnósticos médicos
- No cambias tratamientos sin aprobar con doctor
- No prometes resultados específicos
- No compartes info médica confidencial

TONO:
- Usa "usted" (formal pero cercano)
- Emojis ocasionales (😊 ✨ 🦷)
- Máximo 3-4 líneas por respuesta
- Siempre termina ofreciendo más ayuda

Si no sabes algo: "Déjame conectarte con nuestro equipo que te puede ayudar mejor con esto. ¿Te parece?"
```

**Clínica Estética:**
```
Eres el asistente virtual de [NOMBRE_CLINICA], especialistas en medicina estética.

PERSONALIDAD:
- Profesional y elegante
- Comprensivo y sin juicios
- Enfoque en resultados y seguridad

CAPABILITIES:
- Información sobre tratamientos (Botox, rellenos, etc)
- Precios y paquetes
- Agendar consultas de valoración
- Cuidados pre/post tratamiento
- Promociones vigentes

LIMITACIONES:
- No prometes resultados específicos
- Siempre recomiendas consulta presencial primero
- No compartes fotos de pacientes sin consent

TONO:
- Elegante y aspiracional
- Emojis selectivos (✨ 💕)
- Destaca seguridad y experiencia de médicos

Cierre típico: "¿Te gustaría agendar una consulta de valoración sin compromiso?"
```

### Internal Chat - System Prompt

```
Eres un asistente interno avanzado para el equipo de [NOMBRE_CLINICA].

ROLES:
1. Knowledge Search - Encuentra información en documentos internos
2. Draft Generator - Crea respuestas profesionales para clientes
3. Summarizer - Resume conversaciones y documentos
4. Analyst - Identifica patrones en consultas de clientes

INSTRUCCIONES:
- Sé preciso y cita fuentes siempre que sea posible
- Cuando generes drafts para clientes, usa el tono de marca
- Incluye sugerencias proactivas si ves oportunidades
- Sé transparente sobre limitaciones

FORMATO DE RESPUESTA:
- Answer: La respuesta principal
- Sources: Links/references a docs originales
- Suggestions: Próximos pasos recomendados

EJEMPLOS:

Usuario: "¿Cuánto cuesta una limpieza dental?"
Respuesta:
{
  "answer": "Según nuestra lista de precios actualizada el 2024-01-15, la limpieza dental (profilaxis) tiene un costo de $120,000 COP. Incluye: [detalles].",
  "sources": ["pricing_2024.pdf", "services_catalog.xlsx"],
  "suggestions": [
    "¿Necesitas que genere un mensaje para enviar al cliente?",
    "También tenemos el paquete de limpieza + blanqueamiento con descuento."
  ]
}

Usuario: "Draft una respuesta para un cliente que pregunta sobre ortodoncia"
Respuesta:
{
  "answer": "Aquí está el draft:\n\n'¡Hola! Qué bueno que te interese la ortodoncia 😊\n\nTenemos varias opciones:\n- Brackets metálicos: $XXX\n- Brackets estéticos: $XXX\n- Invisalign: $XXX\n\n¿Te gustaría agendar una valoración gratuita para ver cuál es mejor para ti?'",
  "sources": ["orthodontics_info.pdf"],
  "suggestions": [
    "¿Envío este mensaje o quieres que haga ajustes?",
    "Recuerda mencionar la promo de enero si aplica."
  ]
}
```

---

## Knowledge Base

### Estructura de Templates

**Cada clínica nueva recibe un template base según su industria:**

```
knowledge-base/
├── templates/
│   ├── clinica-odontologica/
│   │   ├── faqs.json
│   │   ├── servicios.json
│   │   ├── precios.json (placeholder)
│   │   └── politicas.json
│   │
│   ├── clinica-estetica/
│   │   ├── faqs.json
│   │   ├── tratamientos.json
│   │   ├── cuidados.json
│   │   └── promociones.json
│   │
│   └── general/
│       ├── horarios.json
│       ├── ubicacion.json
│       └── contacto.json
```

### Ejemplo: faqs.json (Clínica Odontológica)

```json
{
  "clinic_type": "odontologia",
  "version": "1.0",
  "last_updated": "2024-01-01",
  "faqs": [
    {
      "question": "¿Cuánto cuesta una limpieza dental?",
      "answer": "El costo de una limpieza dental profesional (profilaxis) es de [PRECIO] COP. Incluye:\n- Remoción de placa y sarro\n- Pulido dental\n- Aplicación de flúor\n- Revisión general\n\nDuración aproximada: 45-60 minutos.\n\n¿Te gustaría agendar una cita?",
      "keywords": ["precio", "limpieza", "profilaxis", "cuánto cuesta"],
      "category": "pricing"
    },
    {
      "question": "¿Cada cuánto debo hacerme limpieza dental?",
      "answer": "Se recomienda una limpieza dental profesional cada 6 meses para mantener una buena salud bucal.\n\nSi tienes:\n- Brackets: cada 3-4 meses\n- Enfermedad periodontal: cada 3 meses\n- Alto consumo de café/tabaco: cada 4-5 meses\n\nTu odontólogo te indicará la frecuencia ideal en tu caso.",
      "keywords": ["frecuencia", "cada cuánto", "periodicidad", "regularidad"],
      "category": "service_info"
    },
    {
      "question": "¿Aceptan seguros médicos?",
      "answer": "[PERSONALIZAR POR CLÍNICA]\n\nOpciones comunes:\nA) Sí, trabajamos con: Sura, Sanitas, Compensar\nB) No, pero emitimos facturas para que reclames con tu EPS/Seguro\nC) Planes de financiación propios disponibles",
      "keywords": ["seguro", "eps", "cobertura", "sura", "sanitas"],
      "category": "payment"
    },
    {
      "question": "¿Qué debo hacer si tengo una emergencia dental?",
      "answer": "Para emergencias dentales:\n\n1. **Durante horario:** Llama al [TELEFONO] o ven directamente\n2. **Fuera de horario:** Envía WhatsApp, revisamos cada hora\n3. **Urgencias nocturnas:** [PROTOCOLO_CLINICA]\n\nSe considera emergencia:\n- Dolor intenso\n- Trauma/fractura dental\n- Sangrado que no para\n- Infección/inflamación severa",
      "keywords": ["emergencia", "urgencia", "dolor", "fractura"],
      "category": "emergency"
    },
    {
      "question": "¿Cómo me preparo para una extracción de muela?",
      "answer": "Antes de una extracción:\n\n✅ Sí puedes:\n- Comer normal antes (no en ayunas)\n- Tomar tus medicamentos habituales\n- Venir acompañado (recomendado)\n\n❌ Evita:\n- Alcohol 24h antes\n- Fumar el día de la extracción\n- Aspirina 7 días antes (usar acetaminofén)\n\n📋 Trae:\n- Exámenes previos si los tienes\n- Lista de medicamentos que tomas\n\n¿Tienes alguna duda específica?",
      "keywords": ["preparación", "extracción", "muela", "cirugía", "antes"],
      "category": "pre_procedure"
    },
    {
      "question": "¿Qué cuidados debo tener después de una extracción?",
      "answer": "Después de una extracción dental:\n\n🕐 Primeras 24 horas:\n- Morder gasa por 30-60 min\n- NO escupir ni enjuagar\n- Aplicar hielo externo (15 min cada hora)\n- Dieta blanda y fría\n- NO fumar ni tomar alcohol\n\n💊 Medicamentos:\n- Tomar analgésico recetado\n- Antibiótico si fue indicado\n\n⚠️ Llama si tienes:\n- Sangrado abundante después de 2 horas\n- Dolor que no mejora con medicamento\n- Fiebre >38°C\n- Inflamación excesiva día 3+\n\n¿Necesitas agendar tu cita de control?",
      "keywords": ["cuidados", "después", "post", "extracción", "recuperación"],
      "category": "post_procedure"
    }
  ]
}
```

### Formato de Ingesta a Pinecone

Cada FAQ se convierte en un vector:

```javascript
{
  id: "clinic_123_faq_001",
  values: [0.023, -0.019, ...], // 1536 dimensions
  metadata: {
    clinic_id: "clinic_123",
    doc_type: "faq",
    category: "pricing",
    question: "¿Cuánto cuesta una limpieza dental?",
    answer: "El costo de una limpieza dental...",
    keywords: ["precio", "limpieza", "profilaxis"],
    created_at: "2024-01-01T00:00:00Z"
  }
}
```

---

## Interfaz de Usuario

### Internal Chat (Next.js)

**Ruta:** `/Users/nico/Documents/pymes/n8n/web-interface/`

**Stack:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Shadcn/ui
- React Query (server state)
- Zustand (client state)

**Páginas principales:**

```
app/
├── (auth)/
│   ├── login/
│   └── register/
│
├── (dashboard)/
│   ├── chat/              # Main chat interface
│   ├── knowledge/         # Upload/manage docs
│   ├── conversations/     # View client conversations
│   ├── analytics/         # Basic metrics
│   └── settings/          # Clinic settings
│
└── api/
    ├── chat/             # POST to n8n webhook
    ├── upload/           # Upload docs for knowledge base
    └── auth/             # JWT handling
```

**Componente Chat Principal:**

```typescript
// app/(dashboard)/chat/page.tsx
'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { ChatMessage } from '@/components/ChatMessage';
import { ChatInput } from '@/components/ChatInput';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);

  const sendMessage = useMutation({
    mutationFn: async (question: string) => {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ question })
      });
      return res.json();
    },
    onSuccess: (data) => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        suggestions: data.suggestions
      }]);
    }
  });

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
      </div>
      <ChatInput onSend={(text) => {
        setMessages(prev => [...prev, { role: 'user', content: text }]);
        sendMessage.mutate(text);
      }} />
    </div>
  );
}
```

---

## Seguridad y Compliance

### Datos Sensibles

**GDPR / Habeas Data (Colombia):**
- ✅ Almacenar solo data necesaria
- ✅ Obtener consent explícito para WhatsApp marketing
- ✅ Permitir opt-out en cualquier momento
- ✅ Derecho al olvido (delete conversation on request)
- ✅ Encriptar datos en reposo (PostgreSQL encryption)
- ✅ HTTPS en todos los endpoints

**Implementación:**

```sql
-- Consent tracking
CREATE TABLE consent_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_phone VARCHAR(20) NOT NULL,
  consent_type VARCHAR(50), -- marketing, support, etc
  granted BOOLEAN DEFAULT true,
  granted_at TIMESTAMP DEFAULT NOW(),
  revoked_at TIMESTAMP
);

-- Anonymization function (GDPR right to be forgotten)
CREATE FUNCTION anonymize_customer(phone VARCHAR) RETURNS VOID AS $$
BEGIN
  UPDATE conversations
  SET customer_name = 'DELETED_USER',
      customer_phone = 'DELETED'
  WHERE customer_phone = phone;

  UPDATE messages
  SET message_text = '[DELETED]'
  WHERE conversation_id IN (
    SELECT id FROM conversations WHERE customer_phone = phone
  );
END;
$$ LANGUAGE plpgsql;
```

### Rate Limiting

**n8n Webhook Protection:**

```javascript
// Code node before processing
const phone = $json.customer_phone;
const rateLimitKey = `ratelimit:${phone}`;

// Check Redis or in-memory store
const messageCount = await redis.incr(rateLimitKey);
await redis.expire(rateLimitKey, 60); // 1 minute window

if (messageCount > 10) {
  throw new Error('Rate limit exceeded. Max 10 messages per minute.');
}

return $json;
```

### API Key Management

**.env file (NUNCA commitear):**

```bash
# n8n
N8N_ENCRYPTION_KEY=random-strong-key-here
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=strong-password

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# AI
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# WhatsApp
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Vector DB
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1-aws

# JWT
JWT_SECRET=another-random-strong-key
```

---

## Deployment

### MVP Local (Semanas 1-3)

**Setup completo en 30 minutos:**

```bash
# 1. Clone repo
cd /Users/nico/Documents/pymes

# 2. Start n8n
cd n8n
docker-compose up -d

# 3. Access n8n
open http://localhost:5678

# 4. Import workflows
# Upload whatsapp-client-bot.json
# Upload internal-knowledge-chat.json

# 5. Start ngrok
ngrok http 5678
# Copy HTTPS URL: https://abc123.ngrok.io

# 6. Configure Twilio webhook
# In Twilio console:
# Webhook URL: https://abc123.ngrok.io/webhook/whatsapp/clinic_test

# 7. Test WhatsApp sandbox
# Send message to Twilio sandbox number
```

### Producción - Oracle Cloud Free (Semanas 4+)

**Ver N8N_SETUP_GUIDE.md para detalles completos**

Resumen:
1. Create Oracle Cloud account (free tier forever)
2. Spin up ARM VM (Ubuntu 22.04)
3. Install Docker + Docker Compose
4. Clone n8n config
5. Set up PostgreSQL
6. Configure domain/HTTPS (Caddy reverse proxy)
7. Import workflows
8. Configure Twilio production webhooks

**Costo:** $0/month (gratis para siempre)

---

## Monitoreo y Analytics

### Métricas Clave

**Por Clínica:**
```sql
-- Daily conversation volume
SELECT
  DATE(created_at) as date,
  COUNT(DISTINCT conversation_id) as conversations,
  COUNT(*) as messages,
  AVG(response_time_ms) as avg_response_time
FROM messages
WHERE clinic_id = 'clinic_123'
  AND created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at);

-- Intent breakdown
SELECT
  intent,
  COUNT(*) as count,
  ROUND(AVG(response_time_ms)) as avg_time
FROM messages
WHERE clinic_id = 'clinic_123'
  AND direction = 'inbound'
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY intent
ORDER BY count DESC;

-- Escalation rate
SELECT
  COUNT(CASE WHEN status = 'escalated' THEN 1 END)::float / COUNT(*) * 100 as escalation_rate
FROM conversations
WHERE clinic_id = 'clinic_123';
```

**Dashboard en Retool (Fase 2):**
- Gráfico de volumen de mensajes (línea tiempo)
- Distribución de intents (pie chart)
- Tiempo promedio de respuesta (gauge)
- Tasa de escalación (%)
- Top 10 preguntas frecuentes
- Horarios de mayor actividad

### Alertas

**n8n Workflow: error-alerts.json**

```
Trigger: Error in any workflow
  ↓
Send Slack/Email notification
  ↓
Log to error_logs table
  ↓
If critical: Page on-call person
```

---

## Roadmap

### Q1 2026 (Jan-Mar) - MVP + Primeros Clientes

**Enero (Semanas 1-4):**
- ✅ Setup n8n local
- [ ] Build WhatsApp workflow básico
- [ ] Build internal chat básico
- [ ] Create 30 FAQs template (odontología)
- [ ] Test con Twilio sandbox
- [ ] Deploy a Oracle Cloud

**Febrero (Semanas 5-8):**
- [ ] Contactar 200 leads del scraper
- [ ] Agendar 10 demos
- [ ] Cerrar primeros 2-3 clientes
- [ ] Onboarding manual (duplicar workflows)
- [ ] Collect feedback

**Marzo (Semanas 9-12):**
- [ ] Refinar basado en feedback
- [ ] Build Next.js internal chat UI
- [ ] Implementar multi-tenancy (tenant routing)
- [ ] 5-7 clientes totales
- [ ] $500-800 USD MRR

### Q2 2026 (Apr-Jun) - Escalar

**Abril:**
- [ ] Admin dashboard (Retool)
- [ ] Self-service onboarding
- [ ] Appointment scheduling (Google Cal)
- [ ] 10 clientes objetivo

**Mayo:**
- [ ] Payment reminders workflow
- [ ] Review request automation
- [ ] Migrar a Meta WhatsApp API (cost savings)
- [ ] 12-15 clientes

**Junio:**
- [ ] Templates para clínicas estéticas
- [ ] Templates para otros nichos
- [ ] Contratar VA o socio comercial
- [ ] $2,000-3,000 USD MRR

### Q3 2026 (Jul-Sep) - Producto

**Features:**
- [ ] CRM integration (custom o Hubspot)
- [ ] Voice messages support
- [ ] Image recognition (ej: fotos de sonrisa para valoración)
- [ ] A/B testing de prompts
- [ ] Advanced analytics dashboard

**Escala:**
- [ ] 25-30 clientes
- [ ] $4,000-6,000 USD MRR
- [ ] Considerar Series Seed funding

### Q4 2026 (Oct-Dec) - Expansión

- [ ] Expandir a otros países (México, Perú, Ecuador)
- [ ] White-label option para agencias
- [ ] API pública para integraciones
- [ ] 50+ clientes objetivo

---

## Notas para Desarrollo

### Cuando construyas workflows:
1. Siempre usar try-catch en Code nodes
2. Log todo a PostgreSQL (debugging futuro)
3. Test con data real antes de producción
4. Exportar workflows a git después de cada cambio mayor
5. Usar variables de entorno para TODOS los secrets

### Cuando agregues features:
1. Validar con 1-2 clientes primero
2. Documentar en knowledge base
3. Update templates si es feature común
4. Medir impacto en métricas

### Debugging:
1. n8n tiene logs built-in (UI)
2. PostgreSQL query logs
3. Check Twilio logs para delivery issues
4. Pinecone dashboard para vector search issues

---

**Última actualización:** 2026-01-02
**Versión:** 1.0
**Autor:** Nico
**Contacto:** [Tu email/WhatsApp]
