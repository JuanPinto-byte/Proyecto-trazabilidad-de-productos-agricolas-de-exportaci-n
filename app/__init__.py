from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, jwt

def create_app():
    """Función factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(Config)
    
    # Habilitar CORS
    CORS(app)
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Ruta de prueba
    @app.route('/')
    def home():
        return {
            "message": "✅ Plataforma de Trazabilidad Agrícola - Backend funcionando",
            "status": "ok",
            "database": "trazabilidad_db"
        }
    
    print("🚀 Aplicación Flask inicializada correctamente")
    return app