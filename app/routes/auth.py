from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Ruta de prueba
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "✅ Auth blueprint funcionando"}), 200



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # 🔥 VALIDAR SI YA EXISTE
        user_exist = User.query.filter_by(nombre_usuario=username).first()
        email_exist = User.query.filter_by(email=email).first()

        if user_exist:
            return "❌ El nombre de usuario ya existe"

        if email_exist:
            return "❌ El correo ya está registrado"

        # CREAR USUARIO
        nuevo_usuario = User(
            nombre_usuario=username,
            nombre_completo=f"{nombre} {apellido}",
            email=email,
            rol_id=1
        )

        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect('/')

    return render_template('register.html')

from flask import request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash

@auth_bp.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(
        (User.email == username) | (User.nombre_usuario == username)
    ).first()

    if not user:
        return "❌ Usuario no encontrado"

    # 🔐 USAR TU MÉTODO
    if not user.check_password(password):
        return "❌ Contraseña incorrecta"

    return f"✅ Bienvenido {user.nombre_completo}"

    # 🔐 OPCIÓN SEGURA (si usas hash)
    if user.password_hash != password:
        return "❌ Contraseña incorrecta"

    # ✅ LOGIN OK
    return f"Bienvenido {user.nombre_usuario}"