from app.extensions import db
from datetime import datetime


class Anomalia(db.Model):
    __tablename__ = 'anomalias'

    id                        = db.Column(db.Integer, primary_key=True)
    lote_id                   = db.Column(db.Integer, db.ForeignKey('lotes.id'),    nullable=False)
    descripcion               = db.Column(db.Text, nullable=False)
    # Gravedad: 'LEVE', 'MODERADA', 'GRAVE'
    gravedad                  = db.Column(db.String(20), nullable=False)
    # Estado: 'PENDIENTE', 'EN_REVISION', 'RESUELTA'
    estado                    = db.Column(db.String(20), default='PENDIENTE')
    fecha_deteccion = db.Column(
        db.Date,
        nullable=False,
        server_default=db.func.current_date(),
    )
    registrado_por_usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def esta_pendiente(self):
        return self.estado == 'PENDIENTE'

    def __repr__(self):
        return f'<Anomalia lote={self.lote_id} gravedad={self.gravedad} estado={self.estado}>'