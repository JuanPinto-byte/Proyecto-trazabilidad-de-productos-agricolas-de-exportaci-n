from app.extensions import db
import json
from datetime import datetime


class Trazabilidad(db.Model):
    __tablename__ = 'trazabilidad'

    id                   = db.Column(db.Integer, primary_key=True)
    lote_id              = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False, unique=True)
    codigo_trazabilidad  = db.Column(db.String(100), unique=True, nullable=False)
    fecha_generacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )
    # Estados: 'GENERADO', 'EN_TRANSITO', 'EN_PUERTO', 'ENTREGADO', 'BLOQUEADO'
    estado               = db.Column(db.String(30))

    def __repr__(self):
        return f'<Trazabilidad {self.codigo_trazabilidad} — {self.estado}>'


class RecepcionAcopio(db.Model):
    __tablename__ = 'recepcion_acopio'

    id                    = db.Column(db.Integer, primary_key=True)
    lote_id               = db.Column(db.Integer, db.ForeignKey('lotes.id'),    nullable=False)
    fecha_recepcion       = db.Column(db.Date, nullable=False)
    cantidad_kg           = db.Column(db.Numeric(10, 2))
    temperatura_recepcion = db.Column(db.Numeric(5, 2))
    # Estado del producto al ingreso: 'BUENO', 'REGULAR', 'MALO'
    estado_producto       = db.Column(db.String(50))
    operario_id           = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones         = db.Column(db.Text)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    def __repr__(self):
        return f'<RecepcionAcopio lote={self.lote_id} kg={self.cantidad_kg}>'

class TrazabilidadEvento(db.Model):
    """Eventos por lote.

    Nota: La BD define la tabla `eventos_trazabilidad` con columnas `etapa` y `descripcion`.
    Para mantener compatibilidad con el código/templates existentes, exponemos propiedades
    como `estado`, `ubicacion_actual`, etc., que se guardan como JSON dentro de `descripcion`.
    """

    __tablename__ = 'eventos_trazabilidad'

    id = db.Column(db.Integer, primary_key=True)
    lote_id = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False)
    etapa = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_evento = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipios.id'))

    def _load_meta(self):
        if not self.descripcion:
            return {}
        try:
            data = json.loads(self.descripcion)
            return data if isinstance(data, dict) else {}
        except Exception:
            # Si viene como texto plano, lo tratamos como observaciones
            return {'observaciones': self.descripcion}

    def _save_meta(self, meta):
        self.descripcion = json.dumps(meta, ensure_ascii=False) if meta else None

    def _get_meta(self, key):
        return (self._load_meta().get(key) or None)

    def _set_meta(self, key, value):
        meta = self._load_meta()
        if value is None or value == '':
            meta.pop(key, None)
        else:
            meta[key] = value
        self._save_meta(meta)

    # Compatibilidad: `estado` del UI -> `etapa` en BD
    @property
    def estado(self):
        return self.etapa

    @estado.setter
    def estado(self, value):
        self.etapa = value

    @property
    def ubicacion_actual(self):
        return self._get_meta('ubicacion_actual')

    @ubicacion_actual.setter
    def ubicacion_actual(self, value):
        self._set_meta('ubicacion_actual', value)

    @property
    def transportista(self):
        return self._get_meta('transportista')

    @transportista.setter
    def transportista(self, value):
        self._set_meta('transportista', value)

    @property
    def vehiculo(self):
        return self._get_meta('vehiculo')

    @vehiculo.setter
    def vehiculo(self, value):
        self._set_meta('vehiculo', value)

    @property
    def origen(self):
        return self._get_meta('origen')

    @origen.setter
    def origen(self, value):
        self._set_meta('origen', value)

    @property
    def destino(self):
        return self._get_meta('destino')

    @destino.setter
    def destino(self, value):
        self._set_meta('destino', value)

    @property
    def observaciones(self):
        return self._get_meta('observaciones')

    @observaciones.setter
    def observaciones(self, value):
        self._set_meta('observaciones', value)

    def __repr__(self):
        return f'<TrazabilidadEvento lote={self.lote_id} etapa={self.etapa}>'


class Despacho(db.Model):
    __tablename__ = 'despachos'

    id = db.Column(db.Integer, primary_key=True)
    lote_id = db.Column(db.Integer, db.ForeignKey('lotes.id'), nullable=False)

    codigo_contenedor = db.Column(db.String(50))
    fecha_despacho = db.Column(db.Date)
    puerto_destino = db.Column(db.String(100))
    pais_destino = db.Column(db.String(100))
    estado = db.Column(db.String(30), server_default='PROGRAMADO', nullable=True)
    ubicacion_actual = db.Column(db.String(150))
    fecha_estimada_llegada = db.Column(db.Date)

    operario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )
    fecha_actualizacion = db.Column(db.DateTime, nullable=True)

    municipio_origen_id = db.Column(db.Integer, db.ForeignKey('municipios.id'), nullable=True)
    municipio_origen_ref = db.relationship('Municipio', foreign_keys=[municipio_origen_id])

    def __repr__(self):
        return f'<Despacho lote={self.lote_id} estado={self.estado}>'


class SincronizacionOffline(db.Model):
    __tablename__ = 'sincronizacion_offline'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    tipo_formulario = db.Column(db.String(50), nullable=False)
    referencia_id = db.Column(db.Integer)
    estado = db.Column(db.String(20), server_default='PENDIENTE', nullable=True)
    datos_json = db.Column(db.JSON)

    fecha_descarga = db.Column(db.DateTime, nullable=True)
    fecha_sincronizacion = db.Column(db.DateTime, nullable=True)
    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )

    def __repr__(self):
        return f'<SincronizacionOffline usuario={self.usuario_id} estado={self.estado}>'
    
class Auditoria(db.Model):
    """Registro automático de todas las operaciones críticas del sistema."""
    __tablename__ = 'auditoria'

    id               = db.Column(db.Integer, primary_key=True)
    usuario_id       = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tabla_afectada   = db.Column(db.String(100))
    # Operación: 'INSERT', 'UPDATE', 'DELETE'
    tipo_operacion   = db.Column(db.String(30))
    registro_id      = db.Column(db.Integer)
    datos_anteriores = db.Column(db.JSON)
    datos_nuevos     = db.Column(db.JSON)
    fecha_operacion = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=True,
    )
    direccion_ip     = db.Column(db.String(45))

    def __repr__(self):
        return f'<Auditoria {self.tipo_operacion} en {self.tabla_afectada} por usuario={self.usuario_id}>'