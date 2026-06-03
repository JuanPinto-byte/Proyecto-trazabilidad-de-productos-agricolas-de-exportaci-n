from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.extensions import db
from app.models.trazabilidad.trazabilidad import RecepcionAcopio
from app.models.produccion.finca import Finca
from app.models.produccion.lote import Lote
from app.decorators import login_required, require_permiso
from datetime import date

recepciones_bp = Blueprint('recepciones', __name__, url_prefix='/recepciones')


def _parse_peso(value: str):
    """Valida y retorna el peso. Retorna (valor, ok)."""
    raw = (value or '').strip()
    if not raw:
        flash('El peso es obligatorio.', 'error')
        return None, False
    try:
        parsed = float(raw)
    except ValueError:
        flash('El peso debe ser un número válido.', 'error')
        return None, False
    if parsed <= 0:
        flash('El peso debe ser mayor que cero.', 'error')
        return None, False
    return parsed, True


def _parse_fecha(value: str):
    """Valida y retorna la fecha. Retorna (valor, ok)."""
    raw = (value or '').strip()
    if not raw:
        flash('La fecha de recepción es obligatoria.', 'error')
        return None, False
    try:
        parsed = date.fromisoformat(raw)
    except ValueError:
        flash('Formato de fecha inválido. Use YYYY-MM-DD.', 'error')
        return None, False
    return parsed, True


@recepciones_bp.route('/', endpoint='lista')
@login_required
@require_permiso('ver', 'recepcion_acopio')
def lista():
    # La finca se obtiene a través del lote (lote.finca_id → fincas)
    recepciones = (
        db.session.query(RecepcionAcopio, Finca.nombre_finca, Lote.numero_lote)
        .join(Lote,  Lote.id  == RecepcionAcopio.lote_id)
        .join(Finca, Finca.id == Lote.finca_id)
        .order_by(RecepcionAcopio.fecha_recepcion.desc())
        .all()
    )
    return render_template('recepciones/lista.html', recepciones=recepciones)


@recepciones_bp.route('/nueva', methods=['GET', 'POST'], endpoint='nueva')
@login_required
@require_permiso('crear', 'recepcion_acopio')
def nueva():
    fincas = Finca.query.order_by(Finca.nombre_finca).all()
    lotes  = Lote.query.order_by(Lote.numero_lote).all()
    today = date.today().isoformat()

    if request.method == 'POST':
        finca_id_raw  = request.form.get('finca_id', '').strip()
        lote_id_raw   = request.form.get('lote_id', '').strip()
        peso_raw      = request.form.get('cantidad_kg', '')
        fecha_raw     = request.form.get('fecha_recepcion', '')
        observaciones = request.form.get('observaciones', '').strip()

        # Validar finca seleccionada (solo para verificar integridad con lote)
        if not finca_id_raw:
            flash('Seleccione una finca.', 'error')
            return render_template('recepciones/form.html', fincas=fincas, lotes=lotes)

        # Validar lote
        if not lote_id_raw:
            flash('Seleccione un lote.', 'error')
            return render_template('recepciones/form.html', fincas=fincas, lotes=lotes)

        lote = Lote.query.get(int(lote_id_raw))
        if not lote:
            flash('El lote seleccionado no existe.', 'error')
            return render_template('recepciones/form.html', fincas=fincas, lotes=lotes)

        # Verificar integridad referencial: el lote debe pertenecer a la finca
        if lote.finca_id != int(finca_id_raw):
            flash('El lote seleccionado no pertenece a la finca indicada.', 'error')
            return render_template('recepciones/form.html', fincas=fincas, lotes=lotes, today=today)

        # Validar peso
        peso, peso_ok = _parse_peso(peso_raw)
        if not peso_ok:
            return render_template('recepciones/form.html', fincas=fincas, lotes=lotes, today=today)

        # Validar fecha
        fecha, fecha_ok = _parse_fecha(fecha_raw)
        if not fecha_ok:
            return render_template('recepciones/form.html', fincas=fincas, lotes=lotes, today=today)

        recepcion = RecepcionAcopio(
            lote_id         = lote.id,
            cantidad_kg     = peso,
            fecha_recepcion = fecha,
            operario_id     = session.get('user_id'),
            observaciones   = observaciones or None,
        )
        db.session.add(recepcion)
        db.session.commit()
        flash('Recepción registrada correctamente.', 'success')
        return redirect(url_for('recepciones.lista'))

    return render_template('recepciones/form.html', fincas=fincas, lotes=lotes, today=today)


@recepciones_bp.route('/lotes-por-finca')
@login_required
def lotes_por_finca():
    """Devuelve JSON con los lotes de una finca para el select dinámico."""
    finca_id = request.args.get('finca_id', type=int)
    if not finca_id:
        return jsonify([])
    lotes = Lote.query.filter_by(finca_id=finca_id).order_by(Lote.numero_lote).all()
    return jsonify([{'id': l.id, 'numero_lote': l.numero_lote} for l in lotes])
