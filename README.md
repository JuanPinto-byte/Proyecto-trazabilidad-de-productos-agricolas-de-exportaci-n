# Proyecto Flask - Trazabilidad de Productos Agrícolas de Exportación

Aplicacion construida con flask, usando python y msysql (Por ahora usando sqlite hasta que mateo haga la base de poyos)
por ahora agregue la configuracion de extensions y  config

---

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/JuanPinto-byte/Proyecto-trazabilidad-de-productos-agricolas-de-exportaci-n.git
   cd Proyecto-trazabilidad-de-productos-agricolas-de-exportaci-n
2. ##Creacion y activacion del entorno virtual##
   python -m venv venv
   venv\Scripts\Activate.ps1
3. ## Instalacion de dependencias ##
   pip install -r requirements.txt
4. ## Estructura del proyecto ##
   app/
 ├── __init__.py          # Inicialización de la aplicación Flask
 ├── config.py            # Configuración general
 ├── extensions.py        # Extensiones (SQLAlchemy, Migrate, JWT)
 ├── models/              # Modelos de base de datos
 │    └── user.py
 └── routes/              # Rutas y controladores
      └── auth.py
requirements.txt          # Dependencias del proyecto
README.md                 # Documentación del proyecto
