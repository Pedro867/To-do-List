import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from models.user import User

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
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {
                'status': 'erro',
                'msg'   : 'E-mail não cadastrado.' 
            }, 401
        if not user.check_senha(senha):
            return {
                'status': 'erro',
                'msg'   : 'Senha incorreta.' 
            }, 401
        return render_template("base_logado.html", username = user.name)
    else:
        return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome           = request.form.get('name')
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
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return {
                'status': 'erro',
                'msg'   : 'Esse e-mail já está cadastrado.' 
            }, 400
        
        new_user = User(name=nome, email=email)
        new_user.set_senha(senha)

        try:
            db.session.add(new_user)
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
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)