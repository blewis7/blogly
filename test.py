from unittest import TestCase
from model import db, connect_db, User, Post
from app import app

class FlaskTests(TestCase):

    def test_setup(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_home(self):
        response = self.client.get('/users')
        self.assertsIn(b'<form action="/users/new">', response.data)
        self.assertsIn(b'>Add New User<', response.data)

    def test_new_user(self):
        response = self.client.get('/users/new')
        self.assertsIn(b'<h1>Create New User</h1>', response.data)
        self.assertsIn(b"<input type='text' name='img' placeholder='Enter Image URL'>", response.data)

    def test_invalid_user(self):
        response = self.client.get('/posts/1111')
        self.assertsIn(b'Not Found', response.data)

    def test_invalid_post(self):
        response = self.client.get('/users/121212')
        self.assertsIn(b'Not Found', response.data)
    
    def test_invalid_page(self):
        response = self.client.get('/posts')
        self.assertsIn(b'Not Found', response.data)

