from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from decimal import Decimal, InvalidOperation

from app.extensions import db
from app.models.insumos.agroquimico import Agroquimico, AplicacionAgroquimico
from app.models.insumos.normativa import Normativa
from app.models.produccion.lote import Lote


agroquimicos_bp = Blueprint("agroquimicos", __name__)

TIPOS_AGROQUIMICOS = ["FERTILIZANTE", "PESTICIDA", "FUNGICIDA", "HERBICIDA", "INSECTICIDA", "ACARICIDA", "NEMATICIDA", "OTRO"]
UNIDADES_DOSIS = ["kg/ha", "L/ha", "ml/ha", "g/ha", "dosis/ha"]
MAX_DOSIS_HECTAREA = Decimal("1000.00")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def _parse_decimal(
    value: str,
    *,
    field_label: str,
    required: bool = False,
    min_value: Decimal | None = None,
    max_value: Decimal | None = None,
):
    raw = (value or "").strip()
    if not raw:
        if required:
            flash(f"{field_label} es obligatorio.", "error")
            return None, False
        return None, True

    raw = raw.replace(",", ".")
    try:
        parsed = Decimal(raw)
    except InvalidOperation:
        flash(f"{field_label} debe ser un número válido.", "error")
        return None, False

    if min_value is not None and parsed < min_value:
        flash(f"{field_label} no puede ser menor que {min_value}.", "error")
        return None, False

    if max_value is not None and parsed > max_value:
        flash(f"{field_label} no puede ser mayor que {max_value}.", "error")
        return None, False

    return parsed, True


@agroquimicos_bp.route("/agroquimicos")
@login_required
def lista():
    """Listar todos los agroquímicos registrados"""
    agroquimicos = Agroquimico.query.order_by(Agroquimico.fecha_creacion.desc()).all()
    return render_template("agroquimicos/lista.html", agroquimicos=agroquimicos)


@agroquimicos_bp.route("/agroquimicos/crear", methods=["GET", "POST"])
@login_required
def crear():
    """Crear un nuevo agroquímico"""
    
    if request.method == "POST":
        nombre_producto = (request.form.get("nombre_producto") or "").strip()
        tipo = (request.form.get("tipo") or "").strip().upper()
        unidad_dosis = (request.form.get("unidad_dosis") or "").strip()
        ficha_tecnica_url = (request.form.get("ficha_tecnica_url") or "").strip() or None
        
        # Parsear valores numéricos
        dosis_recomendada, ok_dosis_rec = _parse_decimal(
            request.form.get("dosis_recomendada"),
            field_label="Dosis recomendada",
            min_value=Decimal("0.01"),
            max_value=MAX_DOSIS_HECTAREA,
        )
        
        dosis_limite_hectarea, ok_dosis_lim = _parse_decimal(
            request.form.get("dosis_limite_hectarea"),
            field_label="Dosis límite por hectárea",
            min_value=Decimal("0.01"),
            max_value=MAX_DOSIS_HECTAREA,
        )
        
        periodo_carencia = request.form.get("periodo_carencia_dias", type=int) or 0
        
        # Validaciones
        if not nombre_producto:
            flash("El nombre del producto es obligatorio.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=None)
        
        if tipo and tipo not in TIPOS_AGROQUIMICOS:
            flash("Tipo de agroquímico inválido.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=None)
        
        if not ok_dosis_rec or not ok_dosis_lim:
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=None)
        
        # Validar que dosis_recomendada <= dosis_limite_hectarea
        if dosis_recomendada and dosis_limite_hectarea and dosis_recomendada > dosis_limite_hectarea:
            flash("La dosis recomendada no puede ser mayor que la dosis límite.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=None)
        
        if periodo_carencia < 0:
            flash("El período de carencia no puede ser negativo.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=None)
        
        # Crear agroquímico
        nuevo_agroquimico = Agroquimico(
            nombre_producto=nombre_producto,
            tipo=tipo,
            dosis_recomendada=dosis_recomendada,
            dosis_limite_hectarea=dosis_limite_hectarea,
            unidad_dosis=unidad_dosis,
            periodo_carencia_dias=periodo_carencia if periodo_carencia > 0 else None,
            ficha_tecnica_url=ficha_tecnica_url,
            activo=True
        )
        
        db.session.add(nuevo_agroquimico)
        db.session.commit()
        
        flash(f"Agroquímico '{nombre_producto}' creado correctamente.", "success")
        return redirect(url_for("agroquimicos.lista"))
    
    return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=None)


@agroquimicos_bp.route("/agroquimicos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    """Editar un agroquímico existente"""
    agroquimico = Agroquimico.query.get_or_404(id)
    
    if request.method == "POST":
        nombre_producto = (request.form.get("nombre_producto") or "").strip()
        tipo = (request.form.get("tipo") or "").strip().upper()
        unidad_dosis = (request.form.get("unidad_dosis") or "").strip()
        ficha_tecnica_url = (request.form.get("ficha_tecnica_url") or "").strip() or None
        
        # Parsear valores numéricos
        dosis_recomendada, ok_dosis_rec = _parse_decimal(
            request.form.get("dosis_recomendada"),
            field_label="Dosis recomendada",
            min_value=Decimal("0.01"),
            max_value=MAX_DOSIS_HECTAREA,
        )
        
        dosis_limite_hectarea, ok_dosis_lim = _parse_decimal(
            request.form.get("dosis_limite_hectarea"),
            field_label="Dosis límite por hectárea",
            min_value=Decimal("0.01"),
            max_value=MAX_DOSIS_HECTAREA,
        )
        
        periodo_carencia = request.form.get("periodo_carencia_dias", type=int) or 0
        
        # Validaciones
        if not nombre_producto:
            flash("El nombre del producto es obligatorio.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=agroquimico)
        
        if tipo and tipo not in TIPOS_AGROQUIMICOS:
            flash("Tipo de agroquímico inválido.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=agroquimico)
        
        if not ok_dosis_rec or not ok_dosis_lim:
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=agroquimico)
        
        if dosis_recomendada and dosis_limite_hectarea and dosis_recomendada > dosis_limite_hectarea:
            flash("La dosis recomendada no puede ser mayor que la dosis límite.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=agroquimico)
        
        if periodo_carencia < 0:
            flash("El período de carencia no puede ser negativo.", "error")
            return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=agroquimico)
        
        # Actualizar agroquímico
        agroquimico.nombre_producto = nombre_producto
        agroquimico.tipo = tipo
        agroquimico.dosis_recomendada = dosis_recomendada
        agroquimico.dosis_limite_hectarea = dosis_limite_hectarea
        agroquimico.unidad_dosis = unidad_dosis
        agroquimico.periodo_carencia_dias = periodo_carencia if periodo_carencia > 0 else None
        agroquimico.ficha_tecnica_url = ficha_tecnica_url
        
        db.session.commit()
        
        flash(f"Agroquímico '{nombre_producto}' actualizado correctamente.", "success")
        return redirect(url_for("agroquimicos.lista"))
    
    return render_template("agroquimicos/form.html", tipos=TIPOS_AGROQUIMICOS, unidades=UNIDADES_DOSIS, agroquimico=agroquimico)


@agroquimicos_bp.route("/agroquimicos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    """Eliminar un agroquímico (soft delete - marcar como inactivo)"""
    agroquimico = Agroquimico.query.get_or_404(id)
    
    # Verificar si tiene aplicaciones registradas
    aplicaciones = AplicacionAgroquimico.query.filter_by(agroquimico_id=id).count()
    if aplicaciones > 0:
        flash("No se puede eliminar un agroquímico que tiene aplicaciones registradas. Desactívalo en su lugar.", "error")
        return redirect(url_for("agroquimicos.lista"))
    
    db.session.delete(agroquimico)
    db.session.commit()
    
    flash(f"Agroquímico '{agroquimico.nombre_producto}' eliminado correctamente.", "success")
    return redirect(url_for("agroquimicos.lista"))


@agroquimicos_bp.route("/agroquimicos/<int:id>/desactivar", methods=["POST"])
@login_required
def desactivar(id):
    """Desactivar un agroquímico"""
    agroquimico = Agroquimico.query.get_or_404(id)
    agroquimico.activo = False
    db.session.commit()
    
    flash(f"Agroquímico '{agroquimico.nombre_producto}' desactivado.", "success")
    return redirect(url_for("agroquimicos.lista"))


@agroquimicos_bp.route("/agroquimicos/<int:id>/activar", methods=["POST"])
@login_required
def activar(id):
    """Activar un agroquímico desactivado"""
    agroquimico = Agroquimico.query.get_or_404(id)
    agroquimico.activo = True
    db.session.commit()
    
    flash(f"Agroquímico '{agroquimico.nombre_producto}' activado.", "success")
    return redirect(url_for("agroquimicos.lista"))


@agroquimicos_bp.route("/agroquimicos/validar-dosis", methods=["POST"])
@login_required
def validar_dosis():
    """Validar si una dosis aplicada cumple con normativas (AJAX)"""
    agroquimico_id = request.form.get("agroquimico_id", type=int)
    dosis_aplicada = request.form.get("dosis_aplicada", type=float)
    lote_id = request.form.get("lote_id", type=int)

    if not agroquimico_id:
        return jsonify({"valido": False, "mensaje": "Agroquímico no indicado"}), 400

    if dosis_aplicada is None or dosis_aplicada <= 0:
        return jsonify({"valido": False, "mensaje": "Dosis aplicada inválida"}), 400

    if not lote_id:
        return jsonify({"valido": False, "mensaje": "Lote no indicado"}), 400
    
    agroquimico = Agroquimico.query.get(agroquimico_id)
    if not agroquimico:
        return jsonify({"valido": False, "mensaje": "Agroquímico no encontrado"})
    
    lote = Lote.query.get(lote_id)
    if not lote or not lote.area_hectareas:
        return jsonify({"valido": False, "mensaje": "Lote no válido o sin área definida"})
    
    # Convertir dosis aplicada a por hectárea
    area_hectareas = float(lote.area_hectareas)
    dosis_por_hectarea = dosis_aplicada / area_hectareas if area_hectareas > 0 else 0
    
    dosis_limite = float(agroquimico.dosis_limite_hectarea) if agroquimico.dosis_limite_hectarea else None
    dosis_recomendada = float(agroquimico.dosis_recomendada) if agroquimico.dosis_recomendada else None
    
    mensajes = []
    valido = True
    
    if dosis_limite and dosis_por_hectarea > dosis_limite:
        valido = False
        mensajes.append(f"⚠️ La dosis excede el límite de {dosis_limite} {agroquimico.unidad_dosis}")
    
    if dosis_recomendada and dosis_por_hectarea < dosis_recomendada:
        mensajes.append(f"⚠️ La dosis es menor a la recomendada ({dosis_recomendada} {agroquimico.unidad_dosis})")
    elif dosis_recomendada and dosis_por_hectarea == dosis_recomendada:
        mensajes.append(f"✓ Dosis igual a la recomendada ({dosis_recomendada} {agroquimico.unidad_dosis})")
    
    periodo_carencia = agroquimico.periodo_carencia_dias
    if periodo_carencia:
        mensajes.append(f"⏰ Período de carencia: {periodo_carencia} días antes de cosechar")
    
    return jsonify({
        "valido": valido,
        "mensaje": " | ".join(mensajes),
        "dosis_por_hectarea": round(dosis_por_hectarea, 4),
        "dosis_limite": float(dosis_limite) if dosis_limite else None,
        "dosis_recomendada": float(dosis_recomendada) if dosis_recomendada else None,
        "periodo_carencia": periodo_carencia
    })
