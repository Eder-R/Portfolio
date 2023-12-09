import os
import sys
import pytest
from flask import Flask
from flask.testing import FlaskClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import *
from models.models import *

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Cria tabelas no banco de dados de teste
    with app.app_context():
        db.create_all()

    yield client

def test_listar_livros_route(client):
    response = client.get('/')
    assert response.status_code == 200  # Verifica se a rota está acessível
    assert b'Listar livros conforme o filtro' in response.data  # Verifica se a página carrega corretamente

def test_get_authors_route(client):
    response = client.get('/get_authors')
    assert response.status_code == 200  # Verifica se a rota está acessível
    # Aqui você pode adicionar mais asserções para verificar se a resposta é válida

def test_cadastro_livros_route(client):
    response = client.get('/cadastro_livros')
    assert response.status_code == 200  # Verifica se a rota está acessível

def test_listar_livros(client):
    # Adicione um livro de exemplo ao banco de dados de teste
    with app.app_context():
        livro_exemplo = Livro(nome="Livro Teste", autor="Autor Teste", genero="Gênero Teste", status=True)
        db.session.add(livro_exemplo)
        db.session.commit()

    # Faça uma solicitação à rota listar_livros
    response = client.get('/')

    # Verifique se a resposta é bem-sucedida (código de status 200)
    assert response.status_code == 200

    # Converta a string para bytes usando UTF-8 para evitar o erro com caracteres especiais
    assert 'Livro Teste'.encode('utf-8') in response.data
    assert 'Autor Teste'.encode('utf-8') in response.data
    assert 'Gênero Teste'.encode('utf-8') in response.data

def test_add_book_route(client):
    response = client.post('/add_book', data={
        'book-title': 'Novo Livro',
        'autor': 'Autor Teste',
        'genero': 'Gênero Teste',
        'status': 'on'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Novo Livro' in response.data

# def test_edit_book_route(client):
#     # Adiciona um livro de exemplo ao banco de dados de teste
#     with app.app_context():
#         livro_exemplo = Livro(nome="Livro Teste", autor="Autor Teste", genero="Gênero Teste", status=True)
#         db.session.add(livro_exemplo)
#         db.session.commit()

#     response = client.post(f'/edit/{livro_exemplo.id}', data={
#         'nome': 'Livro Modificado',
#         'autor': 'Autor Modificado',
#         'genero': 'Gênero Modificado',
#         'status': 'on'
#     }, follow_redirects=True)

#     assert response.status_code == 200
#     assert b'Livro Modificado' in response.data

# def test_delete_book_route(client):
#     # Adiciona um livro de exemplo ao banco de dados de teste
#     with app.app_context():
#         livro_exemplo = Livro(nome="Livro Teste", autor="Autor Teste", genero="Gênero Teste", status=True)
#         db.session.add(livro_exemplo)
#         db.session.commit()

#     response = client.post(f'/delete/{livro_exemplo.id}', follow_redirects=True)

#     assert response.status_code == 200
#     assert b'Livro Teste' not in response.data

def test_get_books_count_route(client):
    response = client.get('/get_books_count')
    assert response.status_code == 200
    assert b'count' in response.data

# def test_cadastro_pessoa_route(client):
#     response = client.get('/cadastro_pessoa')
#     assert response.status_code == 200

# def test_add_people_route(client):
#     response = client.post('/add_people', data={
#         'people-name': 'Nova Pessoa',
#         'sala': 'Sala Teste',
#         'matricula': '12345',
#         'adm': 'on'
#     }, follow_redirects=True)

#     assert response.status_code == 200
#     assert b'Nova Pessoa' in response.data

def test_unknown_route(client):
    response = client.get('/rota_inexistente')
    assert response.status_code == 404
