-- Multi-Tenant Chatbot Database Schema
-- This creates tables to store multiple client configurations

-- Table: clients
-- Stores information about each client (clinic/business)
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name VARCHAR(255) NOT NULL,
    whatsapp_number VARCHAR(20) UNIQUE NOT NULL, -- Their business WhatsApp number
    industry VARCHAR(100), -- e.g., 'dental_clinic', 'beauty_salon', 'restaurant'

    -- Business details
    services JSONB, -- {"limpieza": 80000, "blanqueamiento": 150000}
    business_hours TEXT,
    location TEXT,
    contact_phone VARCHAR(20),
    website VARCHAR(255),

    -- AI Configuration
    system_prompt TEXT NOT NULL, -- Custom instructions for this client's chatbot
    ai_model VARCHAR(50) DEFAULT 'llama3.2:latest',
    temperature DECIMAL(2,1) DEFAULT 0.7,

    -- Subscription & Status
    plan VARCHAR(50) DEFAULT 'basic', -- 'basic', 'pro', 'enterprise'
    active BOOLEAN DEFAULT true,
    monthly_fee INTEGER, -- in COP (e.g., 400000)

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Additional config (future features)
    config JSONB DEFAULT '{}'::jsonb
);

-- Table: conversations
-- Tracks all conversations for analytics and debugging
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    customer_phone VARCHAR(20) NOT NULL, -- End customer's WhatsApp
    message_text TEXT NOT NULL,
    ai_response TEXT,

    -- Message direction
    direction VARCHAR(10) CHECK (direction IN ('inbound', 'outbound')),

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    response_time_ms INTEGER, -- How long AI took to respond

    -- For analytics
    conversation_session_id UUID, -- Group messages in same conversation

    CONSTRAINT fk_client
        FOREIGN KEY (client_id)
        REFERENCES clients(id)
        ON DELETE CASCADE
);

-- Table: client_faqs (Optional - for advanced knowledge base)
CREATE TABLE IF NOT EXISTS client_faqs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100), -- 'pricing', 'hours', 'services', 'policies'
    keywords TEXT[], -- Array of keywords for better matching

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    times_used INTEGER DEFAULT 0, -- Track which FAQs are most useful

    CONSTRAINT fk_client_faq
        FOREIGN KEY (client_id)
        REFERENCES clients(id)
        ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_clients_whatsapp ON clients(whatsapp_number);
CREATE INDEX IF NOT EXISTS idx_conversations_client ON conversations(client_id);
CREATE INDEX IF NOT EXISTS idx_conversations_customer ON conversations(customer_phone);
CREATE INDEX IF NOT EXISTS idx_conversations_created ON conversations(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_faqs_client ON client_faqs(client_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at
CREATE TRIGGER update_clients_updated_at
    BEFORE UPDATE ON clients
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_faqs_updated_at
    BEFORE UPDATE ON client_faqs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample test clients
INSERT INTO clients (business_name, whatsapp_number, industry, services, business_hours, location, system_prompt, monthly_fee)
VALUES
(
    'Clínica Dental Medellín',
    '+573001111111',
    'dental_clinic',
    '{
        "limpieza_dental": 80000,
        "blanqueamiento": 150000,
        "implantes": 1200000,
        "ortodoncia": 3500000,
        "consulta_gratis": 0
    }'::jsonb,
    'Lunes a Viernes: 8:00 AM - 6:00 PM, Sábados: 9:00 AM - 2:00 PM',
    'Calle 50 #45-30, Medellín, Colombia',
    'Eres un asistente virtual amigable y profesional para Clínica Dental Medellín, una clínica odontológica en Medellín, Colombia.

SERVICIOS Y PRECIOS:
- Limpieza dental (profilaxis): $80,000 COP
- Blanqueamiento dental: $150,000 COP
- Implantes dentales: Desde $1,200,000 COP
- Ortodoncia (brackets): $3,500,000 COP (plan completo)
- Consulta de valoración: GRATIS

HORARIOS DE ATENCIÓN:
Lunes a Viernes: 8:00 AM - 6:00 PM
Sábados: 9:00 AM - 2:00 PM
Domingos: Cerrado

UBICACIÓN:
Calle 50 #45-30, Medellín, Colombia
Teléfono: +57 300 111 1111

POLÍTICA DE CITAS:
- Reservar con 24 horas de anticipación
- Cancelaciones con 12 horas de aviso
- Primera consulta es gratis

INSTRUCCIONES:
Cuando un cliente te escriba:
1. Salúdalo cordialmente
2. Responde de forma clara y breve (máximo 3-4 líneas)
3. Si pregunta por citas, explícale que puede agendar llamando o por WhatsApp
4. Si pregunta algo que no sabes, ofrece transferirlo con un odontólogo
5. Siempre responde en español colombiano, de forma profesional pero amigable',
    400000
),
(
    'Centro Estético Bogotá',
    '+573002222222',
    'beauty_salon',
    '{
        "limpieza_facial": 120000,
        "masaje_relajante": 90000,
        "botox": 800000,
        "rellenos": 600000,
        "depilacion_laser": 250000
    }'::jsonb,
    'Lunes a Sábado: 9:00 AM - 7:00 PM',
    'Carrera 15 #85-40, Bogotá, Colombia',
    'Eres un asistente virtual para Centro Estético Bogotá, un centro de belleza y estética en Bogotá, Colombia.

SERVICIOS Y PRECIOS:
- Limpieza facial profunda: $120,000 COP
- Masaje relajante: $90,000 COP
- Aplicación de Botox: $800,000 COP
- Rellenos faciales: $600,000 COP
- Depilación láser: $250,000 COP

HORARIOS:
Lunes a Sábado: 9:00 AM - 7:00 PM
Domingos: Cerrado

UBICACIÓN:
Carrera 15 #85-40, Bogotá, Colombia
Teléfono: +57 300 222 2222

POLÍTICA DE CITAS:
- Agendar con 48 horas de anticipación para tratamientos especializados
- Primera consulta de valoración: $50,000 COP
- Cancelaciones con 24 horas de aviso

Responde de forma amable, profesional y breve. Si preguntan por disponibilidad, pídeles su preferencia de día/hora.',
    450000
),
(
    'Restaurante La Parrilla Cali',
    '+573003333333',
    'restaurant',
    '{
        "bandeja_paisa": 28000,
        "sancocho": 22000,
        "ajiaco": 24000,
        "carne_asada": 35000,
        "pescado_frito": 32000
    }'::jsonb,
    'Todos los días: 12:00 PM - 10:00 PM',
    'Avenida 6N #18-50, Cali, Colombia',
    'Eres un asistente virtual amigable para Restaurante La Parrilla, un restaurante de comida típica colombiana en Cali.

PLATOS Y PRECIOS:
- Bandeja Paisa: $28,000 COP
- Sancocho: $22,000 COP
- Ajiaco: $24,000 COP
- Carne asada: $35,000 COP
- Pescado frito: $32,000 COP

HORARIO:
Todos los días: 12:00 PM - 10:00 PM

UBICACIÓN:
Avenida 6N #18-50, Cali, Colombia
Teléfono: +57 300 333 3333

SERVICIOS:
- Domicilios a toda Cali
- Reservas para grupos grandes
- Servicio de catering para eventos

Responde de forma amigable y entusiasta. Si preguntan por delivery, explica que hacemos domicilios. Si preguntan por reservas, pide nombre, fecha, hora y número de personas.',
    350000
)
ON CONFLICT (whatsapp_number) DO NOTHING;

-- Display created clients
SELECT business_name, whatsapp_number, industry, monthly_fee
FROM clients
ORDER BY created_at DESC;
