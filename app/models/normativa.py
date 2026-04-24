from app.extensions import db
from datetime import datetime


class Normativa(db.Model):
    __tablename__ = 'normativas'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    activa      = db.Column(db.Boolean, default=True)

    inspecciones           = db.relationship('Inspeccion',           backref='normativa', lazy=True)
    cumplimientos          = db.relationship('CumplimientoNormativa', backref='normativa', lazy=True)

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
    fecha_creacion      = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CumplimientoNormativa lote={self.lote_id} cumple={self.cumple}>'