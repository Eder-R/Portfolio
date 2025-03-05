import pytest
from flask import url_for
import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, session
from models.models import Livro, Pessoa, LivroEmprestado

@pytest.fixture(scope="module")
def test_client():
    """Cria um cliente de teste para a API"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture(autouse=True)
def seed_database():
    """Garante que existam livros e pessoas no banco antes dos testes."""
    with app.app_context():
        session.rollback()  # Evita conflitos anteriores
        session.query(LivroEmprestado).delete()
        session.query(Livro).delete()
        session.query(Pessoa).delete()

        # Criar um livro e uma pessoa
        livro = Livro(nome="Livro Teste", autor="Autor Teste", genero="Ficção")
        pessoa = Pessoa(nome="Pessoa Teste", sala="101", matricula="123456")

        session.add(livro)
        session.add(pessoa)
        session.commit()


@pytest.fixture(autouse=True)
def clean_db():
    """Limpa o banco antes de cada teste"""
    with app.app_context():
        session.rollback()
        session.query(LivroEmprestado).delete()
        session.query(Livro).delete()
        session.query(Pessoa).delete()
        session.commit()

# ------------------- TESTES API -------------------

def test_api_create_book(test_client):
    """Testa a criação de um livro via API"""
    response = test_client.post('/api/livros', json={
        "nome": "Livro Teste",
        "autor": "Autor Teste",
        "genero": "Ficção"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Livro criado com sucesso"

def test_api_get_livros(test_client):
    """Testa listagem de livros via API"""
    response = test_client.get('/api/livros')
    assert response.status_code == 200
    livros = response.get_json()
    assert isinstance(livros, list)
    assert len(livros) > 0  # Deve existir pelo menos 1 livro cadastrado

def test_api_update_book(test_client):
    """Testa atualização de um livro via API"""
    livro = session.query(Livro).first()
    assert livro is not None  # Garante que existe um livro antes do teste
    response = test_client.put(f'/api/livros/{livro.id}', json={
        "nome": "Livro Atualizado"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Livro atualizado com sucesso"

def test_api_delete_book(test_client):
    """Testa exclusão de um livro via API"""
    livro = session.query(Livro).first()
    response = test_client.delete(f'/api/livros/{livro.id}')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Livro removido com sucesso"

def test_api_create_person(test_client):
    """Testa a criação de uma pessoa via API com matrícula única"""
    unique_matricula = str(uuid.uuid4())[:8]  # Gera um ID único curto
    response = test_client.post('/api/pessoas', json={
        "nome": "Pessoa Teste",
        "sala": "Sala 101",
        "matricula": unique_matricula
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Pessoa cadastrada com sucesso"

def test_api_get_pessoas(test_client):
    """Testa listagem de pessoas via API"""
    response = test_client.get('/api/pessoas')
    assert response.status_code == 200
    pessoas = response.get_json()
    assert isinstance(pessoas, list)
    assert len(pessoas) > 0  # Deve existir pelo menos 1 pessoa cadastrada

def test_api_create_emprestimo(test_client):
    """Testa o empréstimo de um livro via API"""
    livro = session.query(Livro).first()
    pessoa = session.query(Pessoa).first()
    response = test_client.post('/api/emprestimos', json={
        "livro_id": livro.id,
        "pessoa_id": pessoa.id
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Livro emprestado com sucesso"

def test_api_devolver_livro(test_client):
    """Testa devolução de um livro via API garantindo que há um empréstimo ativo"""
    livro = session.query(Livro).first()
    pessoa = session.query(Pessoa).first()
     # Criar empréstimo antes do teste
    emprestimo = LivroEmprestado(livro_id=livro.id, pessoa_id=pessoa.id)
    session.add(emprestimo)
    session.commit()

    response = test_client.put(f'/api/emprestimos/{emprestimo.id}')
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Livro devolvido com sucesso"