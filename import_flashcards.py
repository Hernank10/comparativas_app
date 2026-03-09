#!/usr/bin/env python
import json
from app import app, db
from models import User, Flashcard, Exercise
from datetime import datetime

def import_flashcards():
    with app.app_context():
        # Cargar los flashcards del JSON
        with open('static/data/flashcards_complete.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            flashcards_data = data['flashcards']
        
        print(f"📚 Cargando {len(flashcards_data)} flashcards...")
        
        # Para cada usuario, crear sus flashcards
        users = User.query.all()
        for user in users:
            print(f"👤 Procesando usuario: {user.username}")
            
            # Eliminar flashcards existentes del usuario
            Flashcard.query.filter_by(user_id=user.id).delete()
            
            # Crear nuevas flashcards
            for fc in flashcards_data:
                # Buscar si existe un ejercicio similar para mantener consistencia
                exercise = Exercise.query.filter_by(
                    question=fc['question'][:100]  # Buscar por inicio de la pregunta
                ).first()
                
                card = Flashcard(
                    user_id=user.id,
                    exercise_id=exercise.id if exercise else fc['id'],
                    question=fc['question'],
                    answer=fc['answer'],
                    category=fc['category'],
                    difficulty=fc['difficulty'],
                    next_review=datetime.utcnow(),  # Listas para revisar ahora
                    is_active=True
                )
                db.session.add(card)
            
            db.session.commit()
            print(f"  ✅ {len(flashcards_data)} flashcards creadas")
        
        print("\n✅ Importación completada!")

def create_exercises_from_flashcards():
    """Opcional: Crear ejercicios en la tabla Exercise si no existen"""
    with app.app_context():
        with open('static/data/flashcards_complete.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            flashcards_data = data['flashcards']
        
        for fc in flashcards_data:
            exercise = Exercise.query.filter_by(
                question=fc['question'][:100]
            ).first()
            
            if not exercise:
                exercise = Exercise(
                    type=fc.get('type', 'flashcard'),
                    question=fc['question'],
                    answer=fc['answer'],
                    options=json.dumps(fc.get('options', [])),
                    difficulty=fc['difficulty'],
                    category=fc['category'],
                    explanation=fc.get('explanation', '')
                )
                db.session.add(exercise)
        
        db.session.commit()
        print(f"✅ {len(flashcards_data)} ejercicios creados/verificados")

if __name__ == '__main__':
    print("🎴 Importador de Flashcards")
    print("=" * 40)
    
    # Primero crear ejercicios
    create_exercises_from_flashcards()
    
    # Luego importar flashcards para usuarios
    import_flashcards()
