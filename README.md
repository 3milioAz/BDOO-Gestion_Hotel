# Sistema de Gestión de Hotel - "Vista del Bosque Xalapa" (BDOO)

## Descripción
Este proyecto consiste en un sistema de gestión de información desarrollado en **Python** que utiliza una **Base de Datos Orientada a Objetos (BDOO)** nativa mediante la librería **ZODB** (Zope Object Database). El sistema administra la información del Hotel *Vista del Bosque Xalapa*, garantizando la persistencia transparente de objetos de dominio sin necesidad de mapeo relacional (ORM).

---

## Problema que resuelve
El hotel requería una solución tecnológica para superar la gestión manual e inconexa de sus operaciones. El sistema resuelve:
- El descontrol en la asignación de habitaciones y choque de fechas.
- La pérdida de trazabilidad de los cargos adicionales y consumos durante la estancia de los huéspedes.
- La falta de un registro histórico centralizado de huéspedes, sus reservaciones y sus pagos.
- La dificultad para consultar métricas clave como ingresos, ocupación y niveles de demanda de habitaciones.

---

## Objetivo
Desarrollar e implementar una aplicación orientada a objetos en Python respaldada por ZODB, capaz de gestionar las reservaciones, habitaciones, huéspedes, consumos y pagos del hotel, asegurando la persistencia de datos entre ejecuciones y proporcionando un módulo de consultas analíticas para la toma de decisiones.

---

## Tecnologías
- **Lenguaje de programación:** Python 3.10+
- **Base de Datos Orientada a Objetos:** ZODB (Zope Object Database)
- **Componentes de persistencia:** `persistent`, `transaction`, `BTrees`, `FileStorage`
- **Control de versiones:** Git y GitHub
- **Entorno de desarrollo:** Visual Studio Code

---

## Modelo de objetos
El modelo de dominio se basa en cuatro entidades principales representadas como clases persistentes (`persistent.Persistent`):

1. **`Habitacion`**
   - *Identificador:* `numeroHabitacion`
   - *Atributos:* `tipo`, `precioPorNoche`, `estado`
   - *Comportamiento:* `verificarDisponibilidad()`, `ocupar()`, `liberar()`, `ponerEnMantenimiento()`

2. **`Huesped`**
   - *Identificador:* `idHuesped`
   - *Atributos:* `nombre`, `telefono`, `correo`, `reservaciones`
   - *Comportamiento:* `registrarReservacion()`, `consultarReservaciones()`, `consultarHistorial()`

3. **`Reservacion`**
   - *Identificador:* `folio`
   - *Atributos:* `fechaEntrada`, `fechaSalida`, `estado`, `huespedRef`, `habitacionRef`, `consumos`, `pagos`
   - *Comportamiento:* `calcularCosto()`, `agregarConsumo()`, `registrarPago()`, `cancelar()`, `finalizar()`

4. **`Pago`**
   - *Identificador:* `idPago`
   - *Atributos:* `monto`, `fechaPago`, `metodoPago`
   - *Comportamiento:* `registrarPago()`, `consultarPago()`

---

## Estructura del proyecto

```text
DB_tienda/
│
├── datos/                      # Almacenamiento binario persistente de ZODB (.fs)
│
├── models/                     # Clases de dominio persistentes
│   ├── __init__.py
│   ├── habitacion.py
│   ├── huesped.py
│   ├── pago.py
│   └── reservacion.py
│
├── persistence/                # Manejo de conexión y transacciones con ZODB
│   ├── __init__.py
│   └── database.py
│
├── services/                   # Lógica operativa del negocio
│   ├── __init__.py
│   └── hotel_service.py
│
├── queries/                    # Módulo de las 12 consultas obligatorias
│   ├── __init__.py
│   └── consultas.py
│
├── .gitignore                  # Exclusión de binarios (.fs) y caché
├── requirements.txt            # Dependencias del proyecto
├── main.py                     # Script principal de ejecución y demostración
└── README.md                   # Documentación del proyecto
```

---

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/3milioAz/BDOO-Sistema_de_Gestion_de_un_Hotel.git](https://github.com/3milioAz/BDOO-Sistema_de_Gestion_de_un_Hotel.git) DB_tienda
   cd DB_tienda
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución

Para ejecutar el programa y verificar la persistencia, mutabilidad de objetos y la ejecución de las 12 consultas:

```bash
python main.py
```

---

## Funcionalidades
- **Gestión de Registro:** Registro persistente de huéspedes y catálogo de habitaciones.
- **Control de Reservaciones:** Creación de reservas asociando huésped y habitación disponible.
- **Cobros y Servicios Extra:** Registro de consumos adicionales (desayunos, spa) y pagos desglosados (efectivo, tarjeta, transferencia).
- **Control de Estados (Ciclo de vida):** Actualización automática de estado de habitaciones (Disponible, Ocupada, Mantenimiento) y reservaciones (Activa, Cancelada, Finalizada).
- **Persistencia Binaria:** Almacenamiento de objetos sin mapeadores relacionales mediante `transaction.commit()`.

---

## Consultas implementadas
Ubicadas en `queries/consultas.py`:

1. **Listar todas las habitaciones:** Muestra el catálogo completo del hotel.
2. **Buscar habitación por identidad:** Localiza una habitación mediante su `numeroHabitacion`.
3. **Mostrar habitaciones disponibles:** Lista habitaciones listas para ocupación.
4. **Mostrar habitaciones por tipo:** Filtra por categoría (Sencilla, Doble, Suite).
5. **Buscar reservaciones de un huésped:** Obtiene el historial por `idHuesped`.
6. **Mostrar reservaciones activas:** Muestra estancias vigentes en el hotel.
7. **Mostrar huéspedes con reservaciones:** Lista clientes con al menos una estancia.
8. **Mostrar habitaciones ocupadas:** Muestra habitaciones actualmente con huéspedes.
9. **Calcular ingresos por reservaciones:** Suma contable de los pagos validados.
10. **Identificar habitaciones con mayor demanda:** Ranking de habitaciones más reservadas.
11. **Mostrar reservaciones con servicios adicionales:** Identifica reservas con cargos extra.
12. **Consulta propuesta por el equipo:** Promedio de noches de estancia por huésped.

---

## Reglas de negocio
- Una habitación no puede reservarse si su estado no es `"Disponible"`.
- Al crear una reservación, la habitación asignada pasa automáticamente a estado `"Ocupada"`.
- Al cancelar o finalizar una reservación, la habitación pasa automáticamente a estado `"Disponible"`.
- Todo pago debe registrar un monto estrictamente mayor a cero.
- La eliminación o modificación de un objeto notifica a ZODB mediante la bandera `_p_changed = True` para garantizar su sincronización en el almacenamiento.

---

## Uso de Git
El proyecto aplica un flujo de trabajo colaborativo basado en ramas por módulos:
- **`main`:** Rama principal con código estable y listo para producción.
- **`desarrollo-compañero` / `feature/modulo-huespedes`:** Ramas de trabajo individuales para el desarrollo de módulos específicos.
- **Pull Requests (PR):** Mecanismo para la revisión, integración y fusión del código entre integrantes.

---

## Integrantes
- **Josue Ramos Renteria:** Encargado de la carpeta de models y services.
- **Emilio Azael Valencia López:** Encargado de las consultas, persistencia, archivo main y documentacion del proyecto.

---

## Autores
- **Repositorio:** [3milioAz / BDOO-Sistema_de_Gestion_de_un_Hotel](https://github.com/3milioAz/BDOO-Sistema_de_Gestion_de_un_Hotel.git)
- **Proyecto académico:** Base de Datos Orientada a Objetos - Hotel Vista del Bosque Xalapa.