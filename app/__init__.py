from flask import Flask
from flask import render_template
from flask_cors import CORS
from app.config import config
from app.extensions import db, jwt
from app.routes.auth import auth_bp  

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
