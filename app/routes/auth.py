from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.rol import Rol
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# Ruta Login
@auth_bp.route('/login', methods=['GET',"POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Buscar en la tabla usuarios
        user = User.query.filter(
            (User.email == username) | (User.nombre_usuario == username)
        ).first()

        if not user:
            flash("Usuario no encontrado", "user_error")
            return redirect(url_for("auth.login"))
        
        if not check_password_hash(user.password_hash, password):
            flash("Contraseña incorrecta", "password_error")
            return redirect(url_for("auth.login"))
        
        # Login
        session["user_id"] = user.id
        session["username"] = user.nombre_usuario
        return redirect(url_for("auth.dashboard"))
      
    return render_template("login.html")

# Ruta register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        telefono = request.form.get('telefono')

        # 🔥 VALIDAR SI YA EXISTE
        user_exist = User.query.filter_by(nombre_usuario=username).first()
        email_exist = User.query.filter_by(email=email).first()
        
        if user_exist:
            flash("El nombre de usuario ya existe", "user_error")
            return redirect(url_for("auth.register"))

        if email_exist:
            flash("El correo electrónico ya está registrado", "email_error")
            return redirect(url_for("auth.register"))

        # CREAR USUARIO
        nuevo_usuario = User(
            nombre_usuario=username,
            nombre_completo=f"{nombre} {apellido}",
            email=email,
            telefono=telefono
        )

        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')

#Ruta Dashboard
@auth_bp.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")
