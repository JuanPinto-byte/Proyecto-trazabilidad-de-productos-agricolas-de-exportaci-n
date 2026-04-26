from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.seguimiento.bitacora import BitacoraCultivo
from app.models.produccion.lote import Lote
from app.models.produccion.finca import Finca
from app.models.usuarios.user import User
from functools import wraps
from datetime import datetime
import os
from werkzeug.utils import secure_filename

bitacoras_bp = Blueprint("bitacoras", __name__)

# Configuración de carga de archivos
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'bitacoras')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Protección de sesión ──────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


# ── LISTAR CON FILTRADO ───────────────────────────────────────────────────────
@bitacoras_bp.route("/bitacoras")
@login_required
def lista():
    """Lista bitácoras con filtrado por lote y fecha"""
    
    # Parámetros de filtrado
    busqueda_lote = request.args.get("lote", "").strip()
    fecha_desde   = request.args.get("fecha_desde", "")
    fecha_hasta   = request.args.get("fecha_hasta", "")
    
    # Query base
    query = db.session.query(
        BitacoraCultivo, 
        Lote.numero_lote,
        Finca.nombre_finca,
        User.nombre_completo
    ).join(Lote, Lote.id == BitacoraCultivo.lote_id)\
     .join(Finca, Finca.id == Lote.finca_id)\
     .outerjoin(User, User.id == BitacoraCultivo.agronomo_id)
    
    # Filtro por nombre de lote
    if busqueda_lote:
        query = query.filter(Lote.numero_lote.ilike(f"%{busqueda_lote}%"))
    
    # Filtro por fecha desde
    if fecha_desde:
        query = query.filter(BitacoraCultivo.fecha >= fecha_desde)
    
    # Filtro por fecha hasta
    if fecha_hasta:
        query = query.filter(BitacoraCultivo.fecha <= fecha_hasta)
    
    # Ordenar por fecha descendente
    bitacoras = query.order_by(BitacoraCultivo.fecha.desc()).all()
    
    # Obtener lista de lotes para el filtro
    lotes_disponibles = Lote.query.filter_by(estado="ACTIVO").all()
    
    return render_template(
        "bitacoras/lista.html",
        bitacoras=bitacoras,
        lotes_disponibles=lotes_disponibles,
        busqueda_lote=busqueda_lote,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )


