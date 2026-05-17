from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date

from app.extensions import db
from app.models.seguimiento.bitacora import CondicionMeteorologica
from app.models.produccion.lote import Lote
from app.decorators import login_required

clima_bp = Blueprint("clima", __name__)


# ── LISTAR ────────────────────────────────────────────────────────────────────
@clima_bp.route("/clima")
@login_required
def lista():
    """Lista todos los registros de condiciones climáticas."""
    registros = (
        db.session.query(CondicionMeteorologica, Lote.numero_lote)
        .join(Lote, Lote.id == CondicionMeteorologica.lote_id)
        .order_by(CondicionMeteorologica.fecha.desc())
        .all()
    )
    return render_template("clima/lista.html", registros=registros)


# ── CREAR ─────────────────────────────────────────────────────────────────────
@clima_bp.route("/clima/crear", methods=["GET", "POST"])
@login_required
def crear():
    """Formulario y guardado de una nueva condición climática."""
    lotes = Lote.query.filter_by(estado="ACTIVO").order_by(Lote.numero_lote).all()

    if request.method == "POST":
        lote_id      = request.form.get("lote_id", "").strip()
        fecha        = request.form.get("fecha", "").strip()
        temperatura  = request.form.get("temperatura", "").strip()
        humedad      = request.form.get("humedad", "").strip()
        precipitacion = request.form.get("precipitacion", "").strip()
        observaciones = request.form.get("observaciones", "").strip()

        # ── Validaciones obligatorias ────────────────────────────────────────
        errores = False

        if not lote_id:
            flash("Debes seleccionar un lote.", "error")
            errores = True

        if not fecha:
            flash("La fecha es obligatoria.", "error")
            errores = True
        else:
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                if fecha_obj > date.today():
                    flash("La fecha no puede ser futura.", "error")
                    errores = True
            except ValueError:
                flash("Formato de fecha inválido.", "error")
                errores = True

        if not temperatura:
            flash("La temperatura es obligatoria.", "error")
            errores = True
        else:
            try:
                temp_val = float(temperatura)
                if temp_val < 0 or temp_val > 50:
                    flash("La temperatura debe estar entre 0 °C y 50 °C.", "error")
                    errores = True
            except ValueError:
                flash("La temperatura debe ser un número válido.", "error")
                errores = True

        if humedad:
            try:
                hum_val = float(humedad)
                if hum_val < 0 or hum_val > 100:
                    flash("La humedad debe estar entre 0 % y 100 %.", "error")
                    errores = True
            except ValueError:
                flash("La humedad debe ser un número válido.", "error")
                errores = True

        if not precipitacion:
            flash("La precipitación es obligatoria.", "error")
            errores = True
        else:
            try:
                prec_val = float(precipitacion)
                if prec_val < 0 or prec_val > 500:
                    flash("La precipitación debe estar entre 0 mm y 500 mm.", "error")
                    errores = True
            except ValueError:
                flash("La precipitación debe ser un número válido.", "error")
                errores = True

        if errores:
            return render_template(
                "clima/form.html",
                lotes=lotes,
                now=datetime.now(),
                form_data=request.form,
            )

        # ── Guardar en condiciones_meteorologicas ────────────────────────────
        nueva = CondicionMeteorologica(
            lote_id         = int(lote_id),
            fecha           = fecha_obj,
            temperatura     = float(temperatura),
            humedad         = float(humedad) if humedad else None,
            precipitacion_mm = float(precipitacion),
            observaciones   = observaciones or None,
        )
        db.session.add(nueva)
        db.session.commit()

        flash("Condición climática registrada correctamente.", "success")
        return redirect(url_for("clima.lista"))

    return render_template(
        "clima/form.html",
        lotes=lotes,
        now=datetime.now(),
        form_data={},
    )
