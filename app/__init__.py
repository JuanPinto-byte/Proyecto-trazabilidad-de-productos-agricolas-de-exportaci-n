from flask import Flask, session
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

    all_menu_items = {
        "dashboard",
        "fincas",
        "lotes",
        "siembras",
        "bitacoras",
        "trazabilidad",
        "agroquimicos",
        "recepciones",
        "clima",
        "despachos",
        "reportes",
        "usuarios",
    }

    role_menu_map = {
        "COORDINADOR": set(all_menu_items),
        "AGRONOMO": {
            "dashboard",
            "siembras",
            "bitacoras",
            "agroquimicos",
            "trazabilidad",
            "reportes",
        },
        "OPERARIO": {
            "dashboard",
            "recepciones",
            "reportes",
        },
        "INSPECTOR": {
            "dashboard",
            "agroquimicos",
            "trazabilidad",
            "reportes",
        },
    }

    @app.context_processor
    def inject_menu_by_role():
        rol = (session.get("rol") or "").upper()
        allowed = role_menu_map.get(rol, all_menu_items)
        menu = {key: key in allowed for key in all_menu_items}
        return {
            "menu": menu,
            "rol_actual": rol,
        }

    # Asegura que todos los modelos se registren antes de las rutas
    from app import models  # noqa: F401

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.fincas import fincas_bp
    from app.routes.lotes import lotes_bp
    from app.routes.bitacoras import bitacoras_bp
    from app.routes.trazabilidad import trazabilidad_bp
    from app.routes.agroquimicos import agroquimicos_bp
    from app.routes.reportes import reportes_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.recepciones import recepciones_bp
    from app.routes.siembras import siembras_bp
<<<<<<< HEAD
    from app.routes.cosechas import cosechas_bp
=======
    from app.routes.despachos import despachos_bp
    from app.routes.clima import clima_bp
>>>>>>> ad1d9ff02af2d859a660ef8bfd42fc0d34e10802

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(fincas_bp)
    app.register_blueprint(lotes_bp)
    app.register_blueprint(bitacoras_bp)
    app.register_blueprint(trazabilidad_bp)
    app.register_blueprint(agroquimicos_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(recepciones_bp)
    app.register_blueprint(siembras_bp)
<<<<<<< HEAD
    app.register_blueprint(cosechas_bp)
=======
    app.register_blueprint(despachos_bp)
    app.register_blueprint(clima_bp)
>>>>>>> ad1d9ff02af2d859a660ef8bfd42fc0d34e10802

    return app