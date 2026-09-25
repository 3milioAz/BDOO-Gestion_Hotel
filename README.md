# Sistema de Gestión de Hotel - "Vista del Bosque Xalapa" (BDOO)

Este proyecto implementa una Base de Datos Orientada a Objetos (BDOO) utilizando **Python** y **ZODB** (Zope Object Database) para la administración de habitaciones, huéspedes, reservaciones y servicios adicionales del Hotel *Vista del Bosque Xalapa*.

---

## Arquitectura del Proyecto

El sistema está organizado bajo un patrón en capas:

```text
DB_tienda/
│
├── datos/                      # Almacenamiento binario persistente de ZODB (.fs)
│
├── models/                     # Clases de dominio que heredan de persistent.Persistent
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
├── services/                   # Lógica operativa de negocio
│   ├── __init__.py
│   └── hotel_service.py
│
├── queries/                    # Implementación de las 12 consultas obligatorias
│   ├── __init__.py
│   └── consultas.py
│
├── .gitignore                  # Exclusión de archivos binarios y caché
├── requirements.txt            # Dependencias del proyecto
├── main.py                     # Script ejecutable principal y demostración
└── README.md
```

---

## Requisitos e Instalación

1. **Clonar el repositorio y entrar a la carpeta:**
   ```bash
   git clone [https://github.com/3milioAz/BDOO-Sistema_de_Gestion_de_un_Hotel.git](https://github.com/3milioAz/BDOO-Sistema_de_Gestion_de_un_Hotel.git) DB_tienda
   cd DB_tienda
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución del Sistema

Para ejecutar el flujo de prueba completo (creación de objetos, persistencia en `datos/`, reapertura de BD, actualización de estado y ejecución de las 12 consultas):

```bash
python main.py
```

---

## Consultas Requeridas Implementadas

Las consultas se encuentran encapsuladas dentro de la clase `ConsultasHotel` en `queries/consultas.py`:

1. **Listar todas las habitaciones.**
2. **Buscar una habitación mediante su identidad (`numeroHabitacion`).**
3. **Mostrar habitaciones disponibles.**
4. **Mostrar habitaciones por tipo.**
5. **Buscar reservaciones de un huésped.**
6. **Mostrar reservaciones activas.**
7. **Mostrar huéspedes que tienen reservaciones.**
8. **Mostrar habitaciones ocupadas.**
9. **Calcular ingresos por reservaciones.**
10. **Identificar las habitaciones con mayor número de reservaciones.**
11. **Mostrar reservaciones que incluyen servicios adicionales.**
12. **Consulta propuesta por el equipo:** Promedio de noches de estancia por huésped.