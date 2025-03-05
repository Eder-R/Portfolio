from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Modelo da Tabela Livros
class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    genero = Column(String, nullable=False)

# Modelo da Tabela Pessoas
class Pessoa(Base):
    __tablename__ = 'pessoas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    sala = Column(String, nullable=False)

# Modelo da Tabela de Livros Emprestados
class LivroEmprestado(Base):
    __tablename__ = 'livros_emprestados'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    livro_id = Column(Integer, ForeignKey('livros.id'), nullable=False)
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'), nullable=False)
    data_emprestimo = Column(DateTime, default=datetime.utcnow)
    data_devolucao = Column(DateTime, nullable=True)

    # Relacionamentos
    livro = relationship("Livro")
    pessoa = relationship("Pessoa")
