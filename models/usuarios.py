from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios' # Nome da tabela no Postgres
    __table_args__ = {'schema': 'public'}

    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    adm        = db.Column(db.Boolean, default=False, nullable=False)

    tarefas = db.relationship('Tarefa', backref='autor', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)