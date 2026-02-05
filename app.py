import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do .env

app = Flask(__name__, static_folder='static')

# Configurando app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from database import db
db.init_app(app) # Inicializa o BD

@app.route("/")
def index():
    return redirect(url_for('login'))
                    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Faz login"
    else:
        return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirmar_senha  ')

        # Validação simples
        if senha != confirma_senha:
            return "As senhas não coincidem!", 400
        
        # Aqui entrará a lógica para salvar no PostgreSQL
        return "Cadastrou"
    else:
        return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)