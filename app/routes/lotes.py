from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
import re
from decimal import Decimal, InvalidOperation

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.produccion.lote import Lote
from app.models.produccion.finca import Finca
from app.routes.trazabilidad import create_trazabilidad

lotes_bp = Blueprint("lotes", __name__)


ESTADOS_LOTE_VALIDOS = {"ACTIVO", "COSECHADO", "BLOQUEADO", "DESPACHADO"}
NUMERO_LOTE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\s\-_.\/]{1,49}$")


def _parse_decimal(
    value: str,
    *,
    field_label: str,
    required: bool = False,
    min_value: Decimal | None = None,
):
    raw = (value or "").strip()
    if not raw:
        if required:
            flash(f"{field_label} es obligatorio.", "error")
            return None, False
        return None, True

    raw = raw.replace(",", ".")
    try:
        parsed = Decimal(raw)
    except InvalidOperation:
        flash(f"{field_label} debe ser un número válido.", "error")
        return None, False

    if min_value is not None and parsed < min_value:
        flash(f"{field_label} no puede ser menor que {min_value}.", "error")
        return None, False
    return parsed, True


def _to_decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal("0")


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
    lotes = db.session.query(
    Lote,
    Finca.nombre_finca,
    Finca.departamento,
    Finca.municipio
    )\
    .join(Finca, Finca.id == Lote.finca_id)\
    .order_by(Lote.fecha_creacion.desc())\
    .all()
    return render_template("lotes/lista.html", lotes=lotes)
    

# ── CREAR ─────────────────────────────────────────────────────────────────────
@lotes_bp.route("/lotes/crear", methods=["GET", "POST"])
@login_required
def crear():
    fincas = (
        Finca.query.options(joinedload(Finca.departamento_ref), joinedload(Finca.municipio_ref))
        .filter_by(estado="ACTIVO")
        .order_by(Finca.nombre_finca)
        .all()
    )

    if request.method == "POST":
        finca_id = request.form.get("finca_id", type=int)
        numero_lote = (request.form.get("numero_lote") or "").strip()
        descripcion = (request.form.get("descripcion") or "").strip() or None
        estado = ((request.form.get("estado") or "ACTIVO").strip().upper())
        area, ok_area = _parse_decimal(
            request.form.get("area_hectareas"),
            field_label="Área (ha)",
            required=(estado == "ACTIVO"),
            min_value=Decimal("0.01"),
        )

        # Validaciones (profesionales)
        if not finca_id:
            flash("Debes seleccionar una finca.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        finca = (
            Finca.query.options(joinedload(Finca.lotes))
            .options(joinedload(Finca.departamento_ref), joinedload(Finca.municipio_ref))
            .get(finca_id)
        )
        if not finca or finca.estado != "ACTIVO":
            flash("La finca seleccionada no existe o está inactiva.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        if not numero_lote:
            flash("El número de lote es obligatorio.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)
        if len(numero_lote) > 50:
            flash("El número de lote no puede exceder 50 caracteres.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)
        if not NUMERO_LOTE_RE.match(numero_lote):
            flash(
                "Formato de número de lote inválido. Usa letras/números y solo estos símbolos: espacio, - _ . /",
                "error",
            )
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        if estado not in ESTADOS_LOTE_VALIDOS:
            flash("Estado de lote inválido.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        if not ok_area:
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        # Validación de área disponible SOLO para lotes ACTIVO.
        # Regla pedida: los BLOQUEADO no se suman al área ocupada.
        area_cultivable = _to_decimal(finca.area_cultivable_hectareas)
        if estado == "ACTIVO":
            if area_cultivable <= 0:
                flash(
                    "La finca no tiene área cultivable configurada; no se puede activar un lote.",
                    "error",
                )
                return render_template("lotes/form.html", fincas=fincas, lote=None)

            area_ocupada = sum(
                _to_decimal(l.area_hectareas)
                for l in finca.lotes
                if l.area_hectareas and (l.estado or "").upper() == "ACTIVO"
            )
            area_disponible = area_cultivable - area_ocupada
            if area is not None and area > area_disponible:
                flash(
                    f"El área del lote supera el área disponible de la finca ({area_disponible:.2f} ha).",
                    "error",
                )
                return render_template("lotes/form.html", fincas=fincas, lote=None)

        # Duplicado (por finca) — comparación case-insensitive
        existe = Lote.query.filter(
            func.lower(Lote.numero_lote) == numero_lote.lower(),
            Lote.finca_id == finca.id,
        ).first()
        if existe:
            flash(f"El lote '{numero_lote}' ya existe en la finca '{finca.nombre_finca}'.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=None)

        nuevo = Lote(
            finca_id=int(finca_id),
            numero_lote=numero_lote,
            descripcion=descripcion,
            area_hectareas=area,
            estado=estado,
            usuario_creacion_id=session["user_id"],
        )
        db.session.add(nuevo)
        db.session.commit()
        
        # Crear trazabilidad automáticamente para el nuevo lote
        create_trazabilidad(nuevo.id)
        
        flash(f"Lote '{numero_lote}' creado correctamente.", "success")
        return redirect(url_for("lotes.lista"))

    return render_template("lotes/form.html", fincas=fincas, lote=None)


# ── EDITAR ────────────────────────────────────────────────────────────────────
@lotes_bp.route("/lotes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    lote   = Lote.query.get_or_404(id)
    fincas = (
        Finca.query.options(joinedload(Finca.departamento_ref), joinedload(Finca.municipio_ref))
        .filter_by(estado="ACTIVO")
        .order_by(Finca.nombre_finca)
        .all()
    )
    
    if request.method == "POST":
        finca_id = request.form.get("finca_id", type=int)
        numero_lote = (request.form.get("numero_lote") or "").strip()
        descripcion = (request.form.get("descripcion") or "").strip() or None
        estado = ((request.form.get("estado") or "ACTIVO").strip().upper())
        area, ok_area = _parse_decimal(
            request.form.get("area_hectareas"),
            field_label="Área (ha)",
            required=(estado == "ACTIVO"),
            min_value=Decimal("0.01"),
        )

        if not finca_id:
            flash("Debes seleccionar una finca.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        finca = Finca.query.options(joinedload(Finca.lotes)).get(finca_id)
        if not finca or finca.estado != "ACTIVO":
            flash("La finca seleccionada no existe o está inactiva.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        if not numero_lote:
            flash("El número de lote es obligatorio.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)
        if len(numero_lote) > 50:
            flash("El número de lote no puede exceder 50 caracteres.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)
        if not NUMERO_LOTE_RE.match(numero_lote):
            flash(
                "Formato de número de lote inválido. Usa letras/números y solo estos símbolos: espacio, - _ . /",
                "error",
            )
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        if estado not in ESTADOS_LOTE_VALIDOS:
            flash("Estado de lote inválido.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        if not ok_area:
            # Mantener valores en memoria para re-render
            lote.finca_id = finca_id
            lote.numero_lote = numero_lote
            lote.descripcion = descripcion
            lote.estado = estado
            lote.area_hectareas = area
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        # Regla pedida: si está BLOQUEADO, NO validar contra área disponible (permite editar finca “llena”).
        if estado == "ACTIVO":
            area_cultivable = _to_decimal(finca.area_cultivable_hectareas)
            if area_cultivable <= 0:
                flash(
                    "La finca no tiene área cultivable configurada; no se puede activar un lote.",
                    "error",
                )
                return render_template("lotes/form.html", fincas=fincas, lote=lote)

            area_ocupada = sum(
                _to_decimal(l.area_hectareas)
                for l in finca.lotes
                if l.area_hectareas
                and (l.estado or "").upper() == "ACTIVO"
                and l.id != lote.id
            )
            area_disponible = area_cultivable - area_ocupada
            if area is not None and area > area_disponible:
                flash(
                    f"El área del lote supera el área disponible de la finca ({area_disponible:.2f} ha).",
                    "error",
                )
                return render_template("lotes/form.html", fincas=fincas, lote=lote)

        # Duplicados en la misma finca (case-insensitive)
        existe = Lote.query.filter(
            func.lower(Lote.numero_lote) == numero_lote.lower(),
            Lote.finca_id == finca_id,
            Lote.id != lote.id,
        ).first()
        if existe:
            flash(f"El lote '{numero_lote}' ya existe en la finca '{finca.nombre_finca}'.", "error")
            return render_template("lotes/form.html", fincas=fincas, lote=lote)

        lote.finca_id = finca_id
        lote.numero_lote = numero_lote
        lote.descripcion = descripcion
        lote.area_hectareas = area
        lote.estado = estado

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
    finca = lote.finca

    # Para quedar ACTIVO, debe tener área válida y no superar el área disponible.
    if not lote.area_hectareas or _to_decimal(lote.area_hectareas) <= 0:
        flash(
            f"No se puede desbloquear el lote '{lote.numero_lote}' porque no tiene un área válida. Edita el lote y asigna el área.",
            "error",
        )
        return redirect(url_for("lotes.lista"))

    area_cultivable = _to_decimal(finca.area_cultivable_hectareas)
    if area_cultivable <= 0:
        flash(
            f"No se puede desbloquear el lote '{lote.numero_lote}' porque la finca no tiene área cultivable configurada.",
            "error",
        )
        return redirect(url_for("lotes.lista"))

    # Área ocupada actual (solo lotes ACTIVO). Regla pedida: BLOQUEADO no se suma.
    area_ocupada = sum(
        _to_decimal(l.area_hectareas)
        for l in finca.lotes
        if l.area_hectareas and (l.estado or "").upper() == "ACTIVO"
    )
    area_disponible = area_cultivable - area_ocupada

    if _to_decimal(lote.area_hectareas) > area_disponible:
        flash(
            f"No se puede desbloquear el lote '{lote.numero_lote}' porque supera el área disponible ({area_disponible:.2f} ha).",
            "error",
        )
        return redirect(url_for("lotes.lista"))

    # Si no excede, se desbloquea normalmente
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
    if lote.trazabilidad:
        flash(f"No se puede eliminar '{lote.numero_lote}' porque tiene trazabilidades asociadas.", "error")
        return redirect(url_for("lotes.lista"))
    if lote.bitacoras:
        flash(f"No se puede eliminar '{lote.numero_lote}' porque tiene bitácoras asociadas.", "error")
        return redirect(url_for("lotes.lista"))

    numero = lote.numero_lote
    db.session.delete(lote)
    db.session.commit()
    flash(f"Lote '{numero}' eliminado correctamente.", "success")
    return redirect(url_for("lotes.lista"))