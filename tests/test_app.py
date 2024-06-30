import unittest
import sys
import os
import json
from dotenv import load_dotenv

# Asegúrate de que el directorio de la aplicación esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Carga las variables de entorno desde .env (opcional, solo para desarrollo local)
load_dotenv()

# Importa la aplicación y cualquier configuración necesaria
from app import app, db, Vote

class TestVotingApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar SQLite para pruebas locales
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        with app.app_context():
            db.create_all()
            # Añadir datos de prueba
            option1 = Vote(option='option1')
            option2 = Vote(option='option2')
            db.session.add_all([option1, option2])
            db.session.commit()

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.data.decode('utf-8'), 'Welcome to the Voting App!')

    def test_vote_valid_option(self):
        initial_vote_count = Vote.query.filter_by(option='option1').first().count
        data = json.dumps({'option': 'option1'})
        response = self.app.post('/vote', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.query.filter_by(option='option1').first().count, initial_vote_count + 1)

    def test_vote_invalid_option(self):
        data = json.dumps({'option': 'invalid_option'})
        response = self.app.post('/vote', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid option')

    def test_results(self):
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        results = response.json
        self.assertIn('option1', results)
        self.assertIn('option2', results)

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
