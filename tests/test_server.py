import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
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

# Adicione mais testes para as outras rotas e funcionalidades conforme necessário
