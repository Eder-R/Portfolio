import sys
import os
import unittest
import tempfile
from openpyxl import Workbook
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Livro, import_xlsx_to_db

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados na memória
        app.config['SECRET_KEY'] = 'test_key'
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['UPLOAD_FOLDER'] = 'tmp'

        # Criar o diretório temporário de upload
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

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
            deleted_book = db.session.get(Livro, livro_id)
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
            updated_book = db.session.get(Livro, livro_id)
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
        # Criar um arquivo .xlsx válido usando openpyxl
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=True) as tmp_xlsx:
            tmp_xlsx_name = tmp_xlsx.name

        # Criar um arquivo .xlsx com openpyxl
        wb = Workbook()
        sheet = wb.active
        sheet['A1'] = 'Nome'
        sheet['B1'] = 'Autor'
        sheet['C1'] = 'Genero'
        sheet['A2'] = 'Livro Teste'
        sheet['B2'] = 'Autor Teste'
        sheet['C2'] = 'Ficção'  # Adicionada a célula para 'Genero'
        wb.save(tmp_xlsx_name)  # Salva o arquivo .xlsx

        try:
            # Simular o contexto de requisição para flash
            with app.test_request_context():
                # Criar um cliente de teste
                with app.test_client() as client:
                    # Realizar o POST com o arquivo real
                    with open(tmp_xlsx_name, 'rb') as file:
                        response = client.post('/upload', data={
                            'file': (file, 'test.xlsx')
                        })

                    # Verificar se a resposta é um redirecionamento
                    self.assertEqual(response.status_code, 302)

                    # Verificar as mensagens flash
                    with client.session_transaction() as sess:
                        flashes = sess.get('_flashes', [])
                        self.assertTrue(
                            any('Erro ao importar arquivo' in f[1] for f in flashes) or
                            any('Arquivo importado com sucesso!' in f[1] for f in flashes),
                            "Mensagem flash não encontrada ou incorreta."
                        )

                    # Verificar se o arquivo foi processado corretamente no banco
                    livro = Livro.query.filter_by(nome='Livro Teste').first()
                    self.assertIsNotNone(livro, "Livro não foi importado para o banco.")
        finally:
            # Remover o arquivo temporário após o teste
            try:
                os.remove(tmp_xlsx_name)
            except PermissionError as e:
                print(f"Erro ao remover o arquivo: {e}")

if __name__ == '__main__':
    unittest.main()
