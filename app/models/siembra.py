from app.extensions import db
from datetime import datetime


class Siembra(db.Model):
    __tablename__ = 'siembras'

    id                    = db.Column(db.Integer, primary_key=True)
    lote_id               = db.Column(db.Integer, db.ForeignKey('lotes.id'),    nullable=False)
    cultivo_id            = db.Column(db.Integer, db.ForeignKey('cultivos.id'), nullable=False)
    semilla_id            = db.Column(db.Integer, db.ForeignKey('semillas.id'), nullable=False)
    fecha_siembra         = db.Column(db.Date, nullable=False)
    fecha_cosecha_estimada = db.Column(db.Date)   # calculada automáticamente con cultivo.ciclo_dias
    observaciones         = db.Column(db.Text)
    usuario_creacion_id   = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion        = db.Column(db.DateTime, default=datetime.utcnow)

    def calcular_fecha_cosecha(self):
        """Calcula la fecha estimada de cosecha basándose en el ciclo biológico del cultivo."""
        from datetime import timedelta
        if self.fecha_siembra and self.cultivo and self.cultivo.ciclo_dias:
            return self.fecha_siembra + timedelta(days=self.cultivo.ciclo_dias)
        return None

    def __repr__(self):
        return f'<Siembra lote={self.lote_id} cultivo={self.cultivo_id} fecha={self.fecha_siembra}>'