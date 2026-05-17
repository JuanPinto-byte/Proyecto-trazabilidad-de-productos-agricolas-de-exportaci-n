from app.extensions import db
from datetime import datetime


class Agricultor(db.Model):
    __tablename__ = 'agricultores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(30), unique=True, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    departamento = db.Column(db.String(100), nullable=True)

    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    municipio_id = db.Column(db.Integer, db.ForeignKey('municipios.id'), nullable=True)

    municipio_ref = db.relationship('Municipio', foreign_keys=[municipio_id])

    # Un agricultor puede tener muchas fincas
    fincas = db.relationship('Finca', backref='agricultor', lazy=True)

    def __repr__(self):
        return f'<Agricultor {self.nombre}>'