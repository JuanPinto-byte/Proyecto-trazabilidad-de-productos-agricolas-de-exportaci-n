from app.extensions import db
from datetime import datetime


class Finca(db.Model):
    __tablename__ = 'fincas'

    id                        = db.Column(db.Integer, primary_key=True)
    nombre_finca              = db.Column(db.String(100), nullable=False)
    municipio                 = db.Column(db.String(100))
    departamento              = db.Column(db.String(100))
    coordenadas_gps           = db.Column(db.String(100))
    area_total_hectareas      = db.Column(db.Numeric(10, 2))
    area_cultivable_hectareas = db.Column(db.Numeric(10, 2))

    agricultor_id  = db.Column(db.Integer, db.ForeignKey('agricultores.id'), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipios.id'), nullable=True)

    estado              = db.Column(db.String(30))
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )
    fecha_actualizacion = db.Column(db.DateTime, nullable=True)

    departamento_ref = db.relationship('Departamento', foreign_keys=[departamento_id])
    municipio_ref = db.relationship('Municipio', foreign_keys=[municipio_id])

    lotes = db.relationship('Lote', backref='finca', lazy=True)

    def __repr__(self):
        return f'<Finca {self.nombre_finca}>'