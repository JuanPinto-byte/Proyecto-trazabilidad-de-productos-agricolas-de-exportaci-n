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

    # Registrar blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.routes.trazabilidad import trazabilidad_bp
    app.register_blueprint(trazabilidad_bp)

    return app