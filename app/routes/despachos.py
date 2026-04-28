from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from datetime import datetime, date

from app.extensions import db
from app.models.trazabilidad.trazabilidad import Despacho, Trazabilidad
from app.models.produccion.lote import Lote
from app.models.produccion.finca import Finca

despachos_bp = Blueprint("despachos", __name__, url_prefix="/despachos")

ESTADOS = ["PROGRAMADO", "EN_TRANSITO", "EN_PUERTO", "ENTREGADO", "CANCELADO"]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@despachos_bp.route("/")
@login_required
def lista():
    filas = (
        db.session.query(Despacho, Lote.numero_lote, Finca.nombre_finca, Trazabilidad.codigo_trazabilidad)
        .join(Lote, Lote.id == Despacho.lote_id)
        .join(Finca, Finca.id == Lote.finca_id)
        .outerjoin(Trazabilidad, Trazabilidad.lote_id == Lote.id)
        .order_by(Despacho.fecha_despacho.desc())
        .all()
    )
    return render_template("despachos/lista.html", filas=filas, estados=ESTADOS)


@despachos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def crear():
    # Solo lotes cosechados o despachados pueden tener despacho
    lotes = (
        db.session.query(Lote, Finca.nombre_finca)
        .join(Finca, Finca.id == Lote.finca_id)
        .filter(Lote.estado.in_(["COSECHADO", "ACTIVO", "DESPACHADO"]))
        .order_by(Finca.nombre_finca, Lote.numero_lote)
        .all()
    )

    if request.method == "POST":
        lote_id = request.form.get("lote_id", "").strip()
        codigo_contenedor = request.form.get("codigo_contenedor", "").strip()
        fecha_despacho_str = request.form.get("fecha_despacho", "").strip()
        puerto_destino = request.form.get("puerto_destino", "").strip()
        pais_destino = request.form.get("pais_destino", "").strip()
        ubicacion_actual = request.form.get("ubicacion_actual", "").strip()
        fecha_llegada_str = request.form.get("fecha_estimada_llegada", "").strip()
        estado = request.form.get("estado", "PROGRAMADO").strip()
        observaciones = request.form.get("observaciones", "").strip()

        # Validaciones básicas
        if not lote_id:
            flash("Debes seleccionar un lote.", "error")
            return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=None)
        if not puerto_destino:
            flash("El puerto de destino es obligatorio.", "error")
            return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=None)
        if not pais_destino:
            flash("El país de destino es obligatorio.", "error")
            return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=None)

        # Parsear fechas
        fecha_despacho = None
        if fecha_despacho_str:
            try:
                fecha_despacho = date.fromisoformat(fecha_despacho_str)
            except ValueError:
                flash("Formato de fecha de despacho inválido.", "error")
                return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=None)

        fecha_llegada = None
        if fecha_llegada_str:
            try:
                fecha_llegada = date.fromisoformat(fecha_llegada_str)
            except ValueError:
                flash("Formato de fecha estimada de llegada inválido.", "error")
                return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=None)

        despacho = Despacho(
            lote_id=int(lote_id),
            codigo_contenedor=codigo_contenedor or None,
            fecha_despacho=fecha_despacho,
            puerto_destino=puerto_destino,
            pais_destino=pais_destino,
            ubicacion_actual=ubicacion_actual or None,
            fecha_estimada_llegada=fecha_llegada,
            estado=estado,
            observaciones=observaciones or None,
            operario_id=session.get("user_id"),
            fecha_creacion=datetime.utcnow(),
        )
        db.session.add(despacho)

        # Sincronizar estado en trazabilidad si corresponde
        traza = Trazabilidad.query.filter_by(lote_id=int(lote_id)).first()
        if traza and estado in ("EN_TRANSITO", "EN_PUERTO", "ENTREGADO"):
            traza.estado = estado

        db.session.commit()
        flash("Despacho registrado correctamente.", "success")
        return redirect(url_for("despachos.lista"))

    return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=None)


@despachos_bp.route("/<int:despacho_id>/editar", methods=["GET", "POST"])
@login_required
def editar(despacho_id):
    despacho = Despacho.query.get_or_404(despacho_id)
    lotes = (
        db.session.query(Lote, Finca.nombre_finca)
        .join(Finca, Finca.id == Lote.finca_id)
        .filter(Lote.estado.in_(["COSECHADO", "ACTIVO", "DESPACHADO"]))
        .order_by(Finca.nombre_finca, Lote.numero_lote)
        .all()
    )

    if request.method == "POST":
        despacho.codigo_contenedor = request.form.get("codigo_contenedor", "").strip() or None
        despacho.puerto_destino = request.form.get("puerto_destino", "").strip()
        despacho.pais_destino = request.form.get("pais_destino", "").strip()
        despacho.ubicacion_actual = request.form.get("ubicacion_actual", "").strip() or None
        despacho.observaciones = request.form.get("observaciones", "").strip() or None
        nuevo_estado = request.form.get("estado", despacho.estado)
        despacho.estado = nuevo_estado
        despacho.fecha_actualizacion = datetime.utcnow()

        fecha_despacho_str = request.form.get("fecha_despacho", "").strip()
        if fecha_despacho_str:
            try:
                despacho.fecha_despacho = date.fromisoformat(fecha_despacho_str)
            except ValueError:
                flash("Formato de fecha de despacho inválido.", "error")
                return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=despacho)

        fecha_llegada_str = request.form.get("fecha_estimada_llegada", "").strip()
        if fecha_llegada_str:
            try:
                despacho.fecha_estimada_llegada = date.fromisoformat(fecha_llegada_str)
            except ValueError:
                flash("Formato de fecha estimada inválido.", "error")
                return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=despacho)
        else:
            despacho.fecha_estimada_llegada = None

        # Sincronizar estado con trazabilidad
        traza = Trazabilidad.query.filter_by(lote_id=despacho.lote_id).first()
        if traza and nuevo_estado in ("EN_TRANSITO", "EN_PUERTO", "ENTREGADO"):
            traza.estado = nuevo_estado

        db.session.commit()
        flash("Despacho actualizado correctamente.", "success")
        return redirect(url_for("despachos.lista"))

    return render_template("despachos/form.html", lotes=lotes, estados=ESTADOS, despacho=despacho)


@despachos_bp.route("/<int:despacho_id>/eliminar", methods=["POST"])
@login_required
def eliminar(despacho_id):
    despacho = Despacho.query.get_or_404(despacho_id)
    db.session.delete(despacho)
    db.session.commit()
    flash("Despacho eliminado.", "success")
    return redirect(url_for("despachos.lista"))