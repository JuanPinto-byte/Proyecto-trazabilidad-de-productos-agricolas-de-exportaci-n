from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, jwt   # quitamos migrate temporalmente

def create_app():
    """Función factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(Config)
    
    # Habilitar CORS para el frontend
    CORS(app)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    
    # Registrar rutas (blueprints)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Ruta de prueba (homepage)
    @app.route('/')
    def home():
        return {
            "message": "✅ Plataforma de Trazabilidad Agrícola - Backend funcionando",
            "status": "ok",
            "database": str(db.engine.url)
        }
    
    print("🚀 Aplicación Flask inicializada correctamente")
    return app