from models import db
from datetime import datetime

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
