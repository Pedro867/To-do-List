from utils.database   import db
from datetime   import datetime, timezone
from sqlalchemy import func

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    __table_args__ = {'schema': 'public'}

    id                = db.Column(db.Integer, primary_key=True)
    id_usuario        = db.Column(db.Integer, db.ForeignKey('public.usuarios.id'), nullable=False)
    nome_tarefa       = db.Column(db.String(120), nullable=False)
    prioridade_tarefa = db.Column(db.Integer, default=2, nullable=False)
    data_tarefa       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    concluida         = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Tarefa {self.nome_tarefa}>'

    @classmethod
    def contar_por_prioridade(cls, id_usuario):
        """ Retorna um dicionário {prioridade: quantidade} para o usuário """
        resultados = cls.query.with_entities(
            cls.prioridade_tarefa,
            func.count(cls.id)
        ).filter_by(
            id_usuario=id_usuario,
            concluida=True
        ).group_by(
            cls.prioridade_tarefa
        ).order_by(
            cls.prioridade_tarefa.asc()
        ).all()
        return dict(resultados)

    @staticmethod
    def select_all_tarefa(id_usuario: int) -> list:
        list_tarefas = Tarefa.query\
                        .filter_by(id_usuario=id_usuario)\
                        .order_by(Tarefa.prioridade_tarefa)\
                        .all()
        return list_tarefas

    @staticmethod
    def select_one_tarefa(id_tarefa: int) -> Tarefa:
        tarefa = Tarefa.query.get(id_tarefa)
        return tarefa

    @staticmethod
    def insert_tarefa(
        id_usuario       : int,
        nome_tarefa      : str,
        prioridade_tarefa: int
    ):
        try:
            nova_tarefa = Tarefa(nome_tarefa=nome_tarefa, id_usuario=id_usuario, prioridade_tarefa=prioridade_tarefa)
            db.session.add(nova_tarefa)
            db.session.commit()
            return True, nova_tarefa

        except Exception as e:
            db.session.rollback()
            print(f"Erro ao inserir tarefa: {e}")
            return False, "Erro interno no banco de dados"

    @staticmethod
    def update_tarefa(
        id_tarefa        : int,
        nom_tarefa       : str  = None,
        prioridade_tarefa: str  = None,
        tarefa_concluida : bool = None
    ):
        try:
            tarefa = Tarefa.select_one_tarefa(id_tarefa)
            if nom_tarefa is not None:
                tarefa.nome_tarefa = nom_tarefa
            if prioridade_tarefa is not None:
                tarefa.prioridade_tarefa = prioridade_tarefa
            if tarefa_concluida is not None:
                tarefa.concluida = tarefa_concluida
            db.session.commit()
            return True, "ok"
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao editar tarefa: {e}")
            return False, "Erro interno no banco de dados"

    @staticmethod
    def delete_tarefa(id_tarefa: int):
        try:
            tarefa = Tarefa.select_one_tarefa(id_tarefa)
            db.session.delete(tarefa)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar tarefa: {e}")
            return False, "Erro interno no banco de dados"
