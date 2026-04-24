# Modelos existentes
from .user import User
from .rol import Rol

# Modelos nuevos — importar en orden respetando dependencias FK
from .agricultor import Agricultor
from .finca      import Finca
from .cultivo    import Cultivo, Semilla
from .lote       import Lote
from .siembra    import Siembra
from .cosecha    import Cosecha
from .agroquimico import Agroquimico, AplicacionAgroquimico
from .bodega     import Bodega, ControlTemperatura, Almacenamiento
from .anomalia   import Anomalia
from .bitacora   import BitacoraCultivo, CondicionMeteorologica
from .normativa  import Normativa, Inspeccion, CumplimientoNormativa
<<<<<<< HEAD
from .trazabilidad import Trazabilidad, RecepcionAcopio, Auditoria
=======
from .trazabilidad import Trazabilidad, TrazabilidadEvento, RecepcionAcopio, Auditoria
>>>>>>> c7495d7 (Crear trazabilidad)
