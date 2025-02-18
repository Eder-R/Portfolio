from models import db

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
