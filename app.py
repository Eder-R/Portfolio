'''Função principal para rodar o programa'''
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from waitress import serve
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# from models.models import db, Livro, LivrosEmprestados, Pessoa

host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 5000))

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'database', 'libmanager.db')

# Configurações do banco de dados
load_dotenv()
app = Flask(__name__)

db_folder_path = os.path.abspath(os.path.dirname(__file__))
db_file_path = os.path.join(db_folder_path, 'database\libmanager.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configurações do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configuração do Flask-Migrate
migrate = Migrate(app, db)

LOG_DIR = 'logs'  # Diretório onde os logs serão armazenados

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuração do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Configuração do manipulador de arquivos rotativos por tempo
log_filename = os.path.join(LOG_DIR, 'logs.log.txt')
file_handler = TimedRotatingFileHandler(
    log_filename, when='midnight', interval=1, backupCount=5)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s : %(message)s'))

# Adiciona o manipulador ao logger
logger.addHandler(file_handler)

# Models


class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean(), nullable=True)
    emprestado_para = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'autor': self.autor,
            'genero': self.genero,
            'status': self.status,
            'emprestado_para': self.emprestado_para
        }


class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sala = db.Column(db.String(255), nullable=False)
    matricula = db.Column(db.String(255))
    adm = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sala': self.sala,
            'matricula': self.matricula,
            'adm': self.adm
        }


class LivrosEmprestados(db.Model):
    __tablename__ = 'livros_emprestados'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey(
        'pessoa.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey(
        'livros.id'), nullable=False)
    data_devolucao = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow())

    pessoa = db.relationship('Pessoa', backref=db.backref(
        'livros_emprestados', lazy=True))
    livro = db.relationship('Livro', backref=db.backref(
        'livros_emprestados', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'pessoa_id': self.pessoa_id,
            'livro_id': self.livro_id,
            'data_devolucao': self.data_devolucao.strftime('%Y-%m-%d %H:%M:%S')
        }


@app.route('/', methods=['GET'])
def index():
    '''Rota pagina inicial'''
    return render_template('index.html', page=1)

@app.route('/books', methods=['GET'])
def list_books():
    '''Listar livros conforme o filtro'''
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=15, type=int)
    # Cálculo do offset
    offset = (page - 1) * limit

    # Consulta ao banco de dados usando SQLAlchemy
    # ==========================================================
    # Obtém os parâmetros de filtro do request
    matricula_filtrado = request.args.get('matricula', default=None, type=int)
    sala_filtrado = request.args.get('sala', default=None, type=str)
    nome_filtrado = request.args.get('nome', default=None, type=str)

    genero_filtrado = request.args.get('genero', default=None, type=str)
    autor_filtrado = request.args.get('autor', default=None, type=str)
    nome_filtrado = request.args.get('nome', default=None, type=str)
    # Define o limite de registros por página
    limit = 10
    offset = (page - 1) * limit

    query = Livro.query
    query2 = Pessoa.query

    # Aplica os filtros na consulta conforme necessário
    if genero_filtrado:
        query = query.filter_by(genero=genero_filtrado)

    if autor_filtrado:
        query = query.filter_by(autor=autor_filtrado)

    if nome_filtrado:
        query = query.filter(Livro.nome.like(f"%{nome_filtrado}%"))

    if matricula_filtrado:
        query = query.filter_by(matricula=matricula_filtrado)

    if sala_filtrado:
        query = query.filter_by(sala=sala_filtrado)

    if nome_filtrado:
        query = query.filter(Pessoa.nome.like(f"%{nome_filtrado}%"))

    # Ordena os resultados por nome (ordem alfabética)
    query = query.order_by(Livro.nome).offset(offset).limit(limit)
    query2 = query2.order_by(Pessoa.nome).offset(offset).limit(limit)

    # Obtém os resultados da consulta após aplicar os filtros e ordenação
    livros = query.all()
    pessoas = query2.all()

    autores = get_authors()
    salas = get_salas()

    if request.headers.get('Accept') == 'application/json':
        return jsonify(livros=[livro.to_dict() for livro in livros],
                       pessoas=[pessoa.to_dict() for pessoa in pessoas],
                       autores=autores, salas=salas)
    else:
        return redirect(url_for('index'))


def get_authors():
    '''Função para pegar todos os autores'''
    authors = db.session.query(Livro.autor).distinct().all()
    authors = sorted([author[0] for author in authors])
    return authors


def get_genres():
    '''Função para pegar todos os autores'''
    genres = db.session.query(Livro.genero).distinct().all()
    return [genre[0] for genre in genres]


@app.route('/get_authors', methods=['GET'])
def get_authors_route():
    '''Função para listar todos os autores'''
    authors = get_authors()
    return jsonify(authors=authors)


@app.route('/get_genres', methods=['GET'])
def get_genres_route():
    '''Função para listar todos os generos'''
    genres = get_genres()
    return jsonify(genres=genres)


@app.route('/get_books_count', methods=['GET'])
def get_books_count():
    '''Contagem de dados do banco'''
    count = Livro.query.count()
    return jsonify({'count': count})


@app.route('/cadastro_livros')
def cadastro_livros():
    '''rota para cadastro dos livros'''
    return render_template('_regBooks.html')


@app.route('/add_book', methods=['POST'])
def add_book():
    ''' Adicionar livros '''
    if request.method == 'POST':
        nome = request.form['book-title']
        autor = request.form['autor']
        genero = request.form['genero']
        status = request.form.get('status') == 'on'  # Verifica o status

        novo_livro = Livro(nome=nome, autor=autor,
                           genero=genero, status=status)
        db.session.add(novo_livro)
        db.session.commit()
        # Adicione esta linha para depuração
        print(f"ID do novo livro: {novo_livro.id}")

        return redirect(url_for('cadastro_livros'))


@app.route('/edit_book', methods=['POST'])
def edit_book():
    try:
        # Obter os dados do formulário
        dados_livro = request.json

        # Consultar o livro no banco de dados
        livro = Livro.query.get(dados_livro['id'])

        # Atualizar os dados do livro
        livro.nome = dados_livro['nome']
        livro.autor = dados_livro['autor']
        livro.genero = dados_livro['genero']
        livro.status = dados_livro['status']

        # Commit das alterações no banco de dados
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Dados do livro alterados com sucesso!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    ''' Apagar livro '''
    livro = Livro.query.get(id)
    db.session.delete(livro)
    db.session.commit()
    flash('Livro apagado com sucesso')
    return redirect(url_for('index'))


@app.route('/cadastro_pessoa')
def cadastro_pessoa():
    '''rota para cadastro das pessoas'''
    return render_template('_regClients.html')


@app.route('/add_people', methods=['POST'])
def add_people():
    ''' Adicionar pessoa '''
    if request.method == 'POST':
        nome = request.form['people-name']
        sala = request.form['sala']
        matricula = request.form['matricula']
        adm = request.form.get('adm') == 'on'  # Verifica o status

        nova_pessoa = Pessoa(nome=nome, sala=sala,
                             matricula=matricula, adm=adm)
        db.session.add(nova_pessoa)
        db.session.commit()
        # Adicione esta linha para depuração
        print(f"ID da pessoa: {nova_pessoa.id}")

        return redirect(url_for('cadastro_pessoa'))


def get_salas():
    '''Função para pegar todos os autores'''
    salas = db.session.query(Pessoa.sala).distinct().all()
    sala = sorted([sala[0] for sala in salas])
    return sala


def get_matriculas():
    '''Função para pegar todos os autores'''
    matriculas = db.session.query(Pessoa.matricula).distinct().all()
    matricula = [matricula[0] for matricula in matriculas]
    return matricula


@app.route('/verificar_devolucao')
def verificar_devolucao():
    livros_emprestados = LivrosEmprestados.query.all()

    for emprestimo in livros_emprestados:
        if emprestimo.data_devolucao < datetime.utcnow():
            # Livro está atrasado, atualizar o status
            livro = Livro.query.get(emprestimo.livro_id)
            livro.status = False  # Atualize conforme necessário

    db.session.commit()

    return "Verificação de devolução concluída com sucesso!"


if __name__ == "__main__":
    with app.app_context():
        # Importe e crie as tabelas
        db.create_all()
        print("Tabelas criadas com sucesso!")
        print(f"Servidor rodando em http://{host}:{port}")

    serve(app, host='0.0.0.0', port=5000)
