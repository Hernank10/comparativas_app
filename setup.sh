#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     CONFIGURACIÓN DE PRÁCTICA DE COMPARATIVAS             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si ya existe el entorno virtual
if [ -d "venv" ]; then
    echo "📦 Eliminando entorno virtual existente..."
    rm -rf venv
    echo "✅ Entorno virtual eliminado"
fi

# Crear entorno virtual
echo "📦 Creando nuevo entorno virtual..."
python3 -m venv venv
echo "✅ Entorno virtual creado"

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate
echo "✅ Entorno virtual activado"

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip
echo "✅ Pip actualizado"

# Instalar dependencias con versiones específicas
echo "📦 Instalando dependencias (esto puede tomar unos minutos)..."
pip install Flask==2.2.5
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Login==0.6.2
pip install Flask-Bcrypt==1.0.1
pip install Flask-Migrate==4.0.4
pip install python-dotenv==1.0.0
pip install Werkzeug==2.2.3

echo "✅ Dependencias instaladas"

# Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
mkdir -p static/data
mkdir -p instance
echo "✅ Directorios creados"

# Verificar que los archivos necesarios existen
echo "🔍 Verificando archivos necesarios..."

if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    exit 1
else
    echo "✅ app.py encontrado"
fi

if [ ! -f "models.py" ]; then
    echo "❌ Error: No se encuentra models.py"
    exit 1
else
    echo "✅ models.py encontrado"
fi

if [ ! -f "static/data/exercises.json" ]; then
    echo "⚠️  Advertencia: No se encuentra exercises.json"
else
    echo "✅ exercises.json encontrado"
fi

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de datos creada correctamente')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Base de datos inicializada"
else
    echo "❌ Error al inicializar la base de datos"
    exit 1
fi

# Verificar instalación
echo ""
echo "🔧 Verificando instalación..."
python -c "
import flask
import werkzeug
import sqlalchemy
print(f'Flask: {flask.__version__}')
print(f'Werkzeug: {werkzeug.__version__}')
print(f'SQLAlchemy: {sqlalchemy.__version__}')
print('✅ Todas las importaciones funcionan correctamente')
" 2>/dev/null

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     ✅ CONFIGURACIÓN COMPLETADA                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Activar el entorno virtual:  source venv/bin/activate"
echo "   2. Ejecutar la aplicación:      python app.py"
echo "   3. Abrir en el navegador:        http://localhost:5000"
echo ""
echo "   Usuario de prueba (crear manualmente):"
echo "   python -c \"from app import app, db; from models import User; from flask_bcrypt import Bcrypt; bcrypt = Bcrypt(app); with app.app_context(): db.session.add(User(username='test', email='test@test.com', password_hash=bcrypt.generate_password_hash('test123').decode('utf-8'))); db.session.commit(); print('✅ Usuario test creado')\""
echo ""
