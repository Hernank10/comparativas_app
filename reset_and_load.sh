#!/bin/bash

echo "🎴 Resetando y recargando sistema de flashcards..."
echo "================================================"

# Activar entorno virtual
source venv/bin/activate

# Limpiar base de datos (opcional - comentar si no se quiere)
echo "🗑️  Limpiando flashcards existentes..."
python -c "
from app import app, db
from models import Flashcard
with app.app_context():
    Flashcard.query.delete()
    db.session.commit()
    print('✅ Flashcards eliminadas')
"

# Importar nuevos flashcards
echo "📦 Importando nuevos flashcards..."
python import_flashcards.py

echo ""
echo "✅ Proceso completado!"
echo "Ahora puedes ejecutar 'python app.py' y probar las flashcards"
