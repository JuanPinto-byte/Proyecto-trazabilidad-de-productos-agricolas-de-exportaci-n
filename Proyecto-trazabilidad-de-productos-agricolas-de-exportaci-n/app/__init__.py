from flask import Flask, render_template
from flask_cors import CORS
from app.config import Config
from app.extensions import db, jwt   # quitamos migrate temporalmente

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def home():
        return render_template('login.html')

    return app