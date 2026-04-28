from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from sqlalchemy import func
from datetime import datetime, timedelta

from app.extensions import db
from app.models.produccion.finca import Finca
from app.models.produccion.lote import Lote
from app.models.almacenamiento.cosecha import Cosecha
from app.models.almacenamiento.bodega import Bodega, ControlTemperatura, Almacenamiento
from app.models.insumos.agroquimico import Agroquimico, AplicacionAgroquimico
from app.models.trazabilidad.trazabilidad import Trazabilidad, Despacho

reportes_bp = Blueprint("reportes", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@reportes_bp.route("/reportes")
@login_required
def index():
    return render_template("reportes/index.html")


@reportes_bp.route("/reportes/produccion")
@login_required
def produccion():
    datos = (
        db.session.query(
            Finca.nombre_finca,
            Finca.area_cultivable_hectareas,
            func.sum(Cosecha.cantidad_total_kg).label("total_real_kg"),
            func.count(Lote.id).label("total_lotes"),
        )
        .join(Lote, Lote.finca_id == Finca.id)
        .outerjoin(Cosecha, Cosecha.lote_id == Lote.id)
        .group_by(Finca.id, Finca.nombre_finca, Finca.area_cultivable_hectareas)
        .order_by(func.isnull(func.sum(Cosecha.cantidad_total_kg)), func.sum(Cosecha.cantidad_total_kg).desc())
        .all()
    )

    RENDIMIENTO_ESTIMADO_KG_HA = 2500
    filas = []
    total_estimado = 0
    total_real = 0

    for row in datos:
        area = float(row.area_cultivable_hectareas or 0)
        estimado = round(area * RENDIMIENTO_ESTIMADO_KG_HA, 2)
        real = float(row.total_real_kg or 0)
        cumplimiento = round((real / estimado * 100), 1) if estimado > 0 else 0
        filas.append({
            "finca": row.nombre_finca,
            "area_ha": area,
            "estimado_kg": estimado,
            "real_kg": real,
            "lotes": row.total_lotes,
            "cumplimiento": cumplimiento,
        })
        total_estimado += estimado
        total_real += real

    cumplimiento_global = round((total_real / total_estimado * 100), 1) if total_estimado > 0 else 0

    return render_template(
        "reportes/produccion.html",
        filas=filas,
        total_estimado=total_estimado,
        total_real=total_real,
        cumplimiento_global=cumplimiento_global,
        now=datetime.now(),
    )


@reportes_bp.route("/reportes/normativo")
@login_required
def normativo():
    lotes_data = (
        db.session.query(
            Lote,
            Finca.nombre_finca,
            func.max(Cosecha.fecha_cosecha).label("ultima_cosecha"),
            func.count(Cosecha.id).label("num_cosechas"),
        )
        .join(Finca, Finca.id == Lote.finca_id)
        .outerjoin(Cosecha, Cosecha.lote_id == Lote.id)
        .group_by(Lote.id, Finca.nombre_finca)
        .order_by(Lote.fecha_creacion.desc())
        .all()
    )

    hoy = datetime.now().date()
    filas = []
    listos = bloqueados = en_revision = 0

    for lote, nombre_finca, ultima_cosecha, num_cosechas in lotes_data:
        aplicaciones_pendientes = (
            db.session.query(AplicacionAgroquimico)
            .join(Agroquimico, Agroquimico.id == AplicacionAgroquimico.agroquimico_id)
            .filter(AplicacionAgroquimico.lote_id == lote.id)
            .filter(Agroquimico.periodo_carencia_dias > 0)
            .all()
        )

        carencia_activa = False
        for ap in aplicaciones_pendientes:
            if ap.fecha_aplicacion and ap.agroquimico and ap.agroquimico.periodo_carencia_dias:
                fin_carencia = ap.fecha_aplicacion + timedelta(days=int(ap.agroquimico.periodo_carencia_dias))
                if fin_carencia > hoy:
                    carencia_activa = True
                    break

        if lote.estado == "BLOQUEADO":
            estado_cert = "BLOQUEADO"
            bloqueados += 1
        elif carencia_activa:
            estado_cert = "EN_CARENCIA"
            en_revision += 1
        elif lote.estado == "COSECHADO" and num_cosechas > 0:
            estado_cert = "LISTO"
            listos += 1
        else:
            estado_cert = "EN_PRODUCCION"
            en_revision += 1

        filas.append({
            "lote": lote,
            "finca": nombre_finca,
            "ultima_cosecha": ultima_cosecha,
            "num_cosechas": num_cosechas,
            "estado_cert": estado_cert,
            "carencia_activa": carencia_activa,
        })

    return render_template(
        "reportes/normativo.html",
        filas=filas,
        listos=listos,
        bloqueados=bloqueados,
        en_revision=en_revision,
        total=len(filas),
        now=datetime.now(),
    )


@reportes_bp.route("/reportes/almacenamiento")
@login_required
def almacenamiento():
    bodegas = Bodega.query.order_by(Bodega.nombre).all()
    bodegas_data = []

    for bodega in bodegas:
        historial = (
            ControlTemperatura.query
            .filter_by(bodega_id=bodega.id)
            .order_by(ControlTemperatura.fecha_hora.desc())
            .limit(10)
            .all()
        )
        historial.reverse()

        setpoint = float(bodega.temperatura_setpoint or 5)
        temp_actual = float(historial[-1].temperatura) if historial and historial[-1].temperatura else None
        ok = (abs(temp_actual - setpoint) <= 2.0) if temp_actual is not None else None

        kg_almacenados = (
            db.session.query(func.sum(Almacenamiento.cantidad_kg))
            .filter(Almacenamiento.bodega_id == bodega.id)
            .filter(Almacenamiento.fecha_salida == None)
            .scalar() or 0
        )
        cap_max = float(bodega.capacidad_maxima_kg or 1)
        ocupacion_pct = min(round((float(kg_almacenados) / cap_max) * 100, 1), 100)

        bodegas_data.append({
            "bodega": bodega,
            "temp_actual": temp_actual,
            "setpoint": setpoint,
            "ok": ok,
            "historial": historial,
            "kg_almacenados": float(kg_almacenados),
            "ocupacion_pct": ocupacion_pct,
        })

    return render_template(
        "reportes/almacenamiento.html",
        bodegas_data=bodegas_data,
        now=datetime.now(),
    )


@reportes_bp.route("/reportes/agroquimicos")
@login_required
def agroquimicos():
    resumen = (
        db.session.query(
            Agroquimico.nombre_producto,
            Agroquimico.tipo,
            Agroquimico.dosis_limite_hectarea,
            Agroquimico.unidad_dosis,
            func.count(AplicacionAgroquimico.id).label("num_aplicaciones"),
            func.sum(AplicacionAgroquimico.dosis_aplicada).label("total_dosis"),
            func.count(func.distinct(AplicacionAgroquimico.lote_id)).label("num_lotes"),
        )
        .join(AplicacionAgroquimico, AplicacionAgroquimico.agroquimico_id == Agroquimico.id)
        .group_by(
            Agroquimico.id,
            Agroquimico.nombre_producto,
            Agroquimico.tipo,
            Agroquimico.dosis_limite_hectarea,
            Agroquimico.unidad_dosis,
        )
        .order_by(func.isnull(func.sum(AplicacionAgroquimico.dosis_aplicada)), func.sum(AplicacionAgroquimico.dosis_aplicada).desc())
        .all()
    )

    detalle = (
        db.session.query(
            AplicacionAgroquimico,
            Agroquimico.nombre_producto,
            Agroquimico.tipo,
            Agroquimico.dosis_limite_hectarea,
            Lote.numero_lote,
            Finca.nombre_finca,
            Lote.area_hectareas,
        )
        .join(Agroquimico, Agroquimico.id == AplicacionAgroquimico.agroquimico_id)
        .join(Lote, Lote.id == AplicacionAgroquimico.lote_id)
        .join(Finca, Finca.id == Lote.finca_id)
        .order_by(AplicacionAgroquimico.fecha_aplicacion.desc())
        .limit(50)
        .all()
    )

    filas_detalle = []
    for ap, nombre, tipo, limite, numero_lote, nombre_finca, area_ha in detalle:
        area = float(area_ha or 1)
        dosis = float(ap.dosis_aplicada or 0)
        dosis_por_ha = round(dosis / area, 3) if area > 0 else dosis
        lim = float(limite or 0)
        excede = lim > 0 and dosis_por_ha > lim
        filas_detalle.append({
            "ap": ap,
            "nombre": nombre,
            "tipo": tipo,
            "limite": lim,
            "numero_lote": numero_lote,
            "finca": nombre_finca,
            "dosis_por_ha": dosis_por_ha,
            "excede": excede,
        })

    return render_template(
        "reportes/agroquimicos.html",
        resumen=resumen,
        filas_detalle=filas_detalle,
        now=datetime.now(),
    )


@reportes_bp.route("/reportes/despachos")
@login_required
def despachos():
    estado_filtro = request.args.get("estado", "")

    q = (
        db.session.query(
            Despacho,
            Lote.numero_lote,
            Finca.nombre_finca,
            Trazabilidad.codigo_trazabilidad,
        )
        .join(Lote, Lote.id == Despacho.lote_id)
        .join(Finca, Finca.id == Lote.finca_id)
        .outerjoin(Trazabilidad, Trazabilidad.lote_id == Lote.id)
        .order_by(Despacho.fecha_despacho.desc())
    )

    if estado_filtro:
        q = q.filter(Despacho.estado == estado_filtro)

    despachos_raw = q.all()

    conteos = (
        db.session.query(Despacho.estado, func.count(Despacho.id))
        .group_by(Despacho.estado)
        .all()
    )
    conteos_dict = {e: c for e, c in conteos}

    filas = []
    for despacho, numero_lote, nombre_finca, codigo_traza in despachos_raw:
        filas.append({
            "despacho": despacho,
            "numero_lote": numero_lote,
            "finca": nombre_finca,
            "codigo_traza": codigo_traza,
        })

    estados_posibles = ["PROGRAMADO", "EN_TRANSITO", "EN_PUERTO", "ENTREGADO", "CANCELADO"]

    return render_template(
        "reportes/despachos.html",
        filas=filas,
        conteos=conteos_dict,
        estados_posibles=estados_posibles,
        estado_filtro=estado_filtro,
        now=datetime.now(),
    )