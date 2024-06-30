import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Configurar el logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configurar la conexión a la base de datos MySQL en RDS o localmente
if 'SQLALCHEMY_DATABASE_URI' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'  # Para pruebas locales con SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la instancia de SQLAlchemy
db = SQLAlchemy(app)

# Modelo de datos para los votos
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(50), nullable=False, unique=True)
    count = db.Column(db.Integer, default=0)

    def __init__(self, option):
        self.option = option
        self.count = 0

# Crear todas las tablas y añadir opciones iniciales si no existen
with app.app_context():
    db.create_all()
    if not Vote.query.filter_by(option='option1').first():
        db.session.add(Vote(option='option1'))
    if not Vote.query.filter_by(option='option2').first():
        db.session.add(Vote(option='option2'))
    db.session.commit()

@app.route('/')
def home():
    return "Welcome to the Voting App!"

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    option = data.get('option')
    
    if not option:
        return jsonify({"message": "No option provided"}), 400

    # Buscar la opción en la base de datos o crear una nueva si no existe
    vote = Vote.query.filter_by(option=option).first()
    if vote:
        vote.count += 1
    else:
        new_vote = Vote(option=option)
        new_vote.count = 1
        db.session.add(new_vote)

    db.session.commit()
    return jsonify({"message": "Vote counted!"}), 200

@app.route('/results', methods=['GET'])
def results():
    votes = Vote.query.all()
    results = {vote.option: vote.count for vote in votes}
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
