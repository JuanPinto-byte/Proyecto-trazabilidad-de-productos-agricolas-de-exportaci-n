from app.extensions import db
from datetime import datetime


class Lote(db.Model):
    __tablename__ = 'lotes'

    __table_args__ = (
        db.UniqueConstraint('finca_id', 'numero_lote', name='uq_lote_por_finca'),
    )

    id             = db.Column(db.Integer, primary_key=True)
    finca_id       = db.Column(db.Integer, db.ForeignKey('fincas.id'), nullable=False)
    numero_lote    = db.Column(db.String(50))
    descripcion    = db.Column(db.Text)
    area_hectareas = db.Column(db.Numeric(10, 2))

    # Estados posibles: ACTIVO, COSECHADO, BLOQUEADO, DESPACHADO
    estado = db.Column(db.String(30))

    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

    # FK → usuario que creó el lote
    usuario_creacion_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    # Relaciones
    siembras        = db.relationship('Siembra',       backref='lote', lazy=True)
    cosechas        = db.relationship('Cosecha',       backref='lote', lazy=True)
    anomalias       = db.relationship('Anomalia',      backref='lote', lazy=True)
    bitacoras       = db.relationship('BitacoraCultivo', backref='lote', lazy=True)
    almacenamientos = db.relationship('Almacenamiento', backref='lote', lazy=True)
    trazabilidad    = db.relationship('Trazabilidad',  backref='lote', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Lote {self.numero_lote} — {self.estado}>'