import unittest
from ..app import app, db, Livro, Pessoa

class FlaskAppTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Executado uma vez antes de todos os testes"""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        
        # Cria as tabelas no banco de dados para os testes
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Executado uma vez após todos os testes"""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Executado antes de cada teste"""
        self.livro = Livro(nome='Test Book', autor='Test Author', genero='Fiction', status=True)

    def test_add_book(self):
        db.session.add(self.livro)
        db.session.commit()
        # Adicione mais asserções aqui para validar o teste

    # Adicione outros métodos de teste aqui

if __name__ == '__main__':
    unittest.main()
