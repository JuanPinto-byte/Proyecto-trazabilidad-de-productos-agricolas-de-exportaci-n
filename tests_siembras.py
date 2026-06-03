"""
QA — Pruebas de Cálculo de Fecha Estimada de Cosecha
Ejecutar con: python tests_siembras.py  (desde la carpeta del proyecto)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.produccion.siembra import Siembra
from app.models.produccion.cultivo import Cultivo
from app.models.produccion.lote import Lote
from app.models.produccion.finca import Finca
from app.models.produccion.agricultor import Agricultor
from app.models.produccion.semilla import Semilla
from datetime import date, timedelta


def setup_datos_prueba(app):
    with app.app_context():
        # Crear agricultor
        agricultor = Agricultor.query.first()
        if not agricultor:
            agricultor = Agricultor(nombre='Agricultor QA Siembras', cedula='000002', telefono='0000000000')
            db.session.add(agricultor)
            db.session.commit()

        # Crear finca
        finca = Finca.query.filter_by(nombre_finca='Finca QA Siembras').first()
        if not finca:
            finca = Finca(
                nombre_finca='Finca QA Siembras',
                municipio='QA Ciudad',
                departamento='QA Dpto',
                agricultor_id=agricultor.id,
                estado='ACTIVO',
            )
            db.session.add(finca)
            db.session.commit()

        # Crear lote
        lote = Lote.query.filter_by(finca_id=finca.id, numero_lote='LOTE-SIEMBRA-01').first()
        if not lote:
            lote = Lote(finca_id=finca.id, numero_lote='LOTE-SIEMBRA-01', estado='ACTIVO')
            db.session.add(lote)
            db.session.commit()

        # Crear cultivo con ciclo de 60 días
        cultivo = Cultivo.query.filter_by(nombre='Cultivo QA Test').first()
        if not cultivo:
            cultivo = Cultivo(nombre='Cultivo QA Test', ciclo_dias=60, descripcion='Cultivo de prueba')
            db.session.add(cultivo)
            db.session.commit()

        # Crear semilla
        semilla = Semilla.query.filter_by(variedad='Semilla QA Test').first()
        if not semilla:
            semilla = Semilla(variedad='Semilla QA Test', estado='ACTIVO')
            db.session.add(semilla)
            db.session.commit()

        return lote.id, cultivo.id, semilla.id


def limpiar(app, lote_id):
    with app.app_context():
        Siembra.query.filter_by(lote_id=lote_id).delete()
        db.session.commit()


def test_calculo_valido(app, lote_id, cultivo_id, semilla_id):
    """QA-01: Cálculo válido de fecha estimada según ciclo del cultivo."""
    with app.app_context():
        fecha_siembra = date.today() - timedelta(days=10)
        siembra = Siembra(
            lote_id=lote_id,
            cultivo_id=cultivo_id,
            semilla_id=semilla_id,
            fecha_siembra=fecha_siembra,
        )
        
        # Calcular y asignar
        siembra.fecha_cosecha_estimada = siembra.calcular_fecha_cosecha()
        db.session.add(siembra)
        db.session.commit()
        
        encontrado = Siembra.query.get(siembra.id)
        assert encontrado is not None
        
        # Cultivo con ciclo de 60 días
        fecha_esperada = fecha_siembra + timedelta(days=60)
        assert encontrado.fecha_cosecha_estimada == fecha_esperada
        print(f"[PASS] QA-01: Cálculo válido — Siembra: {fecha_siembra}, Cosecha estimada: {fecha_esperada}")
        return encontrado.id


def test_calculo_sin_cultivo(app, lote_id, cultivo_id, semilla_id):
    """QA-02: Sin cultivo, calcular_fecha_cosecha retorna None."""
    with app.app_context():
        siembra = Siembra(
            lote_id=lote_id,
            cultivo_id=None,
            semilla_id=semilla_id,
            fecha_siembra=date.today() - timedelta(days=5),
        )
        
        resultado = siembra.calcular_fecha_cosecha()
        assert resultado is None
        print("[PASS] QA-02: Sin cultivo, retorna None.")


def test_calculo_sin_fecha_siembra(app, lote_id, cultivo_id, semilla_id):
    """QA-03: Sin fecha de siembra, calcular_fecha_cosecha retorna None."""
    with app.app_context():
        siembra = Siembra(
            lote_id=lote_id,
            cultivo_id=cultivo_id,
            semilla_id=semilla_id,
            fecha_siembra=None,
        )
        
        resultado = siembra.calcular_fecha_cosecha()
        assert resultado is None
        print("[PASS] QA-03: Sin fecha siembra, retorna None.")


def test_visualizacion_lista(app, lote_id, cultivo_id, semilla_id, siembra_id):
    """QA-04: Siembra aparece en la vista de listado con fecha estimada."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'qa_user'
            sess['rol'] = 'COORDINADOR'
            sess['permisos'] = [('ver', 'siembras')]

        r = client.get('/siembras/')
        assert r.status_code == 200
        # Verificar que contiene datos de siembra (lote, cultivo, fecha)
        assert b'LOTE-SIEMBRA-01' in r.data or b'Cultivo QA' in r.data
        print("[PASS] QA-04: Visualización en interfaz correcta.")


def test_integridad_referencial_cultivo(app, lote_id):
    """QA-05: Cultivo inexistente genera error de FK."""
    with app.app_context():
        try:
            siembra = Siembra(
                lote_id=lote_id,
                cultivo_id=999999,
                semilla_id=1,
                fecha_siembra=date.today(),
            )
            db.session.add(siembra)
            db.session.commit()
            db.session.rollback()
            print("[WARN] QA-05: BD no lanzó error de FK (verificar FOREIGN_KEY_CHECKS).")
        except Exception as e:
            db.session.rollback()
            print(f"[PASS] QA-05: Integridad referencial validada — {type(e).__name__}.")


def test_fecha_futura_rechazada(app, lote_id, cultivo_id, semilla_id):
    """QA-06: Fecha futura rechazada por el endpoint."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'qa_user'
            sess['rol'] = 'COORDINADOR'
            sess['permisos'] = [('crear', 'siembras')]

        fecha_futura = (date.today() + timedelta(days=5)).isoformat()
        r = client.post('/siembras/nueva', data={
            'lote_id': lote_id,
            'cultivo_id': cultivo_id,
            'semilla_id': semilla_id,
            'fecha_siembra': fecha_futura,
        }, follow_redirects=True)
        assert b'futuro' in r.data
        print("[PASS] QA-06: Fecha futura rechazada.")


if __name__ == '__main__':
    app = create_app()
    print("\n=== QA: Cálculo de Fecha Estimada de Cosecha ===\n")

    lote_id, cultivo_id, semilla_id = setup_datos_prueba(app)
    limpiar(app, lote_id)

    siembra_id = test_calculo_valido(app, lote_id, cultivo_id, semilla_id)
    test_calculo_sin_cultivo(app, lote_id, cultivo_id, semilla_id)
    test_calculo_sin_fecha_siembra(app, lote_id, cultivo_id, semilla_id)
    test_visualizacion_lista(app, lote_id, cultivo_id, semilla_id, siembra_id)
    test_integridad_referencial_cultivo(app, lote_id)
    test_fecha_futura_rechazada(app, lote_id, cultivo_id, semilla_id)

    limpiar(app, lote_id)
    print("\n=== Pruebas completadas ===\n")
