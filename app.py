import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from models import db, User, Exercise, Achievement, UserAchievement, UserExercise, UserExample, ProgressHistory
from datetime import datetime, timedelta
import json
import random
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comparativas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def load_exercises():
    exercises_file = 'static/data/exercises.json'
    if os.path.exists(exercises_file):
        with open(exercises_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['exercises']
    return []

EXERCISES = load_exercises()

def set_language(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'language' not in session:
            session['language'] = 'es'
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@set_language
def index():
    return render_template('index.html')

@app.route('/teoria')
@set_language
def teoria():
    return render_template('teoria.html')

@app.route('/ejercicios')
@login_required
@set_language
def ejercicios():
    return render_template('ejercicios.html')

@app.route('/progreso')
@login_required
@set_language
def progreso():
    return render_template('progreso.html')

@app.route('/logros')
@login_required
@set_language
def logros():
    return render_template('logros.html')

@app.route('/ejemplos')
@login_required
@set_language
def ejemplos():
    return render_template('ejemplos.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/ejercicios/<tipo>')
@login_required
def get_ejercicios(tipo):
    ejercicios_tipo = [e for e in EXERCISES if e['type'] == tipo]
    
    if not ejercicios_tipo:
        return jsonify({'error': 'No exercises found'}), 404
    
    ejercicio = random.choice(ejercicios_tipo)
    return jsonify({
        'id': ejercicio['id'],
        'question': ejercicio['question'],
        'type': ejercicio['type'],
        'options': ejercicio['options'],
        'difficulty': ejercicio['difficulty'],
        'category': ejercicio['category'],
        'hint': ejercicio.get('hint', '')
    })

@app.route('/api/verificar', methods=['POST'])
@login_required
def verificar_respuesta():
    data = request.json
    ejercicio_id = data.get('exercise_id')
    respuesta = data.get('answer')
    tiempo = data.get('time_spent', 0)
    
    ejercicio = next((e for e in EXERCISES if e['id'] == ejercicio_id), None)
    
    if not ejercicio:
        return jsonify({'error': 'Exercise not found'}), 404
    
    es_correcto = respuesta.lower().strip() == ejercicio['answer'].lower().strip()
    
    user_exercise = UserExercise(
        user_id=current_user.id,
        exercise_id=ejercicio_id,
        correct=es_correcto,
        time_spent=tiempo
    )
    db.session.add(user_exercise)
    
    current_user.total_attempts += 1
    if es_correcto:
        current_user.correct_answers += 1
        current_user.current_streak += 1
        if current_user.current_streak > current_user.best_streak:
            current_user.best_streak = current_user.current_streak
    else:
        current_user.current_streak = 0
    
    if current_user.total_attempts > 0:
        current_user.mastery_level = (current_user.correct_answers / current_user.total_attempts) * 100
    
    db.session.commit()
    
    return jsonify({
        'correct': es_correcto,
        'correct_answer': ejercicio['answer'],
        'explanation': ejercicio.get('explanation', ''),
        'hint': ejercicio.get('hint', '') if not es_correcto else None,
        'streak': current_user.current_streak,
        'mastery': current_user.mastery_level
    })

@app.route('/api/progreso')
@login_required
def get_progreso():
    fecha_inicio = datetime.now().date() - timedelta(days=7)
    progreso_semanal = ProgressHistory.query.filter(
        ProgressHistory.user_id == current_user.id,
        ProgressHistory.date >= fecha_inicio
    ).order_by(ProgressHistory.date).all()
    
    ejercicios_por_tipo = db.session.query(
        UserExercise, Exercise
    ).join(Exercise).filter(
        UserExercise.user_id == current_user.id
    ).all()
    
    stats_por_tipo = {}
    for ue, ex in ejercicios_por_tipo:
        if ex.type not in stats_por_tipo:
            stats_por_tipo[ex.type] = {'correctas': 0, 'total': 0}
        stats_por_tipo[ex.type]['total'] += 1
        if ue.correct:
            stats_por_tipo[ex.type]['correctas'] += 1
    
    return jsonify({
        'stats': {
            'correctas': current_user.correct_answers,
            'totales': current_user.total_attempts,
            'racha': current_user.current_streak,
            'mejor_racha': current_user.best_streak,
            'maestria': current_user.mastery_level
        },
        'weekly': [{
            'date': p.date.strftime('%Y-%m-%d'),
            'completed': p.exercises_completed,
            'correct': p.correct_answers
        } for p in progreso_semanal],
        'by_type': stats_por_tipo
    })

@app.route('/api/idioma', methods=['POST'])
def cambiar_idioma():
    data = request.json
    session['language'] = data.get('language', 'es')
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
