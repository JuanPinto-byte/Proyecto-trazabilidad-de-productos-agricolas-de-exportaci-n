from app.extensions import db
from datetime import datetime


class Agroquimico(db.Model):
    __tablename__ = 'agroquimicos'

    id                    = db.Column(db.Integer, primary_key=True)
    nombre_producto       = db.Column(db.String(100), nullable=False)
    # tipo: 'FERTILIZANTE', 'PESTICIDA', 'FUNGICIDA', etc.
    tipo                  = db.Column(db.String(50))
    dosis_recomendada     = db.Column(db.Numeric(10, 2))
    dosis_limite_hectarea = db.Column(db.Numeric(10, 2))
    unidad_dosis          = db.Column(db.String(20))
    periodo_carencia_dias = db.Column(db.Integer)    # días que deben pasar antes de cosechar
    ficha_tecnica_url     = db.Column(db.String(255))
    activo                = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    aplicaciones = db.relationship('AplicacionAgroquimico', backref='agroquimico', lazy=True)

    def __repr__(self):
        return f'<Agroquimico {self.nombre_producto} ({self.tipo})>'


class AplicacionAgroquimico(db.Model):
    __tablename__ = 'aplicaciones_agroquimicos'

    id                = db.Column(db.Integer, primary_key=True)
    lote_id           = db.Column(db.Integer, db.ForeignKey('lotes.id'),        nullable=False)
    agroquimico_id    = db.Column(db.Integer, db.ForeignKey('agroquimicos.id'), nullable=False)
    fecha_aplicacion  = db.Column(db.Date, nullable=False)
    dosis_aplicada    = db.Column(db.Numeric(10, 2))
    unidad_dosis      = db.Column(db.String(20))
    observaciones     = db.Column(db.Text)
    usuario_id        = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AplicacionAgroquimico lote={self.lote_id} producto={self.agroquimico_id}>'