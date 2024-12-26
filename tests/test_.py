import sys
import os
import unittest
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Livro, import_xlsx_to_db

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados na memória
        app.config['SECRET_KEY'] = 'test_secret'
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        """Testar a adição de um novo livro"""
        with app.test_client() as client:
            response = client.post('/add_book', data={
                'book-title': 'Test Book',
                'autor': 'Test Author',
                'genero': 'Test Genre',
                'status': 'on',
                'borrower': 'Test Borrower'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            livro = Livro.query.filter_by(nome='Test Book').first()
            self.assertIsNotNone(livro)
            self.assertEqual(livro.autor, 'Test Author')

    def test_delete_book(self):
        """Testar exclusão de um livro"""
        with app.app_context():
            livro = Livro(nome='Delete Book', autor='Delete Author', genero='Delete Genre')
            db.session.add(livro)
            db.session.commit()
            livro_id = livro.id
        
        with app.test_client() as client:
            response = client.post(f'/delete_book/{livro_id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            deleted_book = Livro.query.get(livro_id)
            self.assertIsNone(deleted_book)

    def test_edit_book(self):
        """Testar a edição de um livro"""
        with app.app_context():
            livro = Livro(nome='Edit Book', autor='Edit Author', genero='Edit Genre')
            db.session.add(livro)
            db.session.commit()
            livro_id = livro.id

        with app.test_client() as client:
            response = client.post(f'/edit_book/{livro_id}', data={
                'nome': 'Updated Book',
                'autor': 'Updated Author',
                'genero': 'Updated Genre',
                'status': 'on',
                'emprestado_para': 'Updated Borrower'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            updated_book = Livro.query.get(livro_id)
            self.assertEqual(updated_book.nome, 'Updated Book')
            self.assertEqual(updated_book.autor, 'Updated Author')

    def test_get_books_count(self):
        """Testar a contagem de livros"""
        with app.app_context():
            db.session.query(Livro).delete()
            db.session.commit()

            livro = Livro(nome='Count Book', autor='Count Author', genero='Count Genre')
            db.session.add(livro)
            db.session.commit()

        with app.test_client() as client:
            response = client.get('/get_books_count')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['count'], 1)

            # Testar após a exclusão
            with app.app_context():
                db.session.query(Livro).delete()
                db.session.commit()
            
            response = client.get('/get_books_count')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['count'], 0)

    def test_import_xlsx_to_db(self):
        """Testar a importação de um arquivo XLSX para o banco de dados"""
        # Simulando um arquivo XLSX em memória
        xlsx_data = b'PK\x03\x04\x14\x00\x06\x00\x08\x00\x8f\x93\xa0=\x99\xe6#\x00\x00\x00\x00\x00'
        xlsx_file = BytesIO(xlsx_data)
        xlsx_file.filename = 'test.xlsx'
        
        # Iniciando o contexto de aplicação para o teste
        with app.app_context():
            # Garantir que o banco de dados seja configurado
            db.create_all()  # Cria todas as tabelas, caso não existam
            import_xlsx_to_db(xlsx_file)


if __name__ == '__main__':
    unittest.main()
