from app.extensions import db

class Cultivo(db.Model):
    __tablename__ = "cultivos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ciclo_dias = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)

    # Relación con Siembra
    siembras = db.relationship("Siembra", back_populates="cultivo")

    def __repr__(self):
        return f'<Cultivo {self.nombre}>'
