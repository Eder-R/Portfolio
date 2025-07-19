import os
import sys
import logging
import requests
import pandas as pd
from urllib.parse import unquote_plus
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
import webview
import threading
import webbrowser
import unicodedata

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from models import Livro, Pessoa, LivroEmprestado, Base, db
# from models import db

# Configuração do Flask
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'MUDE_ME')

# Configuração do Banco de Dados SQLite
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, 'database', 'lib.db')
DATABASE_URL = f"sqlite:///{DATABASE_DIR}"

# Garante que a pasta 'database/' exista
os.makedirs(os.path.dirname(DATABASE_DIR), exist_ok=True)
# Se desejar criar o banco zerado caso não exista:
if not os.path.exists(DATABASE_DIR):
    print(">> Criando banco de dados inicial...")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Criar as tabelas no banco de dados, se não existirem
Base.metadata.create_all(engine)

# Configuração do Logger
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)
log_filename = os.path.join(LOG_DIR, 'logs.log.txt')
file_handler = RotatingFileHandler(log_filename, maxBytes=1024*1024*5, backupCount=5, delay=True)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s'))
logger.addHandler(file_handler)

@app.route('/')
def index():
    # Parâmetros do filtro via GET
    nome = request.args.get('nome', '').strip()
    autor = request.args.get('autor', '').strip()
    genero = request.args.get('genero', '').strip()

    # Query base
    query = session.query(Livro)

    # Aplica os filtros se preenchidos
    if nome:
        query = query.filter(Livro.nome.ilike(f"%{nome}%"))
    if autor:
        query = query.filter(Livro.autor.ilike(f"%{autor}%"))
    if genero and genero != "Genero":
        query = query.filter(Livro.genero.ilike(f"%{genero}%"))

    livros = query.all()
    pessoas = session.query(Pessoa).all()

    # Consulta empréstimos
    emprestimos = session.query(LivroEmprestado).all()
    emprestimos_dict = {
        e.livro_id: {'nome': e.pessoa.nome, 'sala': e.pessoa.sala}
        for e in emprestimos if e.data_devolucao is None
    }

    # Lista de autores únicos para o filtro
    autores_unicos = sorted(set(l.autor for l in session.query(Livro).all()))
    
    return render_template(
        "index.html",
        livros=livros,
        pessoas=pessoas,
        emprestimos=emprestimos_dict,
        autores=autores_unicos,
        filtro_nome=nome,
        filtro_autor=autor,
        filtro_genero=genero
    )
###
# @app.route('/')
# def index():
#     '''Exibir livros, pessoas e empréstimos'''
#     livros = session.query(Livro).all()
#     pessoas = session.query(Pessoa).all()
#     emprestimos = session.query(LivroEmprestado).all()

#     # Consulta para pegar os livros emprestados e associar com nome e sala da pessoa
#     emprestimos_dict = {}
#     for e in emprestimos:
#         if e.data_devolucao is None and e.pessoa and e.pessoa.nome:
#             emprestimos_dict[e.livro_id] = {
#                 'nome': e.pessoa.nome,
#                 'sala': e.pessoa.sala
#             }

#     return render_template("index.html", livros=livros, pessoas=pessoas, emprestimos=emprestimos_dict)
###
@app.route('/livros')
def listar_livros():
    '''Exibir a lista de livros com filtros opcionais'''
    nome = request.args.get('nome', '').strip()
    autor = request.args.get('autor', '').strip()
    genero = request.args.get('genero', '').strip()

    query = session.query(Livro)

    if nome:
        query = query.filter(Livro.nome.ilike(f"%{nome}%"))
    if autor:
        query = query.filter(Livro.autor.ilike(f"%{autor}%"))
    if genero and genero != "Genero":
        query = query.filter(Livro.genero.ilike(f"%{genero}%"))

    livros = query.all()

    # Carregar os dados de empréstimos
    emprestimos = session.query(LivroEmprestado).filter_by(data_devolucao=None).all()
    emprestimos_dict = {e.livro_id: e for e in emprestimos}

    return render_template("listarLivros.html", livros=livros, emprestimos=emprestimos_dict)

@app.route('/pessoas')
def listar_pessoas():
    '''Exibir a lista de pessoas'''
    pessoas = session.query(Pessoa).all()
    return render_template("listarPessoas.html", pessoas=pessoas)

@app.route('/add_book', methods=['POST'])
def add_book():
    ''' Adicionar livros '''
    nome = request.form.get('nome', '').strip()
    autor = request.form.get('autor', '').strip()
    genero = request.form.get('genero', '').strip()

    if not nome or not autor or not genero:
        flash("Todos os campos são obrigatórios!", "error")
        return redirect(url_for('cadastro_livros'))
    
    # API para buscar a capa do livro (exemplo usando Open Library)
    api_url = f"https://openlibrary.org/search.json?title={nome}&author={autor}"
    response = requests.get(api_url)
    
    capa_url = None
    if response.status_code == 200:
        data = response.json()
        if "docs" in data and len(data["docs"]) > 0:
            cover_id = data["docs"][0].get("cover_i")
            if cover_id:
                capa_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

    novo_livro = Livro(nome=nome, autor=autor, genero=genero, capa_url=capa_url)
    session.add(novo_livro)
    session.commit()
    flash("Livro cadastrado com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/cadastro_livros')
def cadastro_livros():
    '''Exibir página de cadastro de livros'''
    return render_template("cadastroLivros.html")

@app.route('/update_book/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    '''Editar informações do livro'''
    livro = session.query(Livro).get(id)
    if not livro:
        flash("Livro não encontrado!", "error")
        return redirect(url_for('listar_livros'))

    if request.method == 'POST':
        livro.nome = request.form.get('nome', livro.nome).strip()
        livro.autor = request.form.get('autor', livro.autor).strip()
        livro.genero = request.form.get('genero', livro.genero).strip()

        # Verifica se o livro está sendo marcado como emprestado
        emprestado_para = request.form.get('emprestado_para')
        pessoa = session.query(Pessoa).filter_by(nome=emprestado_para).first() if emprestado_para else None

        if pessoa:
            # Registrar empréstimo se ainda não estiver emprestado
            if not session.query(LivroEmprestado).filter_by(livro_id=id, data_devolucao=None).first():
                emprestimo = LivroEmprestado(livro_id=id, pessoa_id=pessoa.id)
                session.add(emprestimo)
        else:
            # Se o livro estava emprestado e agora está disponível, registrar devolução
            emprestimo = session.query(LivroEmprestado).filter_by(livro_id=id, data_devolucao=None).first()
            if emprestimo:
                emprestimo.data_devolucao = datetime.utcnow()

        session.commit()
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for('listar_livros'))

    return render_template("editarLivros.html", livro=livro)

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    ''' Apagar livro '''
    livro = session.query(Livro).get(id)
    session.delete(livro)
    session.commit()
    return redirect(url_for('index'))

@app.route('/add_person', methods=['POST'])
def add_person():
    ''' Adicionar pessoa '''
    nome = request.form.get('people-name', '').strip()
    sala = request.form.get('sala', '').strip()
    matricula = request.form.get('matricula', '').strip()

    # Verifica se os campos estão preenchidos
    if not nome or not sala or not matricula:
        flash("Todos os campos são obrigatórios!", "error")
        return redirect(url_for('cadastroPessoas'))

    # Verifica se a matrícula já existe
    pessoa_existente = session.query(Pessoa).filter_by(matricula=matricula).first()
    if pessoa_existente:
        flash("Já existe uma pessoa com essa matrícula!", "error")
        return redirect(url_for('cadastroPessoas'))

    # Cria nova pessoa e adiciona ao banco
    nova_pessoa = Pessoa(nome=nome, sala=sala, matricula=matricula)
    session.add(nova_pessoa)
    session.commit()

    flash("Pessoa cadastrada com sucesso!", "success")
    return redirect(url_for('listar_pessoas'))

@app.route('/cadastro_pessoas')
def cadastro_pessoas():
    '''Exibir página de cadastro de pessoas'''
    return render_template("cadastroPessoas.html")

@app.route('/delete_person/<int:id>', methods=['POST'])
def delete_person(id):
    ''' Apagar pessoa '''
    pessoa = session.query(Pessoa).get(id)
    session.delete(pessoa)
    session.commit()
    return redirect(url_for('index'))

@app.route('/emprestar_livro/<int:livro_id>/<int:pessoa_id>', methods=['POST'])
def emprestar_livro(livro_id, pessoa_id):
    ''' Registrar empréstimo '''
    livro = session.query(Livro).get(livro_id)
    pessoa = session.query(Pessoa).get(pessoa_id)

    if not livro or not pessoa:
        flash("Livro ou pessoa não encontrados.", "error")
        return redirect(url_for('index'))

    if session.query(LivroEmprestado).filter_by(livro_id=livro_id, data_devolucao=None).first():
        flash("Livro já está emprestado!", "error")
        return redirect(url_for('index'))

    emprestimo = LivroEmprestado(livro_id=livro.id, pessoa_id=pessoa.id)
    session.add(emprestimo)
    session.commit()
    flash("Livro emprestado com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/devolver_livro/<int:id>', methods=['POST'])
def devolver_livro(id):
    ''' Registrar devolução '''
    emprestimo = session.query(LivroEmprestado).filter_by(livro_id=id, data_devolucao=None).first()

    if not emprestimo:
        flash("Nenhum empréstimo ativo encontrado para este livro.", "error")
        return redirect(url_for('index'))

    emprestimo.data_devolucao = datetime.utcnow()
    session.commit()
    flash("Livro devolvido com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/upload_books', methods=['POST'])
def upload_books():
    ''' Importar livros via arquivo Excel '''
    file = request.files['file']
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            nome = row['Nome']
            autor = row['Autor']
            genero = row['Genero']
            
            # Buscar imagem na Open Library
            capa_url = None
            try:
                response = requests.get(
                    f"https://openlibrary.org/search.json?title={nome}&author={autor}"
                )
                if response.status_code == 200:
                    data = response.json()
                    if "docs" in data and data["docs"]:
                        cover_id = data["docs"][0].get("cover_i")
                        if cover_id:
                            capa_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            except Exception as e:
                print(f"Erro ao buscar capa para '{nome}':", e)

            livro = Livro(nome=nome, autor=autor, genero=genero, capa_url=capa_url)
            session.add(livro)
        session.commit()
        flash('Livros importados com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/upload_people', methods=['POST'])
def upload_people():
    ''' Importar pessoas via arquivo Excel '''
    file = request.files['file']
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            pessoa = Pessoa(nome=row['Nome'], sala=row['Sala'], matricula=row['Matrícula'])
            session.add(pessoa)
        session.commit()
        flash('Pessoas importadas com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/api/livros', methods=['GET'])
def api_get_livros():
    '''Listar todos os livros como JSON'''
    livros = session.query(Livro).all()
    return jsonify([{
        'id': livro.id,
        'nome': livro.nome,
        'autor': livro.autor,
        'genero': livro.genero
    } for livro in livros])

@app.route('/api/livros', methods=['POST'])
def api_create_book():
    '''Cria um novo livro'''
    data = request.get_json()
    if not data or not all(key in data for key in ["nome", "autor", "genero"]):
        return jsonify({"error": "Dados inválidos"}), 400
    
    novo_livro = Livro(nome=data["nome"], autor=data["autor"], genero=data["genero"])
    session.add(novo_livro)
    session.commit()
    return jsonify({"message": "Livro criado com sucesso", "id": novo_livro.id}), 201

@app.route('/api/livros/<int:id>', methods=['PUT'])
def api_update_book(id):
    '''Atualiza um livro existente'''
    livro = session.query(Livro).get(id)
    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    data = request.get_json()
    livro.nome = data.get("nome", livro.nome)
    livro.autor = data.get("autor", livro.autor)
    livro.genero = data.get("genero", livro.genero)
    session.commit()
    
    return jsonify({"message": "Livro atualizado com sucesso"})

@app.route('/api/livros/<int:id>', methods=['DELETE'])
def api_delete_book(id):
    '''Deleta um livro'''
    livro = session.query(Livro).get(id)
    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    session.delete(livro)
    session.commit()
    return jsonify({"message": "Livro removido com sucesso"})

@app.route('/api/pessoas', methods=['GET'])
def api_get_person():
    '''Listar todas as pessoas como JSON'''
    pessoas = session.query(Pessoa).all()
    return jsonify([{
        'id': pessoa.id,
        'nome': pessoa.nome,
        'sala': pessoa.sala,
        'matricula': pessoa.matricula
    } for pessoa in pessoas])

@app.route('/api/pessoas', methods=['POST'])
def api_create_person():
    '''Cria uma nova pessoa'''
    data = request.get_json()
    if not data or not all(key in data for key in ["nome", "sala", "matricula"]):
        return jsonify({"error": "Dados inválidos"}), 400
    
    nova_pessoa = Pessoa(nome=data["nome"], sala=data["sala"], matricula=data["matricula"])
    session.add(nova_pessoa)
    session.commit()
    return jsonify({"message": "Pessoa cadastrada com sucesso", "id": nova_pessoa.id}), 201

@app.route('/api/pessoas/<int:id>', methods=['PUT'])
def api_update_person(id):
    '''Atualiza os dados de uma pessoa'''
    pessoa = session.query(Pessoa).get(id)
    if not pessoa:
        return jsonify({"error": "Pessoa não encontrada"}), 404

    data = request.get_json()
    pessoa.nome = data.get("nome", pessoa.nome)
    pessoa.sala = data.get("sala", pessoa.sala)
    pessoa.matricula = data.get("matricula", pessoa.matricula)
    session.commit()
    
    return jsonify({"message": "Dados da pessoa atualizados com sucesso"})

@app.route('/api/pessoas/<int:id>', methods=['DELETE'])
def api_delete_person(id):
    '''Deleta uma pessoa'''
    pessoa = session.query(Pessoa).get(id)
    if not pessoa:
        return jsonify({"error": "Pessoa não encontrada"}), 404
    
    session.delete(pessoa)
    session.commit()
    return jsonify({"message": "Pessoa removida com sucesso"})

@app.route('/api/emprestimos', methods=['POST'])
def api_create_emprestimo():
    '''Registra um novo empréstimo'''
    data = request.get_json()
    if not data or not all(key in data for key in ["livro_id", "pessoa_id"]):
        return jsonify({"error": "Dados inválidos"}), 400

    emprestimo = LivroEmprestado(livro_id=data["livro_id"], pessoa_id=data["pessoa_id"])
    session.add(emprestimo)
    session.commit()
    return jsonify({"message": "Livro emprestado com sucesso", "id": emprestimo.id}), 201

@app.route('/api/emprestimos/<int:id>', methods=['PUT'])
def api_devolver_livro(id):
    '''Registra a devolução de um livro'''
    emprestimo = session.query(LivroEmprestado).get(id)
    if not emprestimo:
        return jsonify({"error": "Empréstimo não encontrado"}), 404

    emprestimo.data_devolucao = datetime.utcnow()
    session.commit()
    
    return jsonify({"message": "Livro devolvido com sucesso"})

def iniciar_flask():
    app.run(debug=True, use_reloader=False)

def normalizar(texto):
    if not texto:
        return ''
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.lower().strip()

if __name__ == '__main__':
    print(">> Iniciando servidor Flask...")
    threading.Thread(target=iniciar_flask, daemon=True).start()

    print(">> Aguardando servidor subir...")
    time.sleep(2)

    print(">> Abrindo no navegador padrão...")
    webbrowser.open("http://127.0.0.1:5000")

    # Impede que o script se encerre imediatamente
    while True:
        time.sleep(1)