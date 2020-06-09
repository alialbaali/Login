import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from db import setup_db
from models import User


class AppTest(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "users_test"
        self.database_path = f"postgresql://postgres:135792468@localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_user = {
            'name': 'NAME',
            'username': 'USERNAME',
            'password': 'PASSWORD'
        }
        self.invalid_user = {
            'name': 'invalid',
            'username': 'invalid',
            'password': 'invalid'
        }

        self.search_term = {
            'search_term': 'USERNAME'
        }
        self.invalid_search_term = {
            'search_term': 'invalid'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_user(self):
        res = self.client().post('/users/create', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(len(data['token']))

    def test_409_create_user_with_invalid_username(self):
        res = self.client().post('/users/create', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 409)
        self.assertEqual(data['message'], 'conflict')

    def test_login_user(self):
        res = self.client().post('/users/login', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(len(data['token']))

    def test_401_login_user_with_invalid_credentials(self):
        res = self.client().post('/users/login', json=self.invalid_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_user(self):
        res = self.client().delete('/users/1')
        data = json.loads(res.data)

        user = User.query.filter(User.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertEqual(user, None)

    def test_404_delete_not_existed_user(self):
        res = self.client().delete('/users/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_search_users(self):
        res = self.client().post('/users/search', data=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_users'])
        self.assertTrue(len(data['users']))

    def test_404_search_questions_with_invalid_search_term(self):
        res = self.client().post('/users/search', data=self.invalid_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_user(self):
        res = self.client().patch('/users/1', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], '1')

    def test_404_update_not_existed_user(self):
        res = self.client().patch('/users/1', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
