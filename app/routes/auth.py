from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.user import User
from app.models.rol import Rol
from sqlalchemy import func
from datetime import datetime
from functools import wraps

auth_bp = Blueprint("auth", __name__)


# ── Decorador: protege rutas que requieren sesión activa ──────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


# ── LOGIN ─────────────────────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya hay sesión activa, ir directo al dashboard
    if "user_id" in session:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter(
            (User.email == username) | (User.nombre_usuario == username)
        ).first()

        if not user:
            flash("Usuario no encontrado", "user_error")
            return redirect(url_for("auth.login"))

        if not user.check_password(password):
            flash("Contraseña incorrecta", "password_error")
            return redirect(url_for("auth.login"))

        # Guardar sesión
        session["user_id"]  = user.id
        session["username"] = user.nombre_usuario
        session["rol"]      = user.rol.nombre if user.rol else "sin_rol"

        # Actualizar último acceso
        user.ultimo_acceso = datetime.utcnow()
        db.session.commit()

        return redirect(url_for("auth.dashboard"))

    return render_template("login.html")


# ── REGISTER ──────────────────────────────────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre   = request.form.get('nombre')
        apellido = request.form.get('apellido')
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')
        telefono = request.form.get('telefono')

        if User.query.filter_by(nombre_usuario=username).first():
            flash("El nombre de usuario ya existe", "user_error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("El correo electrónico ya está registrado", "email_error")
            return redirect(url_for("auth.register"))

        # Rol por defecto: buscar el primer rol disponible (puedes cambiarlo)
        rol_defecto = Rol.query.first()

        nuevo_usuario = User(
            nombre_usuario  = username,
            nombre_completo = f"{nombre} {apellido}",
            email           = email,
            telefono        = telefono,
            rol_id          = rol_defecto.id if rol_defecto else None
        )
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ── LOGOUT ────────────────────────────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    # Importar modelos aquí para evitar importaciones circulares
    from app.models.finca    import Finca
    from app.models.lote     import Lote
    from app.models.anomalia import Anomalia
    from app.models.trazabilidad import Trazabilidad
    from app.models.bodega   import Bodega, ControlTemperatura
    from app.models.cosecha  import Cosecha

    # ── Usuario actual ────────────────────────────────────────────────────────
    usuario_actual = User.query.get(session["user_id"])

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_lotes  = Lote.query.filter(
        Lote.estado.in_(['ACTIVO', 'COSECHADO'])
    ).count()

    total_fincas = Finca.query.count()

    alertas_activas = Anomalia.query.filter(
        Anomalia.estado.in_(['PENDIENTE', 'EN_REVISION'])
    ).count()

    despachos_transito = Trazabilidad.query.filter(
        Trazabilidad.estado.in_(['EN_TRANSITO', 'EN_PUERTO'])
    ).count()

    despachos_puerto = Trazabilidad.query.filter_by(estado='EN_PUERTO').count()

    # ── Gráfica: producción por finca (kg cosechados) ─────────────────────────
    produccion = db.session.query(
        Finca.nombre_finca,
        func.sum(Cosecha.cantidad_total_kg).label('total_kg')
    ).join(Lote,    Lote.finca_id == Finca.id)\
     .join(Cosecha, Cosecha.lote_id == Lote.id)\
     .group_by(Finca.id, Finca.nombre_finca)\
     .all()

    grafica_fincas = [row.nombre_finca for row in produccion]
    grafica_real   = [float(row.total_kg or 0) for row in produccion]
    max_produccion = max(grafica_real + [1])

    # ── Últimos 5 lotes registrados ───────────────────────────────────────────
    ultimos_lotes = db.session.query(Lote, Finca.nombre_finca)\
        .join(Finca, Finca.id == Lote.finca_id)\
        .order_by(Lote.fecha_creacion.desc())\
        .limit(5).all()

    # ── Temperatura actual por bodega (último registro) ───────────────────────
    # Subconsulta: fecha más reciente por bodega
    subq = db.session.query(
        ControlTemperatura.bodega_id,
        func.max(ControlTemperatura.fecha_hora).label('ultima')
    ).group_by(ControlTemperatura.bodega_id).subquery()

    temps = db.session.query(Bodega, ControlTemperatura)\
        .join(subq, subq.c.bodega_id == Bodega.id)\
        .join(ControlTemperatura,
              (ControlTemperatura.bodega_id == subq.c.bodega_id) &
              (ControlTemperatura.fecha_hora == subq.c.ultima))\
        .all()

    bodegas_data = []
    for bodega, reg in temps:
        temp    = float(reg.temperatura)
        t_min   = float(bodega.temperatura_setpoint or 2) - 2
        t_max   = float(bodega.temperatura_setpoint or 6) + 2
        en_rango = t_min <= temp <= t_max
        porcentaje = min(int((temp / 10) * 100), 100)
        bodegas_data.append({
            'nombre':     bodega.nombre,
            'temperatura': temp,
            'ok':         en_rango,
            'porcentaje': porcentaje,
        })

    # ── Últimas anomalías (actividad reciente) ────────────────────────────────
    anomalias_recientes = db.session.query(Anomalia, Lote.numero_lote, User.nombre_completo)\
        .join(Lote, Lote.id == Anomalia.lote_id)\
        .join(User, User.id == Anomalia.registrado_por_usuario_id)\
        .order_by(Anomalia.fecha_deteccion.desc())\
        .limit(5).all()

    return render_template(
        "dashboard.html",
        # Usuario
        usuario         = usuario_actual,
        # KPIs
        total_lotes     = total_lotes,
        total_fincas    = total_fincas,
        alertas_activas = alertas_activas,
        despachos_transito = despachos_transito,
        despachos_puerto   = despachos_puerto,
        # Gráfica
        grafica_fincas  = grafica_fincas,
        grafica_real    = grafica_real,
        max_produccion  = max_produccion,
        # Tabla lotes
        ultimos_lotes   = ultimos_lotes,
        # Bodegas
        bodegas_data    = bodegas_data,
        # Actividad
        anomalias_recientes = anomalias_recientes,
        # Fecha actual para el template
        now             = datetime.utcnow(),
    )