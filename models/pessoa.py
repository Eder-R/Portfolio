from models import db

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sala = db.Column(db.String(255), nullable=False, default='Indefinido')
    matricula = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False, default="Aluno")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sala': self.sala,
            'matricula': self.matricula,
            'role': self.role
        }
