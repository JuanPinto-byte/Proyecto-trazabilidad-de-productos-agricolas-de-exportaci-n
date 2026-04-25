from app.extensions import db


rol_permiso = db.Table(
    'rol_permiso',
    db.Column(
        'rol_id',
        db.Integer,
        db.ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    ),
    db.Column(
        'permiso_id',
        db.Integer,
        db.ForeignKey('permisos.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    ),
)

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    permisos = db.relationship(
        'Permiso',
        secondary=rol_permiso,
        back_populates='roles',
        lazy='subquery',
    )
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'
