from app.extensions import db
from datetime import datetime


class Cosecha(db.Model):
    __tablename__ = 'cosechas'

    id                = db.Column(db.Integer, primary_key=True)
    lote_id           = db.Column(db.Integer, db.ForeignKey('lotes.id'),    nullable=False)
    fecha_cosecha     = db.Column(db.Date, nullable=False)
    cantidad_total_kg = db.Column(db.Numeric(10, 2))
    observaciones     = db.Column(db.Text)
    usuario_id        = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    def __repr__(self):
        return f'<Cosecha lote={self.lote_id} kg={self.cantidad_total_kg}>'
    