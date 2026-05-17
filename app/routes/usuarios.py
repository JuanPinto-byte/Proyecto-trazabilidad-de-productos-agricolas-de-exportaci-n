from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from app.extensions import db
from app.models.usuarios.user import User
from app.models.usuarios.rol import Rol
from app.decorators import login_required, require_permiso

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios")
@login_required
@require_permiso("ver", "usuarios")
def lista():
    usuarios = User.query.order_by(User.fecha_creacion.desc()).all()
    roles    = Rol.query.order_by(Rol.nombre).all()
    usuario_actual = db.session.get(User, session["user_id"])
    return render_template(
        "usuarios/lista.html",
        usuarios       = usuarios,
        roles          = roles,
        usuario_actual = usuario_actual,
    )


@usuarios_bp.route("/usuarios/<int:user_id>/rol", methods=["POST"])
@login_required
@require_permiso("editar", "usuarios")
def cambiar_rol(user_id):
    usuario = db.session.get(User, user_id)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("usuarios.lista"))

    # No permitir que el coordinador se cambie su propio rol
    if usuario.id == session["user_id"]:
        flash("No puedes cambiar tu propio rol.", "error")
        return redirect(url_for("usuarios.lista"))

    nuevo_rol_id = request.form.get("rol_id", type=int)
    rol = db.session.get(Rol, nuevo_rol_id)
    if not rol:
        flash("Rol no válido.", "error")
        return redirect(url_for("usuarios.lista"))

    usuario.rol_id             = rol.id
    usuario.fecha_actualizacion = datetime.utcnow()
    db.session.commit()

    flash(f"Rol de {usuario.nombre_completo or usuario.nombre_usuario} actualizado a {rol.nombre}.", "success")
    return redirect(url_for("usuarios.lista"))


@usuarios_bp.route("/usuarios/<int:user_id>/toggle", methods=["POST"])
@login_required
@require_permiso("editar", "usuarios")
def toggle_activo(user_id):
    usuario = db.session.get(User, user_id)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("usuarios.lista"))

    if usuario.id == session["user_id"]:
        flash("No puedes desactivar tu propia cuenta.", "error")
        return redirect(url_for("usuarios.lista"))

    usuario.activo              = not usuario.activo
    usuario.fecha_actualizacion = datetime.utcnow()
    db.session.commit()

    estado = "activado" if usuario.activo else "desactivado"
    flash(f"Usuario {usuario.nombre_completo or usuario.nombre_usuario} {estado}.", "success")
    return redirect(url_for("usuarios.lista"))
