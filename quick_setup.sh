#!/bin/bash

echo "🚀 Configuración rápida de Comparativas App"
echo "=========================================="

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install Flask==2.2.5 Flask-SQLAlchemy==3.0.5 Flask-Login==0.6.2
pip install Flask-Bcrypt==1.0.1 Flask-Migrate==4.0.4 python-dotenv==1.0.0
pip install Werkzeug==2.2.3

# Recrear base de datos
echo "🗄️  Recreando base de datos..."
rm -f instance/comparativas.db
python -c "from app import app, db; with app.app_context(): db.create_all()"

# Importar flashcards
echo "🎴 Importando flashcards..."
python import_flashcards_fixed.py

# Crear usuario test
echo "👤 Creando usuario test..."
python -c "
from app import app, db
from models import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
with app.app_context():
    User.query.filter_by(username='test').delete()
    user = User(username='test', email='test@test.com', 
                password_hash=bcrypt.generate_password_hash('test123').decode('utf-8'))
    db.session.add(user)
    db.session.commit()
"

echo ""
echo "✅ Configuración completada!"
echo "Para ejecutar la app: python app.py"
echo "Usuario: test | Contraseña: test123"
