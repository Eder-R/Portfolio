'''Função principal para rodar o programa'''
from sqlalchemy import func
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from models.models import db, Livro

app = Flask(__name__)

DB_NAME = "LibManager"
DB_USER = "eder3"
DB_PASS = "adm"
DB_HOST = "localhost"

# Configurações do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db.init_app(app)

@app.route('/', methods=['GET'])
def listar_livros():
    '''Listar livros conforme o filtro'''
    #----------------------------------------------------------
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=5, type=int)
    
    # Cálculo do offset
    offset = (page - 1) * limit

    # Consulta ao banco de dados usando SQLAlchemy
    # ==========================================================
    genero_filtrado = request.args.get('genero', default=None, type=str)
    autor_filtrado = request.args.get('autor', default=None, type=str)
    nome = request.args.get('nome', default=None, type=str)  # Mantenha como str

    query = Livro.query

    if genero_filtrado:
        query = query.filter_by(genero=genero_filtrado)

    if autor_filtrado:
        query = query.filter_by(autor=autor_filtrado)

    if nome:
        query = query.filter(Livro.nome.like(f"%{nome}%"))  # Usar 'like' para buscar parte do nome
        
        
    livros = query.offset(offset).limit(limit).all()

    return render_template('_home-adm.html', livros=livros)

def get_authors():
    '''Função para pegar todos os autores'''
    authors = db.session.query(Livro.autor).distinct().all()
    return [author[0] for author in authors]

def get_genres():
    '''Função para pegar todos os autores'''
    genres = db.session.query(Livro.genero).distinct().all()
    return [genre[0] for genre in genres]

@app.route('/get_authors', methods=['GET'])
def get_authors_route():
    '''Função para listar todos os autores'''
    authors = get_authors()
    return jsonify(authors=authors)

@app.route('/get_genres', methods=['GET'])
def get_genres_route():
    '''Função para listar todos os generos'''
    genres = get_genres()
    return jsonify(genres=genres)

@app.route('/books')
def index():
    ''' Mostrar Livros '''
    list_books = Livro.query.all()
    return render_template('index.html', list_books=list_books)

@app.route('/add_book', methods=['POST'])
def add_book():
    ''' Adicionar livros '''
    if request.method == 'POST':
        nome = request.form['nome']
        autor = request.form['autor']
        genero = request.form['genero']
        status = request.form['status']
        
        novo_livro = Livro(nome=nome, autor=autor, genero=genero, status=status)
        db.session.add(novo_livro)
        db.session.commit()
        flash('Livro adicionado com sucesso')
        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    ''' Editar livros'''
    livro = Livro.query.get(id)
    if request.method == 'POST':
        livro.nome = request.form['nome']
        livro.autor = request.form['autor']
        livro.genero = request.form['genero']
        db.session.commit()
        flash('Livro atualizado com sucesso')
        return redirect(url_for('index'))
    return render_template('edit.html', livro=livro)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    ''' Apagar livro '''
    livro = Livro.query.get(id)
    db.session.delete(livro)
    db.session.commit()
    flash('Livro apagado com sucesso')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)