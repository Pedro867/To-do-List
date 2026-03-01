import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from models.usuarios import Usuario
from models.tarefas import Tarefa

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

load_dotenv() # Carrega variáveis do .env

app = Flask(__name__, static_folder='static')

# Configurando app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from database import db
db.init_app(app) # Inicializa o BD

with app.app_context():
    db.create_all() # Fabrica as tabelas no banco


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            return {
                'status': 'erro',
                'msg'   : 'E-mail não cadastrado.' 
            }, 401
        
        if not usuario.check_senha(senha):
            return {
                'status': 'erro',
                'msg'   : 'Senha incorreta.' 
            }, 401
        
        session['id_usuario']   = usuario.id
        session['nome_usuario'] = usuario.nome
        
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome           = request.form.get('nome')
        email          = request.form.get('email')
        senha          = request.form.get('senha')
        confirma_senha = request.form.get('confirmar_senha')

        if not nome:
            return {
                'status': 'erro',
                'msg'   : 'O nome está vazio.' 
            }, 400
        
        if not email:
            return {
                'status': 'erro',
                'msg'   : 'O e-mail está vazio.' 
            }, 400
        
        if senha != confirma_senha:
            return {
                'status': 'erro',
                'msg'   : 'As senhas não coincidem.' 
            }, 400
        
        usuario_existe = Usuario.query.filter_by(email=email).first()
        if usuario_existe:
            return {
                'status': 'erro',
                'msg'   : 'Esse e-mail já está cadastrado.' 
            }, 400
        
        novo_usuario = Usuario(nome=nome, email=email, adm=False)
        novo_usuario.set_senha(senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'erro',
                'msg'   : f'Erro ao salvar: {e}.' 
            }, 500
                
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/tarefa/add", methods=['POST'])
@login_required
def adicionar_tarefa():
    if request.method == 'POST':
        nome_tarefa = request.form.get('nome_tarefa')
        id_usuario  = session['id_usuario']
        if nome_tarefa and id_usuario:
            nova_tarefa = Tarefa(nome_tarefa=nome_tarefa, id_usuario=id_usuario, prioridade_tarefa=2)
            db.session.add(nova_tarefa)
            db.session.commit()
    
    return redirect(url_for('dashboard'))


@app.route("/tarefa/edi/<int:id_tarefa>", methods=['POST'])
@login_required
def editar_tarefa(id_tarefa):
    novo_nome_tarefa       = request.form.get('nome')
    nova_prioridade_tarefa = int(request.form.get('prioridade'))
    tarefa                 = Tarefa.query.filter_by(id=id_tarefa).first()

    if not novo_nome_tarefa or not nova_prioridade_tarefa:
        return {
            'status': 'erro',
            'msg'   : 'Dados da tarefa não foram recebidos'
        }, 400

    if tarefa.id_usuario == session.get('id_usuario'):
        tarefa.nome_tarefa       = novo_nome_tarefa
        tarefa.prioridade_tarefa = nova_prioridade_tarefa
        db.session.commit()
    
    return redirect(url_for('dashboard'))


@app.route("/tarefa/del/<int:id_tarefa>", methods=['POST'])
@login_required
def deletar_tarefa(id_tarefa):
    tarefa = Tarefa.query.filter_by(id=id_tarefa).first()
    if tarefa.id_usuario == session.get('id_usuario'):
        db.session.delete(tarefa)
        db.session.commit()
    
    return redirect(url_for('dashboard'))


@app.route('/tarefa/concluir/<int:id_tarefa>', methods=['GET'])
@login_required
def concluir(id_tarefa):
    tarefa = Tarefa.query.get_or_404(id_tarefa)
    if tarefa.id_usuario == session.get('id_usuario'):
        tarefa.concluida = not tarefa.concluida
        db.session.commit()
        return '', 204
    return {
        'status': 'erro',
        'msg'   : 'Acesso não autorizado.'
    }, 403


@app.route("/dashboard")
@login_required
def dashboard():
    id_usuario = session.get('id_usuario')
    usuario    = Usuario.query.filter_by(id=id_usuario).first()
    if usuario.adm:
        list_usuarios = Usuario.query.all()
        return render_template(
            "dashboard_admin.html", 
            nome_usuario  = usuario.nome,
            list_usuarios = list_usuarios
        )
    else:
        list_tarefas = Tarefa.query.filter_by(id_usuario=id_usuario).order_by(Tarefa.prioridade_tarefa).all()
        return render_template(
            "dashboard.html", 
            nome_usuario    = usuario.nome,
            id_usuario      = usuario.id,
            list_tarefas    = list_tarefas,
            dict_prioridade = Tarefa.contar_por_prioridade(id_usuario),
            num_tarefas     = [t for t in list_tarefas if not t.concluida]
        )


@app.route("/perfil")
@login_required
def perfil():
    return render_template('perfil.html', nome_usuario = session['nome_usuario'])

@app.route("/perfil/editar_perfil", methods=['POST'])
@login_required
def editar_perfil():
    novo_nome  = request.form.get('nome_usuario')
    nova_senha = request.form.get('senha')
    usuario    = Usuario.query.get(session['id_usuario'])   

    if novo_nome:
        usuario.nome = novo_nome
        session['nome_usuario'] = novo_nome
    if nova_senha:
        usuario.senha = Usuario.set_senha(nova_senha)   
    db.session.commit()

    return render_template('perfil.html', nome_usuario = session['nome_usuario'])


if __name__ == '__main__':
    app.run(debug=True)