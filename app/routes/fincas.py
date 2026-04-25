from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from functools import wraps
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.produccion.finca import Finca
from app.models.produccion.agricultor import Agricultor
from app.models.produccion.ubicacion import Departamento, Municipio
from app.models.usuarios.user import User


fincas_bp = Blueprint("fincas", __name__)


ESTADOS_FINCAS_VALIDOS = {"ACTIVO", "INACTIVO"}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def _normalize_name(value: str) -> str:
    return (value or "").strip().lower()


def _parse_float(value: str, *, field_label: str, required: bool = False, min_value: float | None = None):
    raw = (value or "").strip()
    if not raw:
        if required:
            flash(f"{field_label} es obligatorio.", "error")
            return None, False
        return None, True
    try:
        parsed = float(raw)
    except ValueError:
        flash(f"{field_label} debe ser un número válido.", "error")
        return None, False
    if min_value is not None and parsed < min_value:
        flash(f"{field_label} no puede ser menor que {min_value}.", "error")
        return None, False
    return parsed, True


def _render_form(*, finca, agricultores, usuarios, departamentos):
    return render_template(
        "fincas/form.html",
        finca=finca,
        agricultores=agricultores,
        usuarios=usuarios,
        departamentos=departamentos,
    )


@fincas_bp.get("/fincas/municipios")
@login_required
def municipios_por_departamento():
    departamento_id = request.args.get("departamento_id", type=int)
    if not departamento_id:
        return jsonify([])

    municipios = (
        Municipio.query.filter(Municipio.departamento_id == departamento_id)
        .order_by(Municipio.nombre)
        .all()
    )
    return jsonify([{"id": m.id, "nombre": m.nombre} for m in municipios])


@fincas_bp.route("/fincas")
@login_required
def lista():
    fincas = (
        db.session.query(Finca, Agricultor.nombre.label("agricultor_nombre"))
        .join(Agricultor, Agricultor.id == Finca.agricultor_id)
        .options(joinedload(Finca.departamento_ref), joinedload(Finca.municipio_ref))
        .order_by(Finca.fecha_creacion.desc())
        .all()
    )
    return render_template("fincas/lista.html", fincas=fincas)


@fincas_bp.route("/fincas/crear", methods=["GET", "POST"])
@login_required
def crear():
    agricultores = Agricultor.query.order_by(Agricultor.nombre).all()
    usuarios = User.query.filter_by(activo=True).order_by(User.nombre_completo).all()
    departamentos = Departamento.query.order_by(Departamento.nombre).all()

    if request.method == "POST":
        nombre_finca = request.form.get("nombre_finca", "").strip()
        departamento_id = request.form.get("departamento_id", type=int)
        municipio_id = request.form.get("municipio_id", type=int)
        coordenadas_gps = request.form.get("coordenadas_gps", "").strip()
        agricultor_id = request.form.get("agricultor_id", type=int)
        responsable_id = request.form.get("responsable_id", type=int)
        estado = (request.form.get("estado", "ACTIVO") or "ACTIVO").strip().upper()

        
        area_total, ok_total = _parse_float(
            request.form.get("area_total_hectareas"),
            field_label="Área total",
            required=False,
            min_value=0.01,
        )
        area_cultivable, ok_cult = _parse_float(
            request.form.get("area_cultivable_hectareas"),
            field_label="Área cultivable",
            required=True,
            min_value=0.01,
        )
        if area_total > 10000:
            flash("El área total no puede exceder 10,000 hectáreas.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )
        if not (ok_total and ok_cult):
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if not nombre_finca or len(nombre_finca) < 3 or len(nombre_finca) > 100:
            flash("El nombre de la finca es obligatorio (3–100 caracteres).", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if not agricultor_id:
            flash("Debes seleccionar un agricultor.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )
        if not Agricultor.query.get(agricultor_id):
            flash("El agricultor seleccionado no existe.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if responsable_id:
            responsable = User.query.get(responsable_id)
            if not responsable or not responsable.activo:
                flash("El responsable seleccionado no existe o está inactivo.", "error")
                return _render_form(
                    finca=None,
                    agricultores=agricultores,
                    usuarios=usuarios,
                    departamentos=departamentos,
                )

        if estado not in ESTADOS_FINCAS_VALIDOS:
            flash("Estado inválido.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if not departamento_id or not municipio_id:
            flash("Debes seleccionar departamento y municipio.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        departamento = Departamento.query.get(departamento_id)
        municipio = Municipio.query.get(municipio_id)
        if not departamento or not municipio:
            flash("Departamento o municipio inválido.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )
        if municipio.departamento_id != departamento.id:
            flash("El municipio no pertenece al departamento seleccionado.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if coordenadas_gps and len(coordenadas_gps) > 100:
            flash("Las coordenadas GPS no pueden exceder 100 caracteres.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if area_total is not None and area_cultivable is not None and area_cultivable > area_total:
            flash("El área cultivable no puede ser mayor que el área total.", "error")
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        # Permite mismo nombre si cambia la ubicación (municipio)
        nombre_norm = _normalize_name(nombre_finca)
        existe = Finca.query.filter(
            func.lower(Finca.nombre_finca) == nombre_norm,
            Finca.municipio_id == municipio.id,
        ).first()
        if existe:
            flash(
                f"Ya existe una finca llamada '{nombre_finca}' en {municipio.nombre}, {departamento.nombre}.",
                "error",
            )
            return _render_form(
                finca=None,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        nueva = Finca(
            nombre_finca=nombre_finca.strip(),
            departamento_id=departamento.id,
            municipio_id=municipio.id,
            # Copia de nombres (útil para reportes/compatibilidad con datos antiguos)
            departamento=departamento.nombre,
            municipio=municipio.nombre,
            coordenadas_gps=coordenadas_gps or None,
            area_total_hectareas=area_total,
            area_cultivable_hectareas=area_cultivable,
            agricultor_id=agricultor_id,
            responsable_id=responsable_id or None,
            estado=estado,
        )
        db.session.add(nueva)
        db.session.commit()
        flash(f"Finca '{nueva.nombre_finca}' creada correctamente.", "success")
        return redirect(url_for("fincas.lista"))

    return _render_form(
        finca=None,
        agricultores=agricultores,
        usuarios=usuarios,
        departamentos=departamentos,
    )


@fincas_bp.route("/fincas/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    finca = Finca.query.get_or_404(id)
    agricultores = Agricultor.query.order_by(Agricultor.nombre).all()
    usuarios = User.query.filter_by(activo=True).order_by(User.nombre_completo).all()
    departamentos = Departamento.query.order_by(Departamento.nombre).all()

    if request.method == "POST":
        nombre_finca = request.form.get("nombre_finca", "").strip()
        departamento_id = request.form.get("departamento_id", type=int)
        municipio_id = request.form.get("municipio_id", type=int)
        coordenadas_gps = request.form.get("coordenadas_gps", "").strip()
        agricultor_id = request.form.get("agricultor_id", type=int)
        responsable_id = request.form.get("responsable_id", type=int)
        estado = (request.form.get("estado", "ACTIVO") or "ACTIVO").strip().upper()

        area_total, ok_total = _parse_float(
            request.form.get("area_total_hectareas"),
            field_label="Área total",
            required=False,
            min_value=0.01,
        )
        area_cultivable, ok_cult = _parse_float(
            request.form.get("area_cultivable_hectareas"),
            field_label="Área cultivable",
            required=True,
            min_value=0.01,
        )
        if area_total > 10000:
            flash("El área total no puede exceder 10,000 hectáreas.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )
        if not (ok_total and ok_cult):
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if not nombre_finca or len(nombre_finca) < 3 or len(nombre_finca) > 100:
            flash("El nombre de la finca es obligatorio (3–100 caracteres).", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if not agricultor_id:
            flash("Debes seleccionar un agricultor.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )
        if not Agricultor.query.get(agricultor_id):
            flash("El agricultor seleccionado no existe.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if responsable_id:
            responsable = User.query.get(responsable_id)
            if not responsable or not responsable.activo:
                flash("El responsable seleccionado no existe o está inactivo.", "error")
                return _render_form(
                    finca=finca,
                    agricultores=agricultores,
                    usuarios=usuarios,
                    departamentos=departamentos,
                )

        if estado not in ESTADOS_FINCAS_VALIDOS:
            flash("Estado inválido.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if not departamento_id or not municipio_id:
            flash("Debes seleccionar departamento y municipio.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        departamento = Departamento.query.get(departamento_id)
        municipio = Municipio.query.get(municipio_id)
        if not departamento or not municipio:
            flash("Departamento o municipio inválido.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )
        if municipio.departamento_id != departamento.id:
            flash("El municipio no pertenece al departamento seleccionado.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if coordenadas_gps and len(coordenadas_gps) > 100:
            flash("Las coordenadas GPS no pueden exceder 100 caracteres.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        if area_total is not None and area_cultivable is not None and area_cultivable > area_total:
            flash("El área cultivable no puede ser mayor que el área total.", "error")
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        # Validación de consistencia: no reducir el área cultivable por debajo
        # del área actualmente ocupada por lotes activos.
        area_ocupada = sum(
            float(l.area_hectareas)
            for l in finca.lotes
            if l.area_hectareas and l.estado == "ACTIVO"
        )
        if area_cultivable is not None and area_ocupada > area_cultivable:
            flash(
                f"El área cultivable no puede ser menor que el área ocupada por lotes activos ({area_ocupada:.2f} ha).",
                "error",
            )
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        # Duplicado solo si misma ubicación (municipio) y mismo nombre
        nombre_norm = _normalize_name(nombre_finca)
        existe = Finca.query.filter(
            func.lower(Finca.nombre_finca) == nombre_norm,
            Finca.municipio_id == municipio.id,
            Finca.id != finca.id,
        ).first()
        if existe:
            flash(
                f"Ya existe una finca llamada '{nombre_finca}' en {municipio.nombre}, {departamento.nombre}.",
                "error",
            )
            return _render_form(
                finca=finca,
                agricultores=agricultores,
                usuarios=usuarios,
                departamentos=departamentos,
            )

        finca.nombre_finca = nombre_finca.strip()
        finca.departamento_id = departamento.id
        finca.municipio_id = municipio.id
        finca.departamento = departamento.nombre
        finca.municipio = municipio.nombre
        finca.coordenadas_gps = coordenadas_gps or None
        finca.area_total_hectareas = area_total
        finca.area_cultivable_hectareas = area_cultivable
        finca.agricultor_id = agricultor_id
        finca.responsable_id = responsable_id or None
        finca.estado = estado
        finca.fecha_actualizacion = db.func.current_timestamp()

        db.session.commit()
        flash(f"Finca '{finca.nombre_finca}' actualizada correctamente.", "success")
        return redirect(url_for("fincas.lista"))

    return _render_form(
        finca=finca,
        agricultores=agricultores,
        usuarios=usuarios,
        departamentos=departamentos,
    )


@fincas_bp.route("/fincas/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    finca = Finca.query.get_or_404(id)

    if finca.lotes:
        flash(
            f"No se puede eliminar '{finca.nombre_finca}' porque tiene lotes asociados.",
            "error",
        )
        return redirect(url_for("fincas.lista"))

    nombre = finca.nombre_finca
    db.session.delete(finca)
    db.session.commit()
    flash(f"Finca '{nombre}' eliminada correctamente.", "success")
    return redirect(url_for("fincas.lista"))