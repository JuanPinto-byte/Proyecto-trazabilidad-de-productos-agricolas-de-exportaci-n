from app.extensions import db
from datetime import datetime


class Agricultor(db.Model):
    __tablename__ = 'agricultores'

    id              = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(100), nullable=False)
    cedula          = db.Column(db.String(30), unique=True)
    telefono        = db.Column(db.String(20))
    email           = db.Column(db.String(100))
    fecha_creacion  = db.Column(db.DateTime, default=datetime.utcnow)

    # Un agricultor puede tener muchas fincas
    fincas = db.relationship('Finca', backref='agricultor', lazy=True)

    def __repr__(self):
        return f'<Agricultor {self.nombre}>'