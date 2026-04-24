from app.extensions import db
from datetime import datetime


class Bodega(db.Model):
    __tablename__ = 'bodegas'

    id                   = db.Column(db.Integer, primary_key=True)
    nombre               = db.Column(db.String(100), nullable=False)
    ubicacion            = db.Column(db.String(150))
    capacidad_maxima_kg  = db.Column(db.Numeric(10, 2))
    tipo_almacenamiento  = db.Column(db.String(50))
    temperatura_setpoint = db.Column(db.Numeric(5, 2))   # temperatura objetivo
    humedad_setpoint     = db.Column(db.Numeric(5, 2))
    responsable_id       = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    estado               = db.Column(db.String(30))
    fecha_creacion       = db.Column(db.DateTime, default=datetime.utcnow)

    # Registros históricos de temperatura
    registros_temperatura = db.relationship('ControlTemperatura', backref='bodega', lazy=True)
    almacenamientos       = db.relationship('Almacenamiento',     backref='bodega', lazy=True)

    def ultimo_registro(self):
        """Devuelve el registro de temperatura más reciente de esta bodega."""
        return (ControlTemperatura.query
                .filter_by(bodega_id=self.id)
                .order_by(ControlTemperatura.fecha_hora.desc())
                .first())

    def __repr__(self):
        return f'<Bodega {self.nombre}>'


class ControlTemperatura(db.Model):
    __tablename__ = 'control_temperaturas'

    id          = db.Column(db.Integer, primary_key=True)
    bodega_id   = db.Column(db.Integer, db.ForeignKey('bodegas.id'), nullable=False)
    fecha_hora  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperatura = db.Column(db.Numeric(5, 2))
    humedad     = db.Column(db.Numeric(5, 2))

    def __repr__(self):
        return f'<ControlTemperatura bodega={self.bodega_id} temp={self.temperatura}°C>'


class Almacenamiento(db.Model):
    __tablename__ = 'almacenamiento'

    id                   = db.Column(db.Integer, primary_key=True)
    lote_id              = db.Column(db.Integer, db.ForeignKey('lotes.id'),    nullable=False)
    bodega_id            = db.Column(db.Integer, db.ForeignKey('bodegas.id'),  nullable=False)
    cantidad_kg          = db.Column(db.Numeric(10, 2))
    # Estados: 'EN_BODEGA', 'DESPACHADO', 'RECHAZADO'
    estado               = db.Column(db.String(30))
    fecha_ingreso        = db.Column(db.Date)
    fecha_salida         = db.Column(db.Date)
    operario_id          = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones        = db.Column(db.Text)
    fecha_actualizacion  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Almacenamiento lote={self.lote_id} bodega={self.bodega_id}>'