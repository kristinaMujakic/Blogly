from unittest import TestCase
from app import app
from flask import session
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()


class UserTestCase(TestCase):

    def setUp(self):
        '''Testing views for User'''

        with app.app_context():
            User.query.delete()

            user = User(first_name='TestUserFirst', last_name='TestUserLast')

            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        '''Clean up'''

        with app.app_context():
            db.session.rollback()

    def test_users_index(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TestUserFirst', html)

    def test_show_user(self):
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>TestUserFirst TestUserLast</h1>', html)

    def test_user_form(self):
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Create new user</h1>', html)

    def test_new_user(self):
        with app.test_client() as client:
            user = {'first_name': 'TestUserFirst2', 'last_name': 'TestUserLast2',
                    'image_url': 'https://cdn-icons-png.flaticon.com/512/149/149071.png'}
            response = client.post(
                "/users/new", data=user, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TestUserFirst TestUserLast', html)
