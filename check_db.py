#!/usr/bin/env python
from app import app, db
from sqlalchemy import inspect, text
from models import User, Exercise, Flashcard, Achievement, UserAchievement, UserExercise, UserExample, ProgressHistory, FlashcardSession

def check_database():
    print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
    print("=" * 50)
    
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Tablas en la base de datos ({len(tables)}):")
        for table in sorted(tables):
            # Usar text() para consultas SQL literales
            result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"   ✅ {table}: {count} registros")
        
        print("\n🎴 FLASHCARDS:")
        try:
            total = Flashcard.query.count()
            print(f"   Total: {total}")
            
            if total > 0:
                from sqlalchemy import func
                
                # Por categoría
                categories = db.session.query(
                    Flashcard.category, 
                    func.count(Flashcard.id)
                ).group_by(Flashcard.category).all()
                
                print("\n   Por categoría:")
                for cat, count in categories:
                    print(f"      {cat}: {count}")
                
                # Por dificultad
                difficulties = db.session.query(
                    Flashcard.difficulty, 
                    func.count(Flashcard.id)
                ).group_by(Flashcard.difficulty).all()
                
                print("\n   Por dificultad:")
                for diff, count in difficulties:
                    print(f"      Nivel {diff}: {count}")
                
                # Primeros 5 flashcards como ejemplo
                print("\n   📝 Ejemplos:")
                for i, card in enumerate(Flashcard.query.limit(5).all()):
                    print(f"      {i+1}. {card.question[:60]}...")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n👤 USUARIO TEST:")
        try:
            user = User.query.filter_by(username='test').first()
            if user:
                print(f"   ✅ Usuario test existe (ID: {user.id})")
                # Verificar flashcards asignadas al usuario
                user_cards = Flashcard.query.filter_by(user_id=user.id).count()
                print(f"   📚 Flashcards asignadas: {user_cards}")
            else:
                print("   ❌ Usuario test NO existe")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == '__main__':
    check_database()
