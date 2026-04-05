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