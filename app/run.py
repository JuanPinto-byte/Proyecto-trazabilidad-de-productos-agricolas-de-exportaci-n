from flask import Flask, redirect, url_for, request
from app.config import config
from app.extensions import db, jwt
from app.routes.auth import auth_bp
from app.routes.fincas import fincas_bp
from app.routes.lotes  import lotes_bp
from app.routes.bitacoras import bitacoras_bp
from app.routes.trazabilidad import trazabilidad_bp
from app.routes.agroquimicos import agroquimicos_bp

# Cargar todos los modelos (import side-effect) para evitar errores por relaciones string
import app.models  # noqa: F401

app = Flask(__name__)
app.config.from_object(config["development"])

@app.after_request
def add_no_cache_headers(response):
    # Deja que /static (CSS) sí pueda cachearse
    if request.path.startswith("/static/"):
        return response

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(fincas_bp)
app.register_blueprint(lotes_bp)
app.register_blueprint(bitacoras_bp)
app.register_blueprint(trazabilidad_bp)
app.register_blueprint(agroquimicos_bp)

# Ruta raíz → redirige al login
@app.route("/")
def index():
    
    return redirect(url_for("auth.login"))
    
# Crear tablas si no existen (útil en desarrollo)


if __name__ == "__main__":
    app.run(debug=True)