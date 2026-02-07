from database import db
from datetime import datetime, timezone

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    
    id                = db.Column(db.Integer, primary_key=True)
    id_usuario        = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nome_tarefa       = db.Column(db.String(120), nullable=False)
    prioridade_tarefa = db.Column(db.Integer, default=2, nullable=False)
    data_tarefa       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    concluida         = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Tarefa {self.nome_tarefa}>'