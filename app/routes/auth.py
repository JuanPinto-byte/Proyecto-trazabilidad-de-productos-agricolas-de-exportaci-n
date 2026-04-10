from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User   # Lo crearemos después

auth_bp = Blueprint('auth', __name__)

# Ruta de prueba temporal (para que no dé error)
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "✅ Auth blueprint funcionando"}), 200