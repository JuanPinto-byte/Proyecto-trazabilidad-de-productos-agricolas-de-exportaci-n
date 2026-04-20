from app.extensions import db
from datetime import datetime


class Finca(db.Model):
    __tablename__ = 'fincas'

    id                        = db.Column(db.Integer, primary_key=True)
    nombre_finca              = db.Column(db.String(100), nullable=False)
    ubicacion                 = db.Column(db.String(150))
    coordenadas_gps           = db.Column(db.String(100))
    area_total_hectareas      = db.Column(db.Numeric(10, 2))
    area_cultivable_hectareas = db.Column(db.Numeric(10, 2))

    # FK → agricultores
    agricultor_id  = db.Column(db.Integer, db.ForeignKey('agricultores.id'), nullable=False)
    # FK → usuarios (responsable de la finca)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    estado              = db.Column(db.String(30))
    fecha_creacion      = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Un finca tiene muchos lotes
    lotes = db.relationship('Lote', backref='finca', lazy=True)

    def __repr__(self):
        return f'<Finca {self.nombre_finca}>'