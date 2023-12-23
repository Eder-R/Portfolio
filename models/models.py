"""Função para armazenar os models"""
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship, declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey

engine = create_engine('sqlite:///database/LibManager.db', echo=True)
Base = declarative_base()
db = SQLAlchemy()

class Livro(Base):
    """Classe representando um livro."""
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    genero = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False, default=False)  # Corrigido aqui
    emprestado_para = Column(String(255))
    criado_em = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        return f"<Livro {self.id} - {self.nome}>"

class Pessoa(Base):
    """Classe representando uma pessoa."""
    __tablename__ = 'pessoa'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    sala = Column(String(255), nullable=False)
    matricula = Column(String(255))
    adm = Column(Boolean, default=False, nullable=False)

class LivrosEmprestados(Base):
    """Classe representando livros emprestados."""
    __tablename__ = 'livros_emprestados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pessoa_id = Column(Integer, ForeignKey('pessoa.id'), nullable=False)
    livro_id = Column(Integer, ForeignKey('livros.id'), nullable=False)
    data_devolucao = Column(DateTime, nullable=True,
                            default=datetime.utcnow() + timedelta(days=7))

    pessoa = relationship('Pessoa', backref='livros_emprestados')
    livro = relationship('Livro', backref='livros_emprestados')

Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso.")
