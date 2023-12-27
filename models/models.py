'''Arquivo com os models carregados'''
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livro(db.Model):
    '''Classe com o Model livros'''
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean(), nullable=True)
    emprestado_para = db.Column(db.String(255))  # Nova coluna

    def __repr__(self):
        return f"<Livro {self.id} - {self.nome}>"

class Pessoa(db.Model):
    '''Classe com o Model para pessoas'''
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sala = db.Column(db.String(255), nullable=False)
    matricula = db.Column(db.String(255))
    adm = db.Column(db.Boolean, default=False, nullable=False)

class LivrosEmprestados(db.Model):
    '''Classe com o Model para livros emprestados'''
    __tablename__ = 'livros_emprestados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    data_devolucao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow() + timedelta(days=7))

    pessoa = db.relationship('Pessoa', backref=db.backref('livros_emprestados', lazy=True))
    livro = db.relationship('Livro', backref=db.backref('livros_emprestados', lazy=True))
