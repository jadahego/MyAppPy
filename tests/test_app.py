import unittest
import sys
import os
import json

# Asegúrate de que el directorio de la aplicación esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Importa la aplicación y cualquier configuración necesaria
from app import app, votes

class TestVotingApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.data.decode('utf-8'), 'Welcome to the Voting App!')

    def test_vote_valid_option(self):
        initial_vote_count = votes['option1']
        data = json.dumps({'option': 'option1'})
        response = self.app.post('/vote', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(votes['option1'], initial_vote_count + 1)

    def test_vote_invalid_option(self):
        data = json.dumps({'option': 'invalid_option'})
        response = self.app.post('/vote', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid option')

    def test_results(self):
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, votes)

if __name__ == '__main__':
    unittest.main()
