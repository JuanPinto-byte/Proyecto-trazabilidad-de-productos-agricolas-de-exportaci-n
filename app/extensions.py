from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Instancias de las extensiones que usaremos en toda la app
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()