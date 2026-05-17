from app.extensions import db

from .rol import rol_permiso


class Permiso(db.Model):
    __tablename__ = 'permisos'

    id = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(50), nullable=False)
    recurso = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('accion', 'recurso', name='uq_permiso'),
    )

    roles = db.relationship(
        'Rol',
        secondary=rol_permiso,
        back_populates='permisos',
        lazy='subquery',
    )

    def __repr__(self):
        return f'<Permiso {self.accion}:{self.recurso}>'
