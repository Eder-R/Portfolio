'''Arquivo com os models carregados'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livro(db.Model):
    '''Classe com o Model livros'''
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean(), nullable=True)

    def __init__(self, nome, autor, genero, status):
        self.nome = nome
        self.autor = autor
        self.genero = genero
        self.status = status

class Pessoa(db.Model):
    '''Classe com o Model para pessoas'''
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sala = db.Column(db.String(255), nullable=False)
    matricula = db.Column(db.String(255))
    adm = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, nome, sala, matricula=None, adm=False):
        self.nome = nome
        self.sala = sala
        self.matricula = matricula
        self.adm = adm
