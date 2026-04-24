from app.extensions import db
from datetime import datetime


class Cultivo(db.Model):
    __tablename__ = 'cultivos'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100), nullable=False)
    ciclo_dias  = db.Column(db.Integer, nullable=False)   # días desde siembra hasta cosecha
    descripcion = db.Column(db.Text)

    # Un cultivo puede aparecer en muchas siembras
    siembras = db.relationship('Siembra', backref='cultivo', lazy=True)

    def __repr__(self):
        return f'<Cultivo {self.nombre} ({self.ciclo_dias} días)>'


class Semilla(db.Model):
    __tablename__ = 'semillas'

    id              = db.Column(db.Integer, primary_key=True)
    nombre_variedad = db.Column(db.String(100))
    especie         = db.Column(db.String(100))
    proveedor       = db.Column(db.String(100))
    dias_germinacion = db.Column(db.Integer)
    dias_cosecha     = db.Column(db.Integer)
    descripcion      = db.Column(db.Text)
    activo           = db.Column(db.Boolean, default=True)
    fecha_creacion   = db.Column(db.DateTime, default=datetime.utcnow)

    siembras = db.relationship('Siembra', backref='semilla', lazy=True)

    def __repr__(self):
        return f'<Semilla {self.nombre_variedad}>'