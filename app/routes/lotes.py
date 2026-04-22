from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.lote import Lote
from app.models.finca import Finca
from app.models.user import User
from functools import wraps

lotes_bp = Blueprint("lotes", __name__)


# ── Protección de sesión ──────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


# ── LISTAR ────────────────────────────────────────────────────────────────────
@lotes_bp.route("/lotes")
@login_required
def lista():
    lotes = db.session.query(Lote, Finca.nombre_finca)\
        .join(Finca, Finca.id == Lote.finca_id)\
        .order_by(Lote.fecha_creacion.desc())\
        .all()
    return render_template("lotes/lista.html", lotes=lotes)


# ── CREAR ─────────────────────────────────────────────────────────────────────
@lotes_bp.route("/lotes/crear", methods=["GET", "POST"])
@login_required
def crear():
    fincas = Finca.query.filter_by(estado="ACTIVO").order_by(Finca.nombre_finca).all()

    if request.method == "POST":
        finca_id      = request.form.get("finca_id")
        numero_lote   = request.form.get("numero_lote", "").strip()
        descripcion   = request.form.get("descripcion", "").strip()
        area          = request.form.get("area_hectareas") or None
        estado        = request.form.get("estado", "ACTIVO")

        # Validaciones
        if not finca_id:
            flash("Debes seleccionar una finca.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)
        if not numero_lote:
            flash("El número de lote es obligatorio.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)
        finca = Finca.query.get(int(finca_id))
        area_valor = float(area)
        if area_valor > float(finca.area_total_hectareas):
            flash("El área del lote no puede ser mayor que el área de la finca.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        # Verificar que el número de lote no esté duplicado
        existe = Lote.query.filter_by(numero_lote=numero_lote).first()
        if existe:
            flash(f"El lote '{numero_lote}' ya existe.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        nuevo = Lote(
            finca_id            = int(finca_id),
            numero_lote         = numero_lote,
            descripcion         = descripcion,
            area_hectareas      = area,
            estado              = estado,
            usuario_creacion_id = session["user_id"],
        )
        db.session.add(nuevo)
        db.session.commit()
        flash(f"Lote '{numero_lote}' creado correctamente.", "success")
        return redirect(url_for("lotes.lista"))

    return render_template("lotes/form.html", fincas=fincas, lote=None)


# ── EDITAR ────────────────────────────────────────────────────────────────────
@lotes_bp.route("/lotes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    lote   = Lote.query.get_or_404(id)
    fincas = Finca.query.filter_by(estado="ACTIVO").order_by(Finca.nombre_finca).all()

    if request.method == "POST":
        lote.finca_id      = int(request.form.get("finca_id"))
        lote.numero_lote   = request.form.get("numero_lote", "").strip()
        lote.descripcion   = request.form.get("descripcion", "").strip()
        lote.area_hectareas = request.form.get("area_hectareas") or None
        lote.estado        = request.form.get("estado", "ACTIVO")

        if not lote.numero_lote:
            flash("El número de lote es obligatorio.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        db.session.commit()
        flash(f"Lote '{lote.numero_lote}' actualizado correctamente.", "success")
        return redirect(url_for("lotes.lista"))

    return render_template("lotes/form.html", fincas=fincas, lote=lote)


# ── BLOQUEAR / DESBLOQUEAR ────────────────────────────────────────────────────
@lotes_bp.route("/lotes/bloquear/<int:id>", methods=["POST"])
@login_required
def bloquear(id):
    lote = Lote.query.get_or_404(id)
    lote.estado = "BLOQUEADO"
    db.session.commit()
    flash(f"Lote '{lote.numero_lote}' bloqueado.", "warning")
    return redirect(url_for("lotes.lista"))


@lotes_bp.route("/lotes/desbloquear/<int:id>", methods=["POST"])
@login_required
def desbloquear(id):
    lote = Lote.query.get_or_404(id)
    lote.estado = "ACTIVO"
    db.session.commit()
    flash(f"Lote '{lote.numero_lote}' desbloqueado.", "success")
    return redirect(url_for("lotes.lista"))


# ── ELIMINAR ──────────────────────────────────────────────────────────────────
@lotes_bp.route("/lotes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    lote = Lote.query.get_or_404(id)

    if lote.cosechas or lote.siembras:
        flash(f"No se puede eliminar '{lote.numero_lote}' porque tiene siembras o cosechas asociadas.", "error")
        return redirect(url_for("lotes.lista"))

    numero = lote.numero_lote
    db.session.delete(lote)
    db.session.commit()
    flash(f"Lote '{numero}' eliminado correctamente.", "success")
    return redirect(url_for("lotes.lista"))