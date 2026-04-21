from flask import Flask, redirect, url_for
from app.config import config
from app.extensions import db, jwt
from app.routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(config["development"])

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

# Ruta raíz → redirige al login
@app.route("/")
def index():
    return redirect(url_for("auth.login"))

# Crear tablas si no existen (útil en desarrollo)
with app.app_context():
    # Importar todos los modelos para que SQLAlchemy los registre
    from app.models import (
        User, Rol,
        Agricultor, Finca,
        Cultivo, Semilla,
        Lote, Siembra, Cosecha,
        Agroquimico, AplicacionAgroquimico,
        Bodega, ControlTemperatura, Almacenamiento,
        Anomalia, BitacoraCultivo, CondicionMeteorologica,
        Normativa, Inspeccion, CumplimientoNormativa,
        Trazabilidad, RecepcionAcopio, Auditoria
    )


if __name__ == "__main__":
    app.run(debug=True)