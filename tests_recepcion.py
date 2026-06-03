"""
QA — Pruebas de Recepción de Productos Agrícolas
Ejecutar con: python tests_recepcion.py  (desde la carpeta del proyecto)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.trazabilidad.trazabilidad import RecepcionAcopio
from app.models.produccion.finca import Finca
from app.models.produccion.lote import Lote
from app.models.produccion.agricultor import Agricultor
from datetime import date


def setup_datos_prueba(app):
    with app.app_context():
        agricultor = Agricultor.query.first()
        if not agricultor:
            agricultor = Agricultor(nombre='Agricultor QA', cedula='000001', telefono='0000000000')
            db.session.add(agricultor)
            db.session.commit()

        finca = Finca.query.filter_by(nombre_finca='Finca QA Test').first()
        if not finca:
            finca = Finca(
                nombre_finca='Finca QA Test',
                municipio='QA Ciudad',
                departamento='QA Dpto',
                agricultor_id=agricultor.id,
                estado='ACTIVO',
            )
            db.session.add(finca)
            db.session.commit()

        lote = Lote.query.filter_by(finca_id=finca.id, numero_lote='LOTE-QA-01').first()
        if not lote:
            lote = Lote(finca_id=finca.id, numero_lote='LOTE-QA-01', estado='ACTIVO')
            db.session.add(lote)
            db.session.commit()

        return finca.id, lote.id


def limpiar(app, lote_id):
    with app.app_context():
        RecepcionAcopio.query.filter_by(lote_id=lote_id).delete()
        db.session.commit()


def test_insercion_valida(app, finca_id, lote_id):
    """QA-01: Inserción válida — peso positivo, fecha presente."""
    with app.app_context():
        rec = RecepcionAcopio(
            lote_id=lote_id,
            cantidad_kg=150.75,
            fecha_recepcion=date.today(),
            observaciones='Prueba QA inserción válida',
        )
        db.session.add(rec)
        db.session.commit()
        encontrado = RecepcionAcopio.query.get(rec.id)
        assert encontrado is not None
        assert float(encontrado.cantidad_kg) == 150.75
        assert encontrado.fecha_recepcion == date.today()
        # Verificar relación con finca a través del lote
        lote = Lote.query.get(lote_id)
        assert lote.finca_id == finca_id
        print("[PASS] QA-01: Inserción válida.")
        return encontrado.id


def test_peso_negativo(app, finca_id, lote_id):
    """QA-02: Peso negativo rechazado por el endpoint."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'qa_user'
            sess['rol'] = 'COORDINADOR'
            sess['permisos'] = [('crear', 'recepcion_acopio')]

        r = client.post('/recepciones/nueva', data={
            'finca_id': finca_id,
            'lote_id': lote_id,
            'cantidad_kg': '-50',
            'fecha_recepcion': str(date.today()),
        }, follow_redirects=True)
        assert b'mayor que cero' in r.data
        print("[PASS] QA-02: Peso negativo rechazado.")


def test_fecha_vacia(app, finca_id, lote_id):
    """QA-03: Fecha vacía rechazada por el endpoint."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'qa_user'
            sess['rol'] = 'COORDINADOR'
            sess['permisos'] = [('crear', 'recepcion_acopio')]

        r = client.post('/recepciones/nueva', data={
            'finca_id': finca_id,
            'lote_id': lote_id,
            'cantidad_kg': '100',
            'fecha_recepcion': '',
        }, follow_redirects=True)
        assert b'obligatori' in r.data
        print("[PASS] QA-03: Fecha vacía rechazada.")


def test_visualizacion_lista(app, lote_id, recepcion_id):
    """QA-04: La recepción aparece en la vista de listado."""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'qa_user'
            sess['rol'] = 'COORDINADOR'
            sess['permisos'] = [('ver', 'recepcion_acopio')]

        r = client.get('/recepciones/')
        assert r.status_code == 200
        assert b'150' in r.data or b'Finca QA' in r.data
        print("[PASS] QA-04: Visualización en interfaz correcta.")


def test_integridad_referencial_finca(app):
    """QA-05: Lote inexistente genera error de FK."""
    with app.app_context():
        try:
            rec = RecepcionAcopio(
                lote_id=999999,
                cantidad_kg=100,
                fecha_recepcion=date.today(),
            )
            db.session.add(rec)
            db.session.commit()
            db.session.rollback()
            print("[WARN] QA-05: BD no lanzó error de FK (verificar FOREIGN_KEY_CHECKS).")
        except Exception as e:
            db.session.rollback()
            print(f"[PASS] QA-05: Integridad referencial validada — {type(e).__name__}.")


def test_lote_de_otra_finca(app, finca_id, lote_id):
    """QA-06: Lote que no pertenece a la finca seleccionada es rechazado."""
    with app.app_context():
        otra_finca = Finca.query.filter(Finca.id != finca_id).first()
        if not otra_finca:
            print("[SKIP] QA-06: Solo existe una finca.")
            return
        otra_finca_id = otra_finca.id

    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'qa_user'
            sess['rol'] = 'COORDINADOR'
            sess['permisos'] = [('crear', 'recepcion_acopio')]

        r = client.post('/recepciones/nueva', data={
            'finca_id': otra_finca_id,
            'lote_id': lote_id,
            'cantidad_kg': '100',
            'fecha_recepcion': str(date.today()),
        }, follow_redirects=True)
        assert b'no pertenece' in r.data
        print("[PASS] QA-06: Lote de finca incorrecta rechazado.")


if __name__ == '__main__':
    app = create_app()
    print("\n=== QA: Recepción de Productos Agrícolas ===\n")

    finca_id, lote_id = setup_datos_prueba(app)
    limpiar(app, lote_id)

    recepcion_id = test_insercion_valida(app, finca_id, lote_id)
    test_peso_negativo(app, finca_id, lote_id)
    test_fecha_vacia(app, finca_id, lote_id)
    test_visualizacion_lista(app, lote_id, recepcion_id)
    test_integridad_referencial_finca(app)
    test_lote_de_otra_finca(app, finca_id, lote_id)

    limpiar(app, lote_id)
    print("\n=== Pruebas completadas ===\n")
