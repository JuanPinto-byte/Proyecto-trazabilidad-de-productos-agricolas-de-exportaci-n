from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.produccion.lote import Lote
from app.models.trazabilidad.trazabilidad import Trazabilidad, TrazabilidadEvento
from app.extensions import db
from datetime import datetime
import pytz
import uuid
from functools import wraps

trazabilidad_bp = Blueprint('trazabilidad', __name__, url_prefix='/trazabilidad')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@trazabilidad_bp.route('/', endpoint='lista')
@login_required
def lista():
    lotes = Lote.query.all()
    return render_template('trazabilidad/lista.html', lotes=lotes)

def get_colombia_time():
    """Obtiene la hora actual de Colombia sin depender de APIs externas"""
    return datetime.now(pytz.timezone('America/Bogota')).replace(tzinfo=None)

def create_trazabilidad(lote_id):
    """Crea automáticamente un registro de Trazabilidad para un lote con evento inicial en la ubicación de la finca"""
    # Verificar que el lote existe
    lote = Lote.query.get(lote_id)
    if not lote:
        return None
    
    # Verificar que no exista ya una trazabilidad para este lote
    traza_existente = Trazabilidad.query.filter_by(lote_id=lote_id).first()
    if traza_existente:
        return traza_existente
    
    # Crear código de trazabilidad único
    codigo = f"TRZ-{lote.numero_lote}-{uuid.uuid4().hex[:6].upper()}"
    
    # Obtener la ubicación de la finca
    finca = lote.finca
    ubicacion_finca = finca.municipio or finca.departamento or finca.nombre_finca or "Finca"
    
    # Crear nuevo registro de trazabilidad
    nueva_traza = Trazabilidad(
        lote_id=lote_id,
        codigo_trazabilidad=codigo,
        estado='GENERADO',
        fecha_generacion=get_colombia_time()
    )
    
    db.session.add(nueva_traza)
    db.session.commit()
    
    # Crear evento inicial con la ubicación de la finca
    evento_inicial = TrazabilidadEvento(
        lote_id=lote_id,
        etapa='GENERADO',
        fecha_evento=get_colombia_time(),
        ubicacion_actual=ubicacion_finca
    )
    
    db.session.add(evento_inicial)
    db.session.commit()
    
    return nueva_traza


@trazabilidad_bp.route('/<int:lote_id>', methods=['GET', 'POST'])
@login_required
def ver_trazabilidad(lote_id):
    lote = Lote.query.get_or_404(lote_id)
    traza = Trazabilidad.query.filter_by(lote_id=lote_id).first()
    eventos = []
    eventos_usuarios = {}

    # Si no existe trazabilidad, crearla automáticamente
    if not traza:
        codigo = f"TRZ-{lote.numero_lote}-{uuid.uuid4().hex[:6].upper()}"
        traza = Trazabilidad(
            lote_id=lote_id,
            codigo_trazabilidad=codigo,
            estado='GENERADO',
            fecha_generacion=get_colombia_time()
        )
        db.session.add(traza)
        db.session.commit()
        flash(f'Trazabilidad iniciada con código {codigo}.', 'success')

    eventos = TrazabilidadEvento.query.filter_by(lote_id=lote_id)\
        .order_by(TrazabilidadEvento.fecha_evento.desc())\
        .all()

    if request.method == 'POST':
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

        event_time = get_colombia_time()
        traza.estado = nuevo_estado
        traza.fecha_generacion = event_time

        usuario_nombre = session.get('username') if session else 'Sin usuario'

        evento = TrazabilidadEvento(
            lote_id=lote_id,
            usuario_id=session.get('user_id'),
            fecha_evento=event_time,
            estado=nuevo_estado,
            ubicacion_actual=ubicacion_actual,
            transportista=transportista,
            vehiculo=vehiculo,
            origen=origen,
            destino=destino,
            observaciones=observaciones,
        )

        db.session.add(evento)
        db.session.commit()

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