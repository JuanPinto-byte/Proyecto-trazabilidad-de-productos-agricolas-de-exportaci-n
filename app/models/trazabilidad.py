from app.extensions import db
from datetime import datetime


class Trazabilidad(db.Model):
    __tablename__ = 'trazabilidad'

    id                   = db.Column(db.Integer, primary_key=True)
    lote_id              = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False, unique=True)
    codigo_trazabilidad  = db.Column(db.String(100), unique=True, nullable=False)
    fecha_generacion     = db.Column(db.DateTime, default=datetime.utcnow)
    # Estados: 'GENERADO', 'EN_TRANSITO', 'EN_PUERTO', 'ENTREGADO', 'BLOQUEADO'
    estado               = db.Column(db.String(30))

    eventos = db.relationship(
        'TrazabilidadEvento',
        backref='trazabilidad',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Trazabilidad {self.codigo_trazabilidad} — {self.estado}>'


class TrazabilidadEvento(db.Model):
    __tablename__ = 'trazabilidad_eventos'

    id                = db.Column(db.Integer, primary_key=True)
    trazabilidad_id   = db.Column(db.Integer, db.ForeignKey('trazabilidad.id'), nullable=False)
    fecha_evento      = db.Column(db.DateTime, default=datetime.utcnow)
    estado            = db.Column(db.String(30), nullable=False)
    ubicacion_actual  = db.Column(db.String(150))
    transportista     = db.Column(db.String(120))
    vehiculo          = db.Column(db.String(120))
    origen            = db.Column(db.String(150))
    destino           = db.Column(db.String(150))
    observaciones     = db.Column(db.Text)

    def __repr__(self):
        return f'<TrazabilidadEvento traza={self.trazabilidad_id} estado={self.estado} fecha={self.fecha_evento}>'


class RecepcionAcopio(db.Model):
    __tablename__ = 'recepcion_acopio'

    id                    = db.Column(db.Integer, primary_key=True)
    lote_id               = db.Column(db.Integer, db.ForeignKey('lotes.id'),    nullable=False)
    fecha_recepcion       = db.Column(db.Date, nullable=False)
    cantidad_kg           = db.Column(db.Numeric(10, 2))
    temperatura_recepcion = db.Column(db.Numeric(5, 2))
    # Estado del producto al ingreso: 'BUENO', 'REGULAR', 'MALO'
    estado_producto       = db.Column(db.String(50))
    operario_id           = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones         = db.Column(db.Text)
    fecha_creacion        = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<RecepcionAcopio lote={self.lote_id} kg={self.cantidad_kg}>'


class Auditoria(db.Model):
    """Registro automático de todas las operaciones críticas del sistema."""
    __tablename__ = 'auditoria'

    id               = db.Column(db.Integer, primary_key=True)
    usuario_id       = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tabla_afectada   = db.Column(db.String(100))
    # Operación: 'INSERT', 'UPDATE', 'DELETE'
    tipo_operacion   = db.Column(db.String(30))
    registro_id      = db.Column(db.Integer)
    datos_anteriores = db.Column(db.JSON)
    datos_nuevos     = db.Column(db.JSON)
    fecha_operacion  = db.Column(db.DateTime, default=datetime.utcnow)
    direccion_ip     = db.Column(db.String(45))

    def __repr__(self):
        return f'<Auditoria {self.tipo_operacion} en {self.tabla_afectada} por usuario={self.usuario_id}>'