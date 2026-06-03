from app import create_app, db
from app.models.produccion.cultivo import Cultivo

app = create_app()

with app.app_context():
    # Ver cultivos existentes
    cultivos = Cultivo.query.all()
    print(f'Cultivos existentes: {len(cultivos)}')
    for c in cultivos:
        print(f'  - {c.nombre} (ciclo: {c.ciclo_dias} días)')
    
    # Crear nuevos cultivos con solo los campos válidos
    cultivos_nuevos = [
        {'nombre': 'Tomate', 'ciclo_dias': 60, 'descripcion': 'Cultivo de tomate rojo'},
        {'nombre': 'Lechuga', 'ciclo_dias': 45, 'descripcion': 'Lechuga hoja de roble'},
        {'nombre': 'Cebolla', 'ciclo_dias': 120, 'descripcion': 'Cebolla blanca'},
        {'nombre': 'Pimiento', 'ciclo_dias': 90, 'descripcion': 'Pimiento rojo'},
    ]
    
    for c_data in cultivos_nuevos:
        existe = Cultivo.query.filter_by(nombre=c_data['nombre']).first()
        if not existe:
            cultivo = Cultivo(**c_data)
            db.session.add(cultivo)
            print(f"Creado: {c_data['nombre']} ({c_data['ciclo_dias']} días)")
    
    db.session.commit()
    
    # Verificar
    cultivos = Cultivo.query.all()
    print(f'\nCultivos totales: {len(cultivos)}')
    for c in cultivos:
        print(f'  - {c.nombre} ({c.ciclo_dias} días)')
