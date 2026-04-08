from utils.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from .tarefas import Tarefa

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

    @staticmethod
    def select_all_users(listar_adm: bool = True) -> list:
        list_users = Usuario.query\
                    .filter_by(adm=listar_adm)\
                    .outerjoin(Tarefa)\
                    .group_by(Usuario.id)\
                    .order_by(func.count(Tarefa.id).desc())\
                    .all()
        return list_users

    @staticmethod
    def select_one_user(
        id_usuario: int = None,
        email     : str = None
    ) -> Usuario:
        query = Usuario.query

        if id_usuario:
            query = query.filter(Usuario.id == id_usuario)
        elif email:
            query = query.filter(Usuario.email == email)
        else:
            return None

        return query.first()

    @staticmethod
    def insert_usuario(
        nome : str,
        email: str,
        senha: str
    ):
        try:
            novo_usuario = Usuario(nome=nome, email=email, adm=False)
            novo_usuario.set_senha(senha)
            db.session.add(novo_usuario)
            db.session.commit()
            return {'status': 'ok'}
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'erro',
                'msg'   : f'Erro ao salvar: {e}.'
            }