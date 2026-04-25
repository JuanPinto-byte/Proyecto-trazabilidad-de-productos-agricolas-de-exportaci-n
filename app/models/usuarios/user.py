from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .rol import Rol  
from app.extensions import db

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )
    fecha_actualizacion = db.Column(db.DateTime, nullable=True)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)

    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    rol = db.relationship(Rol, backref='usuarios')

    # MÉTODOS DE SEGURIDAD
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        rol_nombre = self.rol.nombre if self.rol else 'sin_rol'
        return f'<User {self.nombre_usuario} ({rol_nombre})>'