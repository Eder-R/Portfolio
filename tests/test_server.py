import os
import tempfile
import pytest
from flask import Flask

from app import app, db, Livro, Pessoa  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

def test_listar_livros(client):
    with app.app_context():  # Adicione isso para criar um contexto de aplicativo
        response = client.get('/')
        assert response.status_code == 200

def test_add_book(client):
    with app.app_context():  # Adicione isso para criar um contexto de aplicativo
        response = client.post('/add_book', data={'book-title': 'Teste Livro', 'autor': 'Autor Teste', 'genero': 'Ficção', 'status': 'on'})
        assert response.status_code == 302  # Redirecionamento após a adição
    
        livro_adicionado = Livro.query.filter_by(nome='Teste Livro').first()
        assert livro_adicionado is not None

def test_add_people(client):
    with app.app_context():  # Adicione isso para criar um contexto de aplicativo
        response = client.post('/add_people', data={'people-name': 'Teste Pessoa', 'sala': 'Sala Teste', 'matricula': '12345', 'adm': 'on'})
        assert response.status_code == 302  # Redirecionamento após a adição
    
        pessoa_adicionada = Pessoa.query.filter_by(nome='Teste Pessoa').first()
        assert pessoa_adicionada is not None
