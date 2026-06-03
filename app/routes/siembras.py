from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.produccion.siembra import Siembra
from app.models.produccion.cultivo import Cultivo
from app.models.produccion.lote import Lote
from app.models.produccion.semilla import Semilla
from app.decorators import login_required, require_permiso
from datetime import date

siembras_bp = Blueprint('siembras', __name__, url_prefix='/siembras')


@siembras_bp.route('/', endpoint='lista')
@login_required
@require_permiso('ver', 'siembras')
def lista():
    """Listar todas las siembras con fecha estimada de cosecha."""
    siembras = (
        Siembra.query
        .join(Cultivo, Cultivo.id == Siembra.cultivo_id)
        .join(Lote, Lote.id == Siembra.lote_id)
        .order_by(Siembra.fecha_siembra.desc())
        .all()
    )
    return render_template('siembras/lista.html', siembras=siembras, today=date.today())


@siembras_bp.route('/nueva', methods=['GET', 'POST'], endpoint='nueva')
@login_required
@require_permiso('crear', 'siembras')
def nueva():
    """Crear nueva siembra con cálculo automático de fecha estimada."""
    lotes = Lote.query.filter_by(estado='ACTIVO').order_by(Lote.numero_lote).all()
    cultivos = Cultivo.query.order_by(Cultivo.nombre).all()
    semillas = Semilla.query.order_by(Semilla.nombre_variedad).all()

    if request.method == 'POST':
        lote_id = request.form.get('lote_id', type=int)
        cultivo_id = request.form.get('cultivo_id', type=int)
        semilla_id = request.form.get('semilla_id', type=int)
        fecha_siembra_str = request.form.get('fecha_siembra', '').strip()
        observaciones = request.form.get('observaciones', '').strip() or None

        # Validar lote
        if not lote_id:
            flash('Seleccione un lote.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        lote = Lote.query.get(lote_id)
        if not lote or lote.estado != 'ACTIVO':
            flash('El lote seleccionado no existe o no está activo.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        # Validar cultivo
        if not cultivo_id:
            flash('Seleccione un cultivo.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        cultivo = Cultivo.query.get(cultivo_id)
        if not cultivo:
            flash('El cultivo seleccionado no existe.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        # Validar semilla
        if not semilla_id:
            flash('Seleccione una semilla.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        semilla = Semilla.query.get(semilla_id)
        if not semilla:
            flash('La semilla seleccionada no existe.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        # Validar fecha
        if not fecha_siembra_str:
            flash('La fecha de siembra es obligatoria.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        try:
            fecha_siembra = date.fromisoformat(fecha_siembra_str)
        except ValueError:
            flash('Formato de fecha inválido. Use YYYY-MM-DD.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        if fecha_siembra > date.today():
            flash('La fecha de siembra no puede ser en el futuro.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas)

        # Crear siembra
        siembra = Siembra(
            lote_id=lote_id,
            cultivo_id=cultivo_id,
            semilla_id=semilla_id,
            fecha_siembra=fecha_siembra,
            observaciones=observaciones,
            usuario_creacion_id=session.get('user_id'),
        )

        # Calcular fecha estimada de cosecha automáticamente
        siembra.fecha_cosecha_estimada = siembra.calcular_fecha_cosecha()

        db.session.add(siembra)
        db.session.commit()
        flash('Siembra registrada correctamente.', 'success')
        return redirect(url_for('siembras.lista'))

    today = date.today().isoformat()
    return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, today=today)


@siembras_bp.route('/editar/<int:id>', methods=['GET', 'POST'], endpoint='editar')
@login_required
@require_permiso('editar', 'siembras')
def editar(id):
    """Editar siembra existente."""
    siembra = Siembra.query.get_or_404(id)
    lotes = Lote.query.filter_by(estado='ACTIVO').order_by(Lote.numero_lote).all()
    cultivos = Cultivo.query.order_by(Cultivo.nombre).all()
    semillas = Semilla.query.order_by(Semilla.nombre_variedad).all()

    if request.method == 'POST':
        cultivo_id = request.form.get('cultivo_id', type=int)
        semilla_id = request.form.get('semilla_id', type=int)
        fecha_siembra_str = request.form.get('fecha_siembra', '').strip()
        observaciones = request.form.get('observaciones', '').strip() or None

        # Validar cultivo
        if not cultivo_id:
            flash('Seleccione un cultivo.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        cultivo = Cultivo.query.get(cultivo_id)
        if not cultivo:
            flash('El cultivo seleccionado no existe.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        # Validar semilla
        if not semilla_id:
            flash('Seleccione una semilla.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        semilla = Semilla.query.get(semilla_id)
        if not semilla:
            flash('La semilla seleccionada no existe.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        # Validar fecha
        if not fecha_siembra_str:
            flash('La fecha de siembra es obligatoria.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        try:
            fecha_siembra = date.fromisoformat(fecha_siembra_str)
        except ValueError:
            flash('Formato de fecha inválido. Use YYYY-MM-DD.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        if fecha_siembra > date.today():
            flash('La fecha de siembra no puede ser en el futuro.', 'error')
            return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra)

        # Actualizar siembra
        siembra.cultivo_id = cultivo_id
        siembra.semilla_id = semilla_id
        siembra.fecha_siembra = fecha_siembra
        siembra.observaciones = observaciones

        # Recalcular fecha estimada
        siembra.fecha_cosecha_estimada = siembra.calcular_fecha_cosecha()

        db.session.commit()
        flash('Siembra actualizada correctamente.', 'success')
        return redirect(url_for('siembras.lista'))

    today = date.today().isoformat()
    return render_template('siembras/form.html', lotes=lotes, cultivos=cultivos, semillas=semillas, siembra=siembra, today=today)


@siembras_bp.route('/eliminar/<int:id>', methods=['POST'], endpoint='eliminar')
@login_required
@require_permiso('eliminar', 'siembras')
def eliminar(id):
    """Eliminar siembra."""
    siembra = Siembra.query.get_or_404(id)
    lote_numero = siembra.lote.numero_lote if siembra.lote else 'desconocido'
    db.session.delete(siembra)
    db.session.commit()
    flash(f'Siembra del lote {lote_numero} eliminada correctamente.', 'success')
    return redirect(url_for('siembras.lista'))
