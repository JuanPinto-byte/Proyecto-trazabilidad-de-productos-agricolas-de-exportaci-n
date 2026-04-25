from app.extensions import db


class Semilla(db.Model):
    __tablename__ = "semillas"

    id = db.Column(db.Integer, primary_key=True)
    nombre_variedad = db.Column(db.String(100), nullable=True)
    especie = db.Column(db.String(100))
    proveedor = db.Column(db.String(100))
    dias_germinacion = db.Column(db.Integer)
    dias_cosecha = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, server_default='1', nullable=True)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    # Relación con Siembra
    siembras = db.relationship("Siembra", back_populates="semilla")

    def __repr__(self):
        return f'<Semilla {self.nombre_variedad}>'
