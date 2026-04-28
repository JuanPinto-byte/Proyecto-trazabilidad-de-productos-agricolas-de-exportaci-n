from flask import Flask
from flask_cors import CORS
from app.config import config
from app.extensions import db, jwt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["development"])

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Asegura que todos los modelos se registren (evita errores de relaciones por strings)
    # Nota: usar `from app import models` evita pisar la variable local `app` (Flask).
    from app import models  # noqa: F401

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.fincas import fincas_bp
    from app.routes.lotes import lotes_bp
    from app.routes.bitacoras import bitacoras_bp
    from app.routes.trazabilidad import trazabilidad_bp
    from app.routes.agroquimicos import agroquimicos_bp
    from app.routes.reportes import reportes_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(fincas_bp)
    app.register_blueprint(lotes_bp)
    app.register_blueprint(bitacoras_bp)
    app.register_blueprint(trazabilidad_bp)
    app.register_blueprint(agroquimicos_bp)
    app.register_blueprint(reportes_bp)

    return app