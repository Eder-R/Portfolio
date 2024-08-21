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

# Carregar variáveis de ambiente do .env
load_dotenv()

host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 5000))

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'database', 'libmanager.db')

# Configuração do Flask e do SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy e Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuração do Logger
LOG_DIR = 'logs'  # Diretório onde os logs serão armazenados

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

log_filename = os.path.join(LOG_DIR, 'logs.log.txt')
file_handler = TimedRotatingFileHandler(
    log_filename, when='midnight', interval=1, backupCount=5)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s : %(message)s'))

logger.addHandler(file_handler)

# Modelos

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

# Demais rotas e funções aqui...

if __name__ == "__main__":
    with app.app_context():
        # Importe e crie as tabelas
        db.create_all()
        print("Tabelas criadas com sucesso!")
        print(f"Servidor rodando em http://{host}:{port}")

    serve(app, host='0.0.0.0', port=5000)
