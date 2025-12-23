#!/bin/bash

echo "================================================"
echo "🚀 Configuración del Scraper de Google Maps"
echo "================================================"

# Verificar Python
echo ""
echo "🔍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
else
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Crear entorno virtual
echo ""
echo "📦 Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo ""
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo ""
echo "📥 Instalando dependencias..."
pip3 install -q --upgrade pip
pip3 install -q -r requirements.txt

# Instalar navegadores de Playwright
echo ""
echo "🌐 Instalando navegadores de Playwright..."
python3 -m playwright install chromium

# Crear directorio para resultados
echo ""
echo "📁 Creando directorio para resultados..."
mkdir -p resultados

echo ""
echo "================================================"
echo "✅ INSTALACIÓN COMPLETADA"
echo "================================================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Activa el entorno virtual:"
echo "   source venv/bin/activate"
echo ""
echo "2. Ejecuta el scraper:"
echo "   python3 buscar_clinicas.py"
echo ""
echo "   O para múltiples ciudades:"
echo "   python3 buscar_por_ciudades.py"
echo ""
echo "3. Revisa los archivos Excel generados"
echo ""
echo "================================================"