# ── CREAR BITÁCORA ────────────────────────────────────────────────────────────
@bitacoras_bp.route("/bitacoras/crear", methods=["GET", "POST"])
@login_required
def crear():
    """Crear nueva bitácora con registro de actividades, clima e imágenes"""
    
    lotes = Lote.query.filter_by(estado="ACTIVO").order_by(Lote.numero_lote).all()
    usuarios = User.query.filter_by(activo=True).all()
    
    if request.method == "POST":
        lote_id = request.form.get("lote_id")
        fecha = request.form.get("fecha")
        actividades = request.form.get("actividades_realizadas", "").strip()
        observaciones = request.form.get("observaciones", "").strip()
        agronomo_id = request.form.get("agronomo_id") or None
        
        # Datos adicionales para el registro
        siembra = request.form.get("siembra", "").strip()
        riego = request.form.get("riego", "").strip()
        fertilizacion = request.form.get("fertilizacion", "").strip()
        insumos = request.form.get("insumos", "").strip()
        temperatura = request.form.get("temperatura", "").strip()
        humedad = request.form.get("humedad", "").strip()
        precipitacion = request.form.get("precipitacion", "").strip()
        
        # Validaciones básicas
        if not lote_id:
            flash("Debes seleccionar un lote.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=None,
                now=datetime.now()
            )
        
        if not fecha:
            flash("La fecha es obligatoria.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=None,
                now=datetime.now()
            )
        
        if not actividades:
            flash("Debes registrar al menos una actividad.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=None,
                now=datetime.now()
            )
        
        # Validación de fecha (no puede ser futura)
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_obj > datetime.now().date():
                flash("No se pueden registrar fechas futuras. Solo hasta el día actual.", "error")
                return render_template(
                    "bitacoras/form.html",
                    lotes=lotes,
                    usuarios=usuarios,
                    bitacora=None,
                    now=datetime.now()
                )
        except ValueError:
            flash("Formato de fecha inválido.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=None,
                now=datetime.now()
            )
        
        # Validación de agrónomo (obligatorio)
        if not agronomo_id:
            flash("Debes asignar un agrólogo obligatoriamente.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=None,
                now=datetime.now()
            )
        
        # Validación de temperatura (máximo 30°C)
        if temperatura:
            try:
                temp_valor = float(temperatura)
                if temp_valor > 30:
                    flash("La temperatura no puede ser superior a 30°C.", "error")
                    return render_template(
                        "bitacoras/form.html",
                        lotes=lotes,
                        usuarios=usuarios,
                        bitacora=None,
                        now=datetime.now()
                    )
            except ValueError:
                flash("Temperatura inválida. Debe ser un número.", "error")
                return render_template(
                    "bitacoras/form.html",
                    lotes=lotes,
                    usuarios=usuarios,
                    bitacora=None,
                    now=datetime.now()
                )
        
        # Validación de precipitación (máximo 15mm)
        if precipitacion:
            try:
                precip_valor = float(precipitacion)
                if precip_valor > 15:
                    flash("La precipitación no puede ser superior a 15mm (límite de riesgo muy alto).", "error")
                    return render_template(
                        "bitacoras/form.html",
                        lotes=lotes,
                        usuarios=usuarios,
                        bitacora=None,
                        now=datetime.now()
                    )
            except ValueError:
                flash("Precipitación inválida. Debe ser un número.", "error")
                return render_template(
                    "bitacoras/form.html",
                    lotes=lotes,
                    usuarios=usuarios,
                    bitacora=None,
                    now=datetime.now()
                )
        
        # Construir el registro detallado en observaciones
        registro_detallado = f"""
=== REGISTRO DE ACTIVIDADES AGRÍCOLAS ===
Fecha: {fecha}

--- ACTIVIDADES REALIZADAS ---
{actividades}

--- ACTIVIDADES ESPECÍFICAS ---
Siembra: {siembra if siembra else 'N/A'}
Riego: {riego if riego else 'N/A'}
Fertilización: {fertilizacion if fertilizacion else 'N/A'}
Insumos utilizados: {insumos if insumos else 'N/A'}

--- CONDICIONES AMBIENTALES ---
Temperatura (°C): {temperatura if temperatura else 'N/A'}
Humedad (%): {humedad if humedad else 'N/A'}
Precipitación (mm): {precipitacion if precipitacion else 'N/A'}

--- OBSERVACIONES ADICIONALES ---
{observaciones if observaciones else 'Sin observaciones'}

=== FIN DEL REGISTRO ===
"""
        
        # Procesar imágenes
        imagenes_info = ""
        if 'imagenes' in request.files:
            archivos = request.files.getlist('imagenes')
            imagenes_guardadas = []
            
            for archivo in archivos:
                if archivo and archivo.filename != '' and allowed_file(archivo.filename):
                    # Generar nombre único para la imagen
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    filename = secure_filename(timestamp + archivo.filename)
                    
                    # Guardar archivo en la carpeta de uploads
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    archivo.save(filepath)
                    
                    imagenes_guardadas.append(filename)
            
            if imagenes_guardadas:
                imagenes_info = f"\n--- EVIDENCIA MULTIMEDIA ---\nImágenes adjuntas: {', '.join(imagenes_guardadas)}\n"
        
        # Construir registro detallado en observaciones
        registro_detallado = f"""=== REGISTRO DE ACTIVIDADES AGRÍCOLAS ===
Fecha: {fecha}

--- ACTIVIDADES REALIZADAS ---
{actividades}

--- ACTIVIDADES ESPECÍFICAS ---
Siembra: {siembra if siembra else 'N/A'}
Riego: {riego if riego else 'N/A'}
Fertilización: {fertilizacion if fertilizacion else 'N/A'}
Insumos utilizados: {insumos if insumos else 'N/A'}

--- CONDICIONES AMBIENTALES ---
Temperatura (°C): {temperatura if temperatura else 'N/A'}
Humedad (%): {humedad if humedad else 'N/A'}
Precipitación (mm): {precipitacion if precipitacion else 'N/A'}

--- OBSERVACIONES ADICIONALES ---
{observaciones if observaciones else 'Sin observaciones'}

=== FIN DEL REGISTRO ==="""
        
        # Crear bitácora con el registro completo
        try:
            nueva_bitacora = BitacoraCultivo(
                lote_id=int(lote_id),
                fecha=datetime.strptime(fecha, "%Y-%m-%d").date(),
                tipo_actividad=siembra if siembra else (riego if riego else (fertilizacion if fertilizacion else "Mantenimiento")),
                actividades_realizadas=actividades,
                insumos_utilizados=insumos if insumos else None,
                temperatura_c=float(temperatura) if temperatura else None,
                humedad_pct=float(humedad) if humedad else None,
                precipitacion_mm=float(precipitacion) if precipitacion else None,
                observaciones=registro_detallado,
                agronomo_id=int(agronomo_id)
            )
            
            db.session.add(nueva_bitacora)
            db.session.commit()
            
            flash("Bitácora creada correctamente.", "success")
            return redirect(url_for("bitacoras.lista"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar la bitácora: {str(e)}", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=None,
                now=datetime.now()
            )
    
    return render_template(
        "bitacoras/form.html",
        lotes=lotes,
        usuarios=usuarios,
        bitacora=None,
        now=datetime.now()
    )


# ── EDITAR BITÁCORA ───────────────────────────────────────────────────────────
@bitacoras_bp.route("/bitacoras/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    """Editar bitácora existente"""
    
    bitacora = BitacoraCultivo.query.get_or_404(id)
    lotes = Lote.query.filter_by(estado="ACTIVO").order_by(Lote.numero_lote).all()
    usuarios = User.query.filter_by(activo=True).all()
    
    if request.method == "POST":
        lote_id = request.form.get("lote_id")
        fecha_str = request.form.get("fecha")
        actividades = request.form.get("actividades_realizadas", "").strip()
        agronomo_id = request.form.get("agronomo_id")
        
        # Datos adicionales
        observaciones = request.form.get("observaciones", "").strip()
        siembra = request.form.get("siembra", "").strip()
        riego = request.form.get("riego", "").strip()
        fertilizacion = request.form.get("fertilizacion", "").strip()
        insumos = request.form.get("insumos", "").strip()
        temperatura = request.form.get("temperatura", "").strip()
        humedad = request.form.get("humedad", "").strip()
        precipitacion = request.form.get("precipitacion", "").strip()
        
        # Validaciones
        if not actividades:
            flash("Debes registrar al menos una actividad.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=bitacora
            )
        
        # Validación de fecha (no puede ser futura)
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha_obj > datetime.now().date():
                flash("No se pueden registrar fechas futuras. Solo hasta el día actual.", "error")
                return render_template(
                    "bitacoras/form.html",
                    lotes=lotes,
                    usuarios=usuarios,
                    bitacora=bitacora,
                    now=datetime.now()
                )
        except ValueError:
            flash("Formato de fecha inválido.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=bitacora,
                now=datetime.now()
            )
        
        # Validación de agrónomo (obligatorio)
        if not agronomo_id:
            flash("Debes asignar un agrólogo obligatoriamente.", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=bitacora,
                now=datetime.now()
            )
        
        # Validación de temperatura (máximo 30°C)
        if temperatura:
            try:
                temp_valor = float(temperatura)
                if temp_valor > 30:
                    flash("La temperatura no puede ser superior a 30°C.", "error")
                    return render_template(
                        "bitacoras/form.html",
                        lotes=lotes,
                        usuarios=usuarios,
                        bitacora=bitacora,
                        now=datetime.now()
                    )
            except ValueError:
                flash("Temperatura inválida. Debe ser un número.", "error")
                return render_template(
                    "bitacoras/form.html",
                    lotes=lotes,
                    usuarios=usuarios,
                    bitacora=bitacora,
                    now=datetime.now()
                )
        
        # Validación de precipitación (máximo 15mm)
        if precipitacion:
            try:
                precip_valor = float(precipitacion)
                if precip_valor > 15:
                    flash("La precipitación no puede ser superior a 15mm (límite de riesgo muy alto).", "error")
                    return render_template(
                        "bitacoras/form.html",
                        lotes=lotes,
                        usuarios=usuarios,
                        bitacora=bitacora
                    )
            except ValueError:
                flash("Precipitación inválida. Debe ser un número.", "error")
                return render_template(
                    "bitacoras/form.html",
                    lotes=lotes,
                    usuarios=usuarios,
                    bitacora=bitacora,
                    now=datetime.now()
                )
        
        # Asignar valores validados
        bitacora.lote_id = int(lote_id)
        bitacora.fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        bitacora.tipo_actividad = siembra if siembra else (riego if riego else (fertilizacion if fertilizacion else "Mantenimiento"))
        bitacora.actividades_realizadas = actividades
        bitacora.insumos_utilizados = insumos if insumos else None
        bitacora.temperatura_c = float(temperatura) if temperatura else None
        bitacora.humedad_pct = float(humedad) if humedad else None
        bitacora.precipitacion_mm = float(precipitacion) if precipitacion else None
        bitacora.agronomo_id = int(agronomo_id)
        
        # Reconstruir registro detallado
        registro_detallado = f"""=== REGISTRO DE ACTIVIDADES AGRÍCOLAS ===
Fecha: {bitacora.fecha}

--- ACTIVIDADES REALIZADAS ---
{bitacora.actividades_realizadas}

--- ACTIVIDADES ESPECÍFICAS ---
Siembra: {siembra if siembra else 'N/A'}
Riego: {riego if riego else 'N/A'}
Fertilización: {fertilizacion if fertilizacion else 'N/A'}
Insumos utilizados: {insumos if insumos else 'N/A'}

--- CONDICIONES AMBIENTALES ---
Temperatura (°C): {temperatura if temperatura else 'N/A'}
Humedad (%): {humedad if humedad else 'N/A'}
Precipitación (mm): {precipitacion if precipitacion else 'N/A'}

--- OBSERVACIONES ADICIONALES ---
{observaciones if observaciones else 'Sin observaciones'}

=== FIN DEL REGISTRO ==="""
        
        bitacora.observaciones = registro_detallado
        
        try:
            db.session.commit()
            flash("Bitácora actualizada correctamente.", "success")
            return redirect(url_for("bitacoras.lista"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar la bitácora: {str(e)}", "error")
            return render_template(
                "bitacoras/form.html",
                lotes=lotes,
                usuarios=usuarios,
                bitacora=bitacora
            )
    
    return render_template(
        "bitacoras/form.html",
        lotes=lotes,
        usuarios=usuarios,
        bitacora=bitacora
    )


# ── VER DETALLE DE BITÁCORA ──────────────────────────────────────────────────
@bitacoras_bp.route("/bitacoras/ver/<int:id>")
@login_required
def ver(id):
    """Ver detalle de una bitácora con galería de imágenes"""
    
    bitacora = db.session.query(
        BitacoraCultivo,
        Lote.numero_lote,
        Finca.nombre_finca,
        User.nombre_completo
    ).join(Lote, Lote.id == BitacoraCultivo.lote_id)\
     .join(Finca, Finca.id == Lote.finca_id)\
     .outerjoin(User, User.id == BitacoraCultivo.agronomo_id)\
     .filter(BitacoraCultivo.id == id).first_or_404()
    
    # Extraer nombres de imágenes del campo observaciones
    imagenes = []
    if bitacora[0].observaciones and "Imágenes adjuntas:" in bitacora[0].observaciones:
        # Parsear nombres de imágenes
        inicio = bitacora[0].observaciones.find("Imágenes adjuntas:") + len("Imágenes adjuntas:")
        fin = bitacora[0].observaciones.find("\n", inicio)
        if fin == -1:
            fin = len(bitacora[0].observaciones)
        imagenes_str = bitacora[0].observaciones[inicio:fin].strip()
        imagenes = [img.strip() for img in imagenes_str.split(",")]
    
    return render_template(
        "bitacoras/ver.html",
        bitacora=bitacora[0],
        numero_lote=bitacora[1],
        nombre_finca=bitacora[2],
        agronomo=bitacora[3],
        imagenes=imagenes
    )


# ── ELIMINAR BITÁCORA ─────────────────────────────────────────────────────────
@bitacoras_bp.route("/bitacoras/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    """Eliminar una bitácora"""
    
    bitacora = BitacoraCultivo.query.get_or_404(id)
    
    # Eliminar imágenes asociadas
    if bitacora.observaciones and "Imágenes adjuntas:" in bitacora.observaciones:
        inicio = bitacora.observaciones.find("Imágenes adjuntas:") + len("Imágenes adjuntas:")
        fin = bitacora.observaciones.find("\n", inicio)
        if fin == -1:
            fin = len(bitacora.observaciones)
        imagenes_str = bitacora.observaciones[inicio:fin].strip()
        imagenes = [img.strip() for img in imagenes_str.split(",")]
        
        for imagen in imagenes:
            filepath = os.path.join(UPLOAD_FOLDER, imagen)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
    
    db.session.delete(bitacora)
    db.session.commit()
    
    flash("Bitácora eliminada correctamente.", "success")
    return redirect(url_for("bitacoras.lista"))
