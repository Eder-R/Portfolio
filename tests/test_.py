import os
import tempfile
import unittest
from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from app import app, db

class TestApp(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_listar_livros(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_cadastro_livros(self):
        response = self.client.get('/cadastro_livros')
        self.assert200(response)

    def test_add_book(self):
        response = self.client.post('/add_book', data={'book-title': 'Test Book', 'autor': 'Test Autor', 'genero': 'Test Genre'})
        expected_location = '/cadastro_livros'
        self.assertTrue(response.headers['Location'].endswith(expected_location), f"Expected redirect to {expected_location}, got {response.headers['Location']}")


if __name__ == '__main__':
    unittest.main()
