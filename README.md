# 📚 Práctica de Comparativas en Español

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.2.5-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Hernank10/comparativas_app)](https://github.com/Hernank10/comparativas_app/stargazers)

Aplicación educativa interactiva para practicar **estructuras comparativas en español** con 100 flashcards y sistema de repetición espaciada. Ideal para estudiantes de español como lengua extranjera y hablantes nativos que quieran perfeccionar su gramática.

## ✨ Características Principales

| Característica | Descripción |
|----------------|-------------|
| 🎴 **100 Flashcards** | Ejercicios interactivos de diferentes tipos |
| 🔄 **Repetición Espaciada** | Algoritmo SM-2 para optimizar el aprendizaje |
| 📊 **Estadísticas** | Seguimiento de progreso en tiempo real |
| 🏆 **Logros** | Sistema de gamificación para motivar |
| 📝 **Ejercicios Variados** | Corrección, completación, selección múltiple |
| 👤 **Perfil Personal** | Guarda tu progreso y ejemplos |

## 🎯 Categorías Cubiertas

- ✅ Comparaciones de igualdad (`tan...como`, `tanto...como`)
- ✅ Comparaciones de superioridad (`más...que`)
- ✅ Comparaciones de inferioridad (`menos...que`)
- ✅ Estructuras correlativas (`cuanto más...más`)
- ✅ Comparativos irregulares (`mejor`, `peor`, `mayor`, `menor`)
- ✅ Superlativos (`el más...de`, `el mejor...de`)
- ✅ Comparaciones con relativas (`más...de lo que`)
- ✅ Y muchas más...

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask 2.2.5, SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Frontend:** Bootstrap 5, Chart.js, JavaScript
- **Base de Datos:** SQLite
- **Algoritmo de Estudio:** SM-2 (Spaced Repetition)

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar)

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)

```bash
# Clonar el repositorio
git clone https://github.com/Hernank10/comparativas_app.git
cd comparativas_app

# Dar permisos y ejecutar instalación
chmod +x setup.sh
./setup.sh

# Activar entorno virtual y ejecutar
source venv/bin/activate
python app.py

# 1. Clonar el repositorio
git clone https://github.com/Hernank10/comparativas_app.git
cd comparativas_app

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar base de datos
python -c "from app import app, db; with app.app_context(): db.create_all()"

# 5. Importar flashcards
python import_flashcards_fixed.py

# 6. Ejecutar la aplicación
python app.py

🎮 Cómo Usar la Aplicación
Accede a la aplicación: http://localhost:5000

Inicia sesión con el usuario de prueba:

Usuario: test

Contraseña: test123

Navega por las pestañas:

📖 Teoría: Aprende los conceptos

🎴 Flashcards: Practica con repetición espaciada

📊 Progreso: Revisa tus estadísticas

🏆 Logros: Desbloquea metas

📝 Mis Ejemplos: Crea tus propios ejemplos

comparativas_app/
├── 📂 templates/           # Plantillas HTML
│   ├── base.html          # Plantilla base
│   ├── flashcards.html    # Sistema de flashcards
│   ├── ejercicios.html    # Ejercicios tradicionales
│   └── ...
├── 📂 static/              # Archivos estáticos
│   ├── 📂 css/            # Estilos
│   ├── 📂 js/             # JavaScript
│   └── 📂 data/           # JSON con flashcards
│       ├── exercises.json
│       └── flashcards_complete.json
├── 📝 app.py              # Aplicación principal
├── 📝 models.py           # Modelos de base de datos
├── 📝 requirements.txt    # Dependencias
├── 📝 import_flashcards.py # Importador de flashcards
└── 📝 check_db.py         # Script de diagnóstico
📊 Estadísticas de los Flashcards
Categoría	Cantidad	Dificultad
Igualdad	23	★★★
Relativas	15	★★★
Correlativas	8	★★★
Superlativos	7	★★☆
Irregulares	7	★★☆
Redundancia	6	★☆☆
Elipsis	4	★★☆
Inferioridad	4	★★☆
Intensificadores	4	★★☆
Concordancia	3	★☆☆
Pronombres	3	★☆☆
Y más...	16	Variada
🧪 Scripts Útiles
bash
# Verificar la base de datos
python check_db.py

# Reimportar flashcards (si es necesario)
python import_flashcards_fixed.py

# Diagnóstico rápido
python quick_check.py
🤝 Cómo Contribuir
Fork el repositorio

Crea una rama (git checkout -b feature/NuevaCaracteristica)

Commit tus cambios (git commit -m 'Añadir nueva característica')

Push a la rama (git push origin feature/NuevaCaracteristica)

Abre un Pull Request

📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

📧 Contacto
Hernank10 - GitHub

🙏 Agradecimientos
A todos los que contribuyeron con ideas y sugerencias

A la comunidad de Flask por sus excelentes herramientas

A los estudiantes que probaron la aplicación

⭐ ¿Te gusta el proyecto? ¡Dale una estrella en GitHub! ⭐


