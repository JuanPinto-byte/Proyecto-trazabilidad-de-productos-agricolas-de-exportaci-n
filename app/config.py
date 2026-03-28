import os
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

class Config:
    """Configuración de la aplicación Flask"""

    # Clave secreta para seguridad (JWT, etc.)
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-temporal-super-secreta-2026')

    # Base de datos SQLite temporal (fácil para desarrollo)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    # Desactivamos esta opción para evitar warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave para JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-clave-temporal-diferente-2026')
