from app.extensions import db
from datetime import datetime


class Normativa(db.Model):
    __tablename__ = 'normativas'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    organismo_emisor = db.Column(db.String(100))
    mercado_destino = db.Column(db.String(100))
    version = db.Column(db.String(20))
    fecha_vigencia = db.Column(db.Date)
    activa      = db.Column(db.Boolean, default=True)

    inspecciones           = db.relationship('Inspeccion',           backref='normativa', lazy=True)
    cumplimientos          = db.relationship('CumplimientoNormativa', backref='normativa', lazy=True)
    certificaciones        = db.relationship('Certificacion',        backref='normativa', lazy=True)

    def __repr__(self):
        return f'<Normativa {self.nombre}>'


class Inspeccion(db.Model):
    __tablename__ = 'inspecciones'

    id            = db.Column(db.Integer, primary_key=True)
    lote_id       = db.Column(db.Integer, db.ForeignKey('lotes.id'),      nullable=False)
    normativa_id  = db.Column(db.Integer, db.ForeignKey('normativas.id'), nullable=False)
    fecha         = db.Column(db.Date, nullable=False)
    resultado     = db.Column(db.Boolean)     # True = aprobado, False = rechazado
    observaciones = db.Column(db.Text)
    inspector_id  = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __repr__(self):
        return f'<Inspeccion lote={self.lote_id} resultado={self.resultado}>'


class CumplimientoNormativa(db.Model):
    __tablename__ = 'cumplimiento_normativas'

    id                  = db.Column(db.Integer, primary_key=True)
    lote_id             = db.Column(db.Integer, db.ForeignKey('lotes.id'),      nullable=False)
    normativa_id        = db.Column(db.Integer, db.ForeignKey('normativas.id'), nullable=False)
    fecha_verificacion  = db.Column(db.Date)
    cumple              = db.Column(db.Boolean)
    observaciones       = db.Column(db.Text)
    inspector_id        = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    def __repr__(self):
        return f'<CumplimientoNormativa lote={self.lote_id} cumple={self.cumple}>'


class Certificacion(db.Model):
    __tablename__ = 'certificaciones'

    id = db.Column(db.Integer, primary_key=True)
    lote_id = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False)
    normativa_id = db.Column(db.Integer, db.ForeignKey('normativas.id'), nullable=False)

    entidad_certificadora = db.Column(db.String(100))
    numero_certificado = db.Column(db.String(100))
    fecha_emision = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    estado = db.Column(db.String(30), server_default='PENDIENTE', nullable=True)
    observaciones = db.Column(db.Text)

    inspector_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    def __repr__(self):
        return f'<Certificacion lote={self.lote_id} estado={self.estado}>'