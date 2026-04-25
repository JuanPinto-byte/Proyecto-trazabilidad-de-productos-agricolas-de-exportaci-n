from app.extensions import db
from datetime import datetime


class BitacoraCultivo(db.Model):
    __tablename__ = 'bitacoras_cultivo'

    id                      = db.Column(db.Integer, primary_key=True)
    lote_id                 = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False)
    fecha                   = db.Column(db.Date, nullable=False)
    tipo_actividad          = db.Column(db.String(50))
    actividades_realizadas  = db.Column(db.Text)
    insumos_utilizados      = db.Column(db.Text)
    temperatura_c           = db.Column(db.Numeric(5, 2))
    humedad_pct             = db.Column(db.Numeric(5, 2))
    precipitacion_mm        = db.Column(db.Numeric(6, 2))
    observaciones           = db.Column(db.Text)
    agronomo_id             = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    def __repr__(self):
        return f'<BitacoraCultivo lote={self.lote_id} fecha={self.fecha}>'

class CondicionMeteorologica(db.Model):
    __tablename__ = 'condiciones_meteorologicas'

    id                = db.Column(db.Integer, primary_key=True)
    lote_id           = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False)
    fecha             = db.Column(db.Date, nullable=False)
    temperatura       = db.Column(db.Numeric(5, 2))
    humedad           = db.Column(db.Numeric(5, 2))
    precipitacion_mm  = db.Column(db.Numeric(6, 2))
    observaciones     = db.Column(db.Text)

    def __repr__(self):
        return f'<CondicionMeteorologica lote={self.lote_id} fecha={self.fecha}>'