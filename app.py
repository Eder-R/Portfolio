import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from logging.handlers import RotatingFileHandler
from waitress import serve
import pandas as pd
from flask_migrate import Migrate
from models import db, init_app
from models.livro import Livro
from models.pessoa import Pessoa
from models.livros_emprestados import LivrosEmprestados

host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 5000))

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'database', 'libmanager.db')

# Configuração do Flask e do SQLAlchemy
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'MUDE_ME')  
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'upload'

# Inicialização do SQLAlchemy e Flask-Migrate
db = init_app(app)
migrate = Migrate(app, db)

# Configuração do Logger
LOG_DIR = 'logs'  # Diretório onde os logs serão armazenados

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

log_filename = os.path.join(LOG_DIR, 'logs.log.txt')
# Remover handlers antigos
for handler in logger.handlers[:]:
    logger.removeHandler(handler)
    handler.close()

file_handler = RotatingFileHandler(
    log_filename, maxBytes=1024*1024*5, backupCount=5, delay=True)

# Adicionar o novo handler
logger.addHandler(file_handler)
# file_handler = TimedRotatingFileHandler(
#     log_filename, when='midnight', interval=1, backupCount=5, delay=True)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s : %(message)s'))

logger.addHandler(file_handler)

# Demais rotas e funções aqui...
@app.route("/index")
def index():
    ''' Rota para testes '''
    return redirect('/')

@app.route('/', methods=['GET'])
def listar_livros():
    '''Listar livros e pessoas conforme os filtros'''
    # Parâmetros de paginação
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    offset = (page - 1) * limit
    # Parâmetros de filtro para livros
    genero_filtrado = request.args.get('genero', default=None, type=str)
    autor_filtrado = request.args.get('autor', default=None, type=str)
    nome_livro_filtrado = request.args.get('nome_livro', default=None, type=str)
    # Parâmetros de filtro para pessoas
    matricula_filtrado = request.args.get('matricula', default=None, type=int)
    sala_filtrado = request.args.get('sala', default=None, type=str)
    nome_pessoa_filtrado = request.args.get('nome_pessoa', default=None, type=str)
    # Consultas para livros
    query_livros = Livro.query
    if genero_filtrado:
        query_livros = query_livros.filter_by(genero=genero_filtrado)
    if autor_filtrado:
        query_livros = query_livros.filter_by(autor=autor_filtrado)
    if nome_livro_filtrado:
        query_livros = query_livros.filter(Livro.nome.like(f"%{nome_livro_filtrado}%"))
    # Consultas para pessoas
    query_pessoas = Pessoa.query
    if matricula_filtrado:
        query_pessoas = query_pessoas.filter_by(matricula=matricula_filtrado)
    if sala_filtrado:
        query_pessoas = query_pessoas.filter_by(sala=sala_filtrado)
    if nome_pessoa_filtrado:
        query_pessoas = query_pessoas.filter(Pessoa.nome.like(f"%{nome_pessoa_filtrado}%"))
    # Aplicar paginação
    livros = query_livros.order_by(Livro.nome).offset(offset).limit(limit).all()
    pessoas = query_pessoas.order_by(Pessoa.nome).offset(offset).limit(limit).all()
    # Dados auxiliares
    autores = get_authors()
    salas = get_salas()
    # Renderiza ambos os dados no template
    return render_template(
        'index.html',
        livros=livros,
        pessoas=pessoas,
        page=page,
        limit=limit,
        autores=autores,
        salas=salas
    )

def get_authors():
    '''Função para pegar todos os autores'''
    authors = db.session.query(Livro.autor).distinct().all()
    authors = sorted([author[0] for author in authors])
    return authors

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

@app.route('/get_books_count', methods=['GET'])
def get_books_count():
    '''Contagem de dados do banco'''
    count = Livro.query.count()
    return jsonify({'count': count})

@app.route('/cadastro_livros')
def cadastro_livros():
    '''rota para cadastro dos livros'''
    return render_template('cadastroLivros.html')

@app.route('/add_book', methods=['POST'])
def add_book():
    ''' Adicionar livros '''
    if request.method == 'POST':
        nome = request.form['book-title']
        autor = request.form['autor']
        genero = request.form['genero']
        status = request.form.get('status') == 'on'  # Verifica o status

        # Se o livro está emprestado, verifique a pessoa
        emprestado_para = request.form.get('borrower') if status else None
        pessoa = None
        
        # Verifique se a pessoa já está registrada
        if emprestado_para:
            pessoa = Pessoa.query.filter_by(
                    nome=emprestado_para
                ).first()
            if not pessoa:
                # Cadastra a nova pessoa se não existir
                pessoa = Pessoa(nome=emprestado_para)
                db.session.add(pessoa)
                db.session.commit()

       # Criação do novo livro
        novo_livro = Livro(nome=nome, autor=autor, genero=genero, status=status, emprestado_para=pessoa.id if pessoa else None)
        db.session.add(novo_livro)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/emprestar_livro/<int:livro_id>/<int:pessoa_id>', methods=['POST'])
def emprestar_livro(livro_id, pessoa_id):
    livro = db.session.get(Livro, livro_id)
    pessoa = db.session.get(Pessoa, pessoa_id)
    if not livro:
        abort(404, description="Livro não encontrado")
    if not pessoa:
        abort(404, description="Pessoa não encontrada")
    # Se o livro não está emprestado, empresta
    if livro.status is True:  # O livro está disponível
        livro.status = False  # Livro agora está emprestado
        livro.emprestado_para_id = pessoa.id
        
        # Registrar o empréstimo na tabela de LivrosEmprestados
        emprestimo = LivrosEmprestados(livro_id=livro.id, pessoa_id=pessoa.id, data_devolucao=None)
        db.session.add(emprestimo)
        db.session.commit()
        flash('Livro emprestado com sucesso', 'success')
    else:
        flash('Livro já está emprestado', 'error')

    return redirect(url_for('listar_livros'))

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    livro = db.session.get(Livro, id)
    if request.method == 'POST':
        livro.nome = request.form['nome']
        livro.autor = request.form['autor']
        livro.genero = request.form['genero']
        livro.status = request.form.get('status') == 'on'
        # Verifique se o livro foi marcado como emprestado
        emprestado_para = request.form.get('emprestado_para') if livro.status else None
        pessoa = None
        
        if emprestado_para:
            pessoa = Pessoa.query.filter_by(nome=emprestado_para).first()
            if not pessoa:
                # Cadastrar uma nova pessoa, se não existir
                pessoa = Pessoa(nome=emprestado_para)
                db.session.add(pessoa)
                db.session.commit()
                print(f"ID da nova pessoa: {pessoa.id}")  # Adicione esta linha para depuração
                
        # Atualizar o campo de empréstimo do livro
        livro.emprestado_para = pessoa.nome if pessoa else None
        db.session.commit()
        flash('Livro atualizado com sucesso')
        return redirect(url_for('listar_livros'))
    return render_template('editarLivros.html', livro=livro)

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    ''' Apagar livro '''
    livro = Livro.query.get(id)
    db.session.delete(livro)
    db.session.commit()
    flash('Livro apagado com sucesso')
    return redirect(url_for('index'))

@app.route('/delete_person/<int:id>', methods=['POST'])
def delete_person(id):
    ''' Apagar pessoa '''
    pessoa = db.session.get(Pessoa, id)
    db.session.delete(pessoa)
    db.session.commit()
    flash('Pessoa apagada com sucesso')
    return redirect(url_for('index'))

@app.route('/cadastro_pessoa')
def cadastro_pessoa():
    '''rota para cadastro das pessoas'''
    return render_template('cadastroPessoas.html')

@app.route('/add_people', methods=['POST'])
def add_people():
    ''' Adicionar pessoa '''
    if request.method == 'POST':
        nome = request.form['people-name']
        sala = request.form['sala']
        matricula = request.form['matricula']
        role = request.form.get('role')  # Verifica o status

        nova_pessoa = Pessoa(nome=nome, sala=sala, matricula=matricula, role=role)
        db.session.add(nova_pessoa)
        db.session.commit()
        print(f"ID da pessoa: {nova_pessoa.id}")  # Adicione esta linha para depuração

        return redirect(url_for('cadastro_pessoa'))

@app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    pessoa = db.session.get(Pessoa, id)
    page = 1 
    if not pessoa:
        flash('Cliente não encontrado', 'error')
        return redirect(url_for('listar_clientes'))
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.sala = request.form['sala']
        pessoa.matricula = request.form['matricula']
        pessoa.role = request.form['role']
        
        db.session.commit()
        flash('Cliente atualizado com sucesso', 'success')
        return redirect(url_for('listar_livros'))
    
    return render_template('editarClients.html', pessoa=pessoa)

def get_salas():
    '''Função para pegar todos os autores'''
    salas = db.session.query(Pessoa.sala).distinct().all()
    sala = sorted([sala[0] for sala in salas])
    return sala

def get_matriculas():
    '''Função para pegar todos os autores'''
    matriculas = db.session.query(Pessoa.matricula).distinct().all()
    matricula = [matricula[0] for matricula in matriculas]
    return matricula

@app.route('/verificar_devolucao')
def verificar_devolucao():
    livros_emprestados = LivrosEmprestados.query.all()

    for emprestimo in livros_emprestados:
        if emprestimo.data_devolucao and emprestimo.data_devolucao < datetime.utcnow():
            # Livro está atrasado, atualizar o status
            livro = Livro.query.get(emprestimo.livro_id)
            livro.status = True  # Livro está disponível após devolução

    db.session.commit()

    return "Verificação de devolução concluída com sucesso!"

@app.route('/livros', methods=['GET'])
def list_books():
    ''' Exibir livros em HTML '''
    livros = Livro.query.all()  # Consulta todos os livros do banco de dados
    return render_template('listarLivros.html', livros=livros)

@app.route('/pessoas', methods=['GET'])
def list_persons():
    """Listar todas as pessoas cadastradas."""
    pessoas = Pessoa.query.order_by(Pessoa.nome).all()  # Consulta todas as pessoas do banco de dados
    pessoas_dict = [pessoa.to_dict() for pessoa in pessoas]  # Converte para JSON
    print(f'pessoas listadas:\n {pessoas_dict}')  # Exibe no terminal
    return render_template('listarPessoas.html', pessoas=pessoas_dict)

@app.route('/api/livros', methods=['GET'])
def api_listar_livros():
    '''Listar todos os livros como JSON com paginação'''
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    offset = (page - 1) * limit

    livros = Livro.query.offset(offset).limit(limit).all()
    livros_dict = [livro.to_dict() for livro in livros]  
    return jsonify(livros=livros_dict), 200

@app.route('/api/pessoas', methods=['GET'])
def api_listar_pessoas():
    '''Listar todas as pessoas como JSON com paginação'''
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    offset = (page - 1) * limit

    pessoas = Pessoa.query.offset(offset).limit(limit).all()
    pessoas_dict = [pessoa.to_dict() for pessoa in pessoas]
    return jsonify(pessoas=pessoas_dict), 200

@app.route('/api/livros', methods=['POST'])
def api_add_livro():
    '''Adicionar um novo livro via API'''
    data = request.json

    # Validação dos campos
    nome = data.get('nome')
    autor = data.get('autor')
    genero = data.get('genero')
    
    if not nome or not autor or not genero:
        return jsonify({'message': 'Nome, Autor e Gênero são obrigatórios!'}), 400
    
    status = data.get('status', True)

    novo_livro = Livro(nome=nome, autor=autor, genero=genero, status=status)
    db.session.add(novo_livro)
    db.session.commit()

    return jsonify({'message': 'Livro adicionado com sucesso!', 'livro': novo_livro.to_dict()}), 201

@app.route('/api/pessoas', methods=['POST'])
def api_add_pessoa():
    '''Adicionar uma nova pessoa via API'''
    data = request.json
    nome = data.get('nome')
    sala = data.get('sala')
    matricula = data.get('matricula')
    
    if not nome or not sala or not matricula:
        return jsonify({'message': 'Nome, Sala e Matrícula são obrigatórios!'}), 400
    
    role = data.get('role', 'Aluno')  # Papel padrão é 'Aluno'
    
    nova_pessoa = Pessoa(nome=nome, sala=sala, matricula=matricula, role=role)
    db.session.add(nova_pessoa)
    db.session.commit()

    return jsonify({'message': 'Pessoa adicionada com sucesso!', 'pessoa': nova_pessoa.to_dict()}), 201

@app.route('/api/livros/<int:id>', methods=['PUT'])
def api_update_livro(id):
    '''Atualizar um livro existente via API'''
    livro = Livro.query.get_or_404(id)
    data = request.json

    # Atualizando os campos
    livro.nome = data.get('nome', livro.nome)
    livro.autor = data.get('autor', livro.autor)
    livro.genero = data.get('genero', livro.genero)
    livro.status = data.get('status', livro.status)

    db.session.commit()
    
    # Retornando uma resposta adequada
    return jsonify({
        'message': 'Livro atualizado com sucesso!',
        'livro': {
            'id': livro.id,
            'nome': livro.nome,
            'autor': livro.autor,
            'genero': livro.genero,
            'status': livro.status
        }
    }), 200

@app.route('/api/pessoas/<int:id>', methods=['PUT'])
def api_update_pessoa(id):
    '''Atualizar uma pessoa existente via API'''
    pessoa = Pessoa.query.get_or_404(id)
    data = request.json

    pessoa.nome = data.get('nome', pessoa.nome)
    pessoa.sala = data.get('sala', pessoa.sala)
    pessoa.matricula = data.get('matricula', pessoa.matricula)
    pessoa.role = data.get('role', pessoa.role)

    db.session.commit()

    return jsonify({'message': 'Pessoa atualizada com sucesso!', 'pessoa': pessoa.to_dict()}), 200

@app.route('/api/livros/<int:id>', methods=['DELETE'])
def api_delete_livro(id):
    '''Excluir um livro via API'''
    livro = Livro.query.get(id)
    if not livro:
        return jsonify({'message': 'Livro não encontrado!'}), 404

    db.session.delete(livro)
    db.session.commit()

    return jsonify({'message': 'Livro excluído com sucesso!'}), 200

@app.route('/api/pessoas/<int:id>', methods=['DELETE'])
def api_delete_pessoa(id):
    '''Excluir uma pessoa via API'''
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return jsonify({'message': 'Pessoa não encontrada!'}), 404

    db.session.delete(pessoa)
    db.session.commit()

    return jsonify({'message': 'Pessoa excluída com sucesso!'}), 200


def import_xlsx_to_db(file_path):
    try:
        # Lê o arquivo .xlsx
        df = pd.read_excel(file_path)
        
        # Remove espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Remove colunas vazias ou desnecessárias
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Exibe os nomes das colunas para debug (apagar em produção)
        print("Colunas após remoção das 'Unnamed':", df.columns.tolist())
        
        # Renomeia as colunas para os nomes esperados pelo sistema
        df = df.rename(columns={
            'Nome': 'Titulo',       # Mapeia "Nome" para "Titulo"
            'Autor': 'Autor',
            'Genero': 'Genero'
        })
        
        # Exibe os nomes das colunas após renomeação para debug (apagar em produção)
        print("Colunas após renomeação:", df.columns.tolist())
        
        # Verifica se as colunas renomeadas estão presentes
        required_columns = ['Titulo', 'Autor', 'Genero']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colunas ausentes no arquivo: {', '.join(missing_columns)}")

        # Preenche valores NaN em colunas essenciais com valores padrão
        df['Titulo'] = df['Titulo'].fillna("Título desconhecido")
        df['Autor'] = df['Autor'].fillna("Desconhecido")
        df['Genero'] = df['Genero'].fillna("Gênero não especificado")

        # Converte os dados em objetos Livro para inserção no banco
        for _, row in df.iterrows():
            novo_livro = Livro(
                nome=row['Titulo'],
                autor=row['Autor'],
                genero=row['Genero'],
                status=False,          # Define status como False (não emprestado)
                emprestado_para=None   # Define emprestado_para como None
            )
            db.session.add(novo_livro)
        
        # Commit para salvar os registros no banco de dados
        db.session.commit()
        flash("Livros importados com sucesso!", "success")
    
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro ao importar arquivo: {e}")
        flash(f"Erro ao importar arquivo: {e}", "error")
    except Exception as e:
        # Reverte a transação e loga o erro
        db.session.rollback()
        logger.error(f"Erro ao importar arquivo: {e}")
        flash(f"Erro ao importar arquivo: {e}", "error")

# Rota de upload para processar o arquivo .xlsx
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('Nome do arquivo vazio', 'error')
        return redirect(request.url)
    
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        try:
            # Chama a função para importar o arquivo .xlsx para o banco de dados
            import_xlsx_to_db(file_path)
            flash('Arquivo importado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao importar arquivo: {e}', 'error')
        
        return redirect(url_for('listar_livros'))
    else:
        flash('Formato de arquivo inválido. Apenas .xlsx é suportado.', 'error')
        return redirect(request.url)

if __name__ == "__main__":
    with app.app_context():
        # Importe e crie as tabelas
        db.create_all()
        print("Tabelas criadas com sucesso!")
        print(f"Servidor rodando em http://{host}:{port}")

    serve(app, host='0.0.0.0', port=5000)