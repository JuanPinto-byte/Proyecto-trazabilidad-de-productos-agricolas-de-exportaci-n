from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, nullable=False)           # FK hacia tabla roles (más adelante)
    telefono = db.Column(db.String(20), nullable=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.nombre_usuario} - {self.nombre_completo}>'