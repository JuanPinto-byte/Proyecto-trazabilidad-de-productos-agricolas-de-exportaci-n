from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.lote import Lote
from app.models.trazabilidad import Trazabilidad, TrazabilidadEvento
from app.extensions import db
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen
import json

trazabilidad_bp = Blueprint('trazabilidad', __name__, url_prefix='/trazabilidad')


@trazabilidad_bp.route('/', endpoint='lista')
def lista():
    lotes = Lote.query.all()
    return render_template('trazabilidad/lista.html', lotes=lotes)

def get_remote_colombia_time():
    try:
        with urlopen('http://worldtimeapi.org/api/timezone/America/Bogota', timeout=5) as response:
            payload = json.load(response)

        utc_dt_str = payload.get('utc_datetime')
        utc_offset = payload.get('utc_offset')
        if utc_dt_str and utc_offset:
            if utc_dt_str.endswith('Z'):
                utc_dt_str = utc_dt_str[:-1] + '+00:00'
            utc_dt = datetime.fromisoformat(utc_dt_str)
            if utc_dt.tzinfo is None:
                utc_dt = utc_dt.replace(tzinfo=timezone.utc)

            sign = 1 if utc_offset[0] == '+' else -1
            offset_hours = int(utc_offset[1:3])
            offset_minutes = int(utc_offset[4:6])
            bogota_tz = timezone(sign * timedelta(hours=offset_hours, minutes=offset_minutes))
            bogota_dt = utc_dt.astimezone(bogota_tz)
            return bogota_dt.replace(tzinfo=None)
    except Exception:
        pass

    # Fallback local Colombia time if remote fails
    return datetime.utcnow() - timedelta(hours=5)


@trazabilidad_bp.route('/<int:lote_id>', methods=['GET', 'POST'])
def ver_trazabilidad(lote_id):
    lote = Lote.query.get_or_404(lote_id)
    traza = Trazabilidad.query.filter_by(lote_id=lote_id).first()
    eventos = []
    eventos_usuarios = {}

    if traza:
        eventos = TrazabilidadEvento.query.filter_by(trazabilidad_id=traza.id).order_by(TrazabilidadEvento.fecha_evento.desc()).all()

    if request.method == 'POST':
        if not traza:
            flash('No se encontró registro de trazabilidad para este lote.', 'error')
            return redirect(url_for('trazabilidad.ver_trazabilidad', lote_id=lote_id))

        nuevo_estado = request.form.get('estado')
        ubicacion_actual = request.form.get('ubicacion_actual')
        transportista = request.form.get('transportista')
        vehiculo = request.form.get('vehiculo')
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        observaciones = request.form.get('observaciones')

        # Validar que al menos un valor sea diferente del último evento
        if eventos:
            ultimo_evento = eventos[0]
            
            # Comparar los campos
            es_igual = (
                nuevo_estado == ultimo_evento.estado and
                ubicacion_actual == (ultimo_evento.ubicacion_actual or '') and
                transportista == (ultimo_evento.transportista or '') and
                vehiculo == (ultimo_evento.vehiculo or '') and
                origen == (ultimo_evento.origen or '') and
                destino == (ultimo_evento.destino or '') and
                observaciones == (ultimo_evento.observaciones or '')
            )
            
            if es_igual:
                flash('El evento debe tener al menos un valor diferente al anterior. Por favor, modifica algún campo.', 'error')
                return redirect(url_for('trazabilidad.ver_trazabilidad', lote_id=lote_id))

        event_time = get_remote_colombia_time()
        traza.estado = nuevo_estado
        traza.fecha_generacion = event_time

        usuario_nombre = session.get('username') if session else 'Sin usuario'

        evento = TrazabilidadEvento(
            trazabilidad_id=traza.id,
            fecha_evento=event_time,
            estado=nuevo_estado,
            ubicacion_actual=ubicacion_actual,
            transportista=transportista,
            vehiculo=vehiculo,
            origen=origen,
            destino=destino,
            observaciones=observaciones
        )

        db.session.add(evento)
        db.session.commit()
        
        # Guardar el usuario en un diccionario para mostrar en la plantilla
        eventos_usuarios[evento.id] = usuario_nombre

        flash('Estado de trazabilidad y evento registrados correctamente.', 'success')
        return redirect(url_for('trazabilidad.ver_trazabilidad', lote_id=lote_id))

    return render_template(
        'trazabilidad/ver.html',
        lote=lote,
        traza=traza,
        eventos=eventos,
        eventos_usuarios=eventos_usuarios
    )