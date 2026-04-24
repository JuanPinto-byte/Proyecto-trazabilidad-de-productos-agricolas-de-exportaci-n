from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.finca import Finca
from app.models.agricultor import Agricultor
from app.models.user import User
from functools import wraps
from sqlalchemy import func

fincas_bp = Blueprint("fincas", __name__)


# ── Protección de sesión ──────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


# ── LISTAR ───────────────────────────────────────────────────────────────────
@fincas_bp.route("/fincas")
@login_required
def lista():
    fincas = db.session.query(Finca, Agricultor.nombre.label("agricultor_nombre"))\
        .join(Agricultor, Agricultor.id == Finca.agricultor_id)\
        .order_by(Finca.fecha_creacion.desc())\
        .all()
    return render_template("fincas/lista.html", fincas=fincas)


# ── CREAR ─────────────────────────────────────────────────────────────────────
@fincas_bp.route("/fincas/crear", methods=["GET", "POST"])
@login_required
def crear():
    agricultores = Agricultor.query.order_by(Agricultor.nombre).all()
    usuarios     = User.query.filter_by(activo=True).order_by(User.nombre_completo).all()

    if request.method == "POST":
        nombre       = request.form.get("nombre_finca", "").strip()
        ubicacion    = request.form.get("ubicacion", "").strip()
        coordenadas  = request.form.get("coordenadas_gps", "").strip()
        area_total   = request.form.get("area_total_hectareas") or None
        area_cultiv  = request.form.get("area_cultivable_hectareas") or None
        agricultor_id = request.form.get("agricultor_id")
        responsable_id = request.form.get("responsable_id") or None
        estado       = request.form.get("estado", "ACTIVO")

        # Validaciones básicas
        if not nombre:
            flash("El nombre de la finca es obligatorio.", "error")
            return render_template("fincas/form.html",
                                   agricultores=agricultores,
                                   usuarios=usuarios, finca=None)
        if area_cultiv>area_total:
            flash("El area cultivable no puede ser mas grande que area total.", "error")
            return render_template("fincas/form.html",
                                   agricultores=agricultores,
                                   usuarios=usuarios, finca=None)
        if not area_cultiv:
            flash("El Area Cultivable es obligatorio.", "error")
            return render_template("fincas/form.html",
                                   agricultores=agricultores,
                                   usuarios=usuarios, finca=None)
        if not agricultor_id:
            flash("Debes seleccionar un agricultor.", "error")
            return render_template("fincas/form.html",
                                   agricultores=agricultores,
                                   usuarios=usuarios, finca=None)
        
        nombre = request.form.get("nombre_finca", "").strip().lower()
        existe = Finca.query.filter(
            Finca.nombre_finca.ilike(nombre)   # compara sin importar mayúsculas
            ).first()

        if existe:
            flash(f"La '{nombre}' ya existe.", "error")
            return render_template("fincas/form.html", agricultores=agricultores, usuarios=usuarios, finca=None)

        nueva = Finca(
            nombre_finca              = nombre,
            ubicacion                 = ubicacion,
            coordenadas_gps           = coordenadas,
            area_total_hectareas      = area_total,
            area_cultivable_hectareas = area_cultiv,
            agricultor_id             = int(agricultor_id),
            responsable_id            = int(responsable_id) if responsable_id else None,
            estado                    = estado,
        )
        db.session.add(nueva)
        db.session.commit()
        flash(f"Finca '{nombre}' creada correctamente.", "success")
        return redirect(url_for("fincas.lista"))

    return render_template("fincas/form.html",
                           agricultores=agricultores,
                           usuarios=usuarios, finca=None)


# ── EDITAR ────────────────────────────────────────────────────────────────────
@fincas_bp.route("/fincas/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    finca        = Finca.query.get_or_404(id)
    agricultores = Agricultor.query.order_by(Agricultor.nombre).all()
    usuarios     = User.query.filter_by(activo=True).order_by(User.nombre_completo).all()

    if request.method == "POST":
        finca.nombre_finca              = request.form.get("nombre_finca", "").strip()
        finca.ubicacion                 = request.form.get("ubicacion", "").strip()
        finca.coordenadas_gps           = request.form.get("coordenadas_gps", "").strip()
        finca.area_total_hectareas      = request.form.get("area_total_hectareas") or None
        finca.area_cultivable_hectareas = request.form.get("area_cultivable_hectareas") or None
        finca.agricultor_id             = int(request.form.get("agricultor_id"))
        finca.responsable_id            = int(request.form.get("responsable_id")) if request.form.get("responsable_id") else None
        finca.estado                    = request.form.get("estado", "ACTIVO")

        if not finca.nombre_finca:
            flash("El nombre de la finca es obligatorio.", "error")
            return render_template("fincas/form.html",
                                   agricultores=agricultores,
                                   usuarios=usuarios, finca=finca)
        nombre = request.form.get("nombre_finca", "").strip().lower()
        # Obtener y convertir datos correctamente
        area_total = float(request.form.get("area_total_hectareas") or 0)
        area_cultivable = float(request.form.get("area_cultivable_hectareas") or 0)

        # Asignar ya como números
        finca.area_total_hectareas = area_total
        finca.area_cultivable_hectareas = area_cultivable

        # Validación correcta
        if area_cultivable > area_total:
            flash("El area cultivable no puede ser mayor que el area total.", "error")
            return render_template(
            "fincas/form.html",
            agricultores=agricultores,
            usuarios=usuarios,
            finca=finca   
    )
# Validar que no exista otra finca con el mismo nombre (case-insensitive),
# excluyendo la finca que estás editando
        existe = Finca.query.filter(
        func.lower(Finca.nombre_finca) == nombre,
            Finca.id != finca.id
            ).first()

        if existe:
            flash(f"La finca '{nombre}' ya existe.", "error")
            return render_template("fincas/form.html",
                           agricultores=agricultores,
                           usuarios=usuarios, finca=finca)
        db.session.commit()
        flash(f"La '{finca.nombre_finca}' actualizada correctamente.", "success")
        return redirect(url_for("fincas.lista"))

    return render_template("fincas/form.html",
                           agricultores=agricultores,
                           usuarios=usuarios, finca=finca)


# ── ELIMINAR ──────────────────────────────────────────────────────────────────
@fincas_bp.route("/fincas/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    finca = Finca.query.get_or_404(id)

    # Verificar si tiene lotes asociados antes de eliminar
    if finca.lotes:
        flash(f"No se puede eliminar '{finca.nombre_finca}' porque tiene lotes asociados.", "error")
        return redirect(url_for("fincas.lista"))

    nombre = finca.nombre_finca
    db.session.delete(finca)
    db.session.commit()
    flash(f"Finca '{nombre}' eliminada correctamente.", "success")
    return redirect(url_for("fincas.lista"))