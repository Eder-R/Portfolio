from app import app
from models import db

def reset_database():
    with app.app_context():
        print("Apagando tabelas existentes...")
        db.drop_all()  # Remove todas as tabelas do banco de dados
        print("Criando tabelas novamente...")
        db.create_all()  # Recria as tabelas
        print("Banco de dados resetado com sucesso!")

if __name__ == "__main__":
    reset_database()
