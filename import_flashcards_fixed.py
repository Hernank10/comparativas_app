#!/usr/bin/env python
import json
from app import app, db
from models import User, Flashcard, Exercise
from datetime import datetime

def import_flashcards_fixed():
    print("🎴 IMPORTADOR DE FLASHCARDS (VERSIÓN CORREGIDA)")
    print("=" * 50)
    
    with app.app_context():
        # Cargar flashcards del JSON
        with open('static/data/flashcards_complete.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            flashcards_data = data['flashcards']
        
        print(f"📚 Cargados {len(flashcards_data)} flashcards del JSON")
        
        # Obtener el usuario test
        user = User.query.filter_by(username='test').first()
        if not user:
            print("❌ Usuario test no encontrado. Creándolo...")
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(app)
            user = User(
                username='test',
                email='test@test.com',
                password_hash=bcrypt.generate_password_hash('test123').decode('utf-8')
            )
            db.session.add(user)
            db.session.commit()
            print("✅ Usuario test creado")
        
        # Eliminar flashcards existentes del usuario
        deleted = Flashcard.query.filter_by(user_id=user.id).delete()
        print(f"🗑️  Eliminadas {deleted} flashcards existentes")
        
        # Crear ejercicios si no existen
        exercise_count = 0
        for fc in flashcards_data:
            exercise = Exercise.query.filter_by(question=fc['question'][:100]).first()
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
                exercise_count += 1
        
        if exercise_count > 0:
            db.session.commit()
            print(f"✅ Creados {exercise_count} nuevos ejercicios")
        
        # Crear flashcards para el usuario
        flashcard_count = 0
        for fc in flashcards_data:
            # Buscar el exercise_id
            exercise = Exercise.query.filter_by(question=fc['question'][:100]).first()
            exercise_id = exercise.id if exercise else fc['id']
            
            card = Flashcard(
                user_id=user.id,
                exercise_id=exercise_id,
                question=fc['question'],
                answer=fc['answer'],
                category=fc['category'],
                difficulty=fc['difficulty'],
                options=json.dumps(fc.get('options', [])),
                next_review=datetime.utcnow(),
                is_active=True
            )
            db.session.add(card)
            flashcard_count += 1
            
            # Commit cada 20 flashcards para no sobrecargar
            if flashcard_count % 20 == 0:
                db.session.commit()
                print(f"   ... {flashcard_count} flashcards creadas")
        
        db.session.commit()
        print(f"✅ Creadas {flashcard_count} flashcards para usuario {user.username}")
        
        # Verificación final
        final_count = Flashcard.query.filter_by(user_id=user.id).count()
        print(f"\n📊 VERIFICACIÓN FINAL:")
        print(f"   Flashcards en BD: {final_count}")
        
        if final_count > 0:
            # Mostrar algunas estadísticas
            from sqlalchemy import func
            categories = db.session.query(
                Flashcard.category, 
                func.count(Flashcard.id)
            ).filter(Flashcard.user_id == user.id).group_by(Flashcard.category).all()
            
            print("\n   Por categoría:")
            for cat, count in categories:
                print(f"      {cat}: {count}")
        
        return final_count

if __name__ == '__main__':
    count = import_flashcards_fixed()
    if count > 0:
        print(f"\n✅ IMPORTACIÓN EXITOSA: {count} flashcards listas para usar")
    else:
        print("\n❌ ERROR: No se crearon flashcards")
