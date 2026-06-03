from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.almacenamiento.cosecha import Cosecha
from app.models.produccion.lote import Lote
from app.models.produccion.siembra import Siembra
from app.decorators import login_required, require_permiso
from datetime import date

cosechas_bp = Blueprint('cosechas', __name__, url_prefix='/cosechas')


@cosechas_bp.route('/', endpoint='lista')
@login_required
@require_permiso('ver', 'cosechas')
def lista():
    """Listar todas las cosechas."""
    cosechas = (
        db.session.query(Cosecha, Lote.numero_lote)
        .join(Lote, Lote.id == Cosecha.lote_id)
        .order_by(Cosecha.fecha_cosecha.desc())
        .all()
    )
    return render_template('cosechas/lista.html', cosechas=cosechas)


@cosechas_bp.route('/nueva', methods=['GET', 'POST'], endpoint='nueva')
@login_required
@require_permiso('crear', 'cosechas')
def nueva():
    """Registrar nueva cosecha. Acepta ?siembra_id=X para precargar lote."""
    lotes = Lote.query.order_by(Lote.numero_lote).all()
    today = date.today().isoformat()

    # Contexto informativo si se llega desde siembras
    siembra_info = None
    siembra_id = request.args.get('siembra_id', type=int)
    if siembra_id:
        siembra = Siembra.query.get(siembra_id)
        if siembra and siembra.lote and siembra.cultivo:
            siembra_info = {
                'id': siembra.id,
                'lote_id': siembra.lote_id,
                'numero_lote': siembra.lote.numero_lote,
                'cultivo': siembra.cultivo.nombre,
                'fecha_estimada': (
                    siembra.fecha_cosecha_estimada.strftime('%d/%m/%Y')
                    if siembra.fecha_cosecha_estimada else 'No calculada'
                ),
            }

    if request.method == 'POST':
        lote_id = request.form.get('lote_id', type=int)
        fecha_str = request.form.get('fecha_cosecha', '').strip()
        cantidad_str = request.form.get('cantidad_total_kg', '').strip()
        observaciones = request.form.get('observaciones', '').strip() or None

        # Validar lote
        if not lote_id:
            flash('Seleccione un lote.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        lote = Lote.query.get(lote_id)
        if not lote:
            flash('El lote seleccionado no existe.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        # Validar fecha
        if not fecha_str:
            flash('La fecha de cosecha es obligatoria.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        try:
            fecha_cosecha = date.fromisoformat(fecha_str)
        except ValueError:
            flash('Formato de fecha inválido. Use YYYY-MM-DD.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        if fecha_cosecha > date.today():
            flash('La fecha de cosecha no puede ser en el futuro.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        # Validar cantidad
        if not cantidad_str:
            flash('La cantidad cosechada es obligatoria.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        try:
            cantidad_kg = float(cantidad_str)
        except ValueError:
            flash('La cantidad debe ser un número válido.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        if cantidad_kg <= 0:
            flash('La cantidad debe ser mayor que cero.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, siembra_info=siembra_info)

        cosecha = Cosecha(
            lote_id=lote_id,
            fecha_cosecha=fecha_cosecha,
            cantidad_total_kg=cantidad_kg,
            observaciones=observaciones,
            usuario_id=session.get('user_id'),
        )

        db.session.add(cosecha)
        db.session.commit()
        flash('Cosecha registrada correctamente.', 'success')
        return redirect(url_for('cosechas.lista'))

    return render_template('cosechas/form.html',
                           lotes=lotes, today=today, siembra_info=siembra_info)


@cosechas_bp.route('/editar/<int:id>', methods=['GET', 'POST'], endpoint='editar')
@login_required
@require_permiso('editar', 'cosechas')
def editar(id):
    """Editar cosecha existente."""
    cosecha = Cosecha.query.get_or_404(id)
    lotes = Lote.query.order_by(Lote.numero_lote).all()
    today = date.today().isoformat()

    if request.method == 'POST':
        lote_id = request.form.get('lote_id', type=int)
        fecha_str = request.form.get('fecha_cosecha', '').strip()
        cantidad_str = request.form.get('cantidad_total_kg', '').strip()
        observaciones = request.form.get('observaciones', '').strip() or None

        if not lote_id:
            flash('Seleccione un lote.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        lote = Lote.query.get(lote_id)
        if not lote:
            flash('El lote seleccionado no existe.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        if not fecha_str:
            flash('La fecha de cosecha es obligatoria.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        try:
            fecha_cosecha = date.fromisoformat(fecha_str)
        except ValueError:
            flash('Formato de fecha inválido.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        if fecha_cosecha > date.today():
            flash('La fecha de cosecha no puede ser en el futuro.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        if not cantidad_str:
            flash('La cantidad cosechada es obligatoria.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        try:
            cantidad_kg = float(cantidad_str)
        except ValueError:
            flash('La cantidad debe ser un número válido.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        if cantidad_kg <= 0:
            flash('La cantidad debe ser mayor que cero.', 'error')
            return render_template('cosechas/form.html',
                                   lotes=lotes, today=today, cosecha=cosecha)

        cosecha.lote_id = lote_id
        cosecha.fecha_cosecha = fecha_cosecha
        cosecha.cantidad_total_kg = cantidad_kg
        cosecha.observaciones = observaciones

        db.session.commit()
        flash('Cosecha actualizada correctamente.', 'success')
        return redirect(url_for('cosechas.lista'))

    return render_template('cosechas/form.html',
                           lotes=lotes, today=today, cosecha=cosecha)


@cosechas_bp.route('/eliminar/<int:id>', methods=['POST'], endpoint='eliminar')
@login_required
@require_permiso('eliminar', 'cosechas')
def eliminar(id):
    """Eliminar cosecha."""
    cosecha = Cosecha.query.get_or_404(id)
    lote_numero = cosecha.lote.numero_lote if cosecha.lote else 'desconocido'
    db.session.delete(cosecha)
    db.session.commit()
    flash(f'Cosecha del lote {lote_numero} eliminada correctamente.', 'success')
    return redirect(url_for('cosechas.lista'))
