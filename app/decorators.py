"""
Decoradores centrales de autenticación y control de acceso.

Uso:
    from app.decorators import login_required, require_permiso

    @fincas_bp.route("/fincas")
    @login_required
    @require_permiso("ver", "fincas")
    def lista():
        ...
"""

from functools import wraps
from flask import session, flash, redirect, url_for, abort

from app.extensions import db
from app.models.usuarios.user import User


# ── helpers internos ──────────────────────────────────────────────────────────

def _usuario_tiene_permiso(user_id: int, accion: str, recurso: str) -> bool:
    """
    Consulta si el usuario tiene el permiso (accion, recurso) a través de su rol.
    Hace una sola consulta con JOIN para no cargar toda la relación en memoria.
    """
    from app.models.usuarios.permiso import Permiso
    from app.models.usuarios.rol import rol_permiso

    usuario = db.session.get(User, user_id)
    if not usuario or not usuario.rol:
        return False

    # Busca el permiso dentro de los permisos del rol del usuario
    for permiso in usuario.rol.permisos:
        if permiso.accion == accion and permiso.recurso == recurso:
            return True
    return False


# ── decoradores públicos ──────────────────────────────────────────────────────

def login_required(f):
    """Redirige al login si no hay sesión activa."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def require_permiso(accion: str, recurso: str):
    """
    Verifica que el usuario en sesión tenga el permiso (accion, recurso).
    Debe usarse DESPUÉS de @login_required.

    Ejemplo:
        @require_permiso("crear", "fincas")
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = session.get("user_id")
            if not user_id:
                flash("Debes iniciar sesión primero.", "warning")
                return redirect(url_for("auth.login"))

            if not _usuario_tiene_permiso(user_id, accion, recurso):
                flash(
                    f"No tienes permiso para {accion} en {recurso.replace('_', ' ')}.",
                    "error"
                )
                return redirect(url_for("auth.dashboard"))

            return f(*args, **kwargs)
        return decorated
    return decorator
