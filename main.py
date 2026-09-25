import datetime
import os
from persistence.database import ZODBManager
from services.hotel_service import HotelService
from queries.consultas import ConsultasHotel

def paso_1_crear_y_persistir_datos():
    print("=" * 70)
    print(" PASO 1: CREACIÓN DE OBJETOS Y PERSISTENCIA EN DB_hotel/datos ")
    print("=" * 70)

    # Inicializar administrador de base de datos ZODB
    db_manager = ZODBManager()
    root = db_manager.open()

    # Servicio de hotel
    service = HotelService(root)

    # 1. Registrar Habitaciones
    h101 = service.registrar_habitacion("101", "Sencilla", 800.0)
    h102 = service.registrar_habitacion("102", "Doble", 1200.0)
    h103 = service.registrar_habitacion("103", "Suite", 2500.0)

    # 2. Registrar Huéspedes
    hue1 = service.registrar_huesped("HUE-1001", "Juan Pérez", "2288112233", "juan.perez@email.com")
    hue2 = service.registrar_huesped("HUE-1002", "María López", "2281998877", "maria.lopez@email.com")

    # 3. Crear Reservaciones
    res1 = service.crear_reservacion(
        folio="RES-2026-01",
        fecha_in=datetime.date(2026, 10, 1),
        fecha_out=datetime.date(2026, 10, 5),
        id_huesped="HUE-1001",
        num_hab="102"
    )

    res2 = service.crear_reservacion(
        folio="RES-2026-02",
        fecha_in=datetime.date(2026, 10, 10),
        fecha_out=datetime.date(2026, 10, 12),
        id_huesped="HUE-1002",
        num_hab="103"
    )

    # 4. Registrar consumos adicionales y pagos
    res1.agregarConsumo("Servicio a la habitación - Desayuno", 250.0)
    res1.agregarConsumo("Uso de Gimnasio / Spa", 150.0)

    service.agregar_pago_a_reserva("RES-2026-01", "PAG-001", 1000.0, "Tarjeta de Crédito/Débito")
    service.agregar_pago_a_reserva("RES-2026-01", "PAG-002", 3800.0, "Efectivo")
    service.agregar_pago_a_reserva("RES-2026-02", "PAG-003", 5000.0, "Transferencia")

    # Guardar cambios
    db_manager.commit()
    print("✓ Transacción confirmada con transaction.commit()")
    print("✓ Objetos guardados correctamente en DB_hotel/datos/hotel_vista_bosque.fs")

    # Cerrar conexión para simular fin de ejecución
    db_manager.close()
    print("✓ Conexión cerrada y aplicación finalizada temporalmente.\n")


def paso_2_recuperar_y_ejecutar_consultas():
    print("=" * 70)
    print(" PASO 2: REAPERTURA DE BD Y DEMOSTRACIÓN DE LAS 12 CONSULTAS ")
    print("=" * 70)

    db_manager = ZODBManager()
    root = db_manager.open()

    consultas = ConsultasHotel(root)

    print("\n--- RESULTADO DE LAS CONSULTAS (queries/consultas.py) ---")

    # 1. Listar todas las habitaciones
    print("\n1. Listar todas las habitaciones:")
    for hab in consultas.listar_todas_las_habitaciones():
        print(f"   - {hab}")

    # 2. Buscar habitación por identidad
    print("\n2. Buscar habitación por número '102':")
    hab_encontrada = consultas.buscar_habitacion_por_numero("102")
    print(f"   - Encontrada: {hab_encontrada}")

    # 3. Mostrar habitaciones disponibles
    print("\n3. Mostrar habitaciones disponibles:")
    for hab in consultas.mostrar_habitaciones_disponibles():
        print(f"   - {hab}")

    # 4. Mostrar habitaciones por tipo
    print("\n4. Mostrar habitaciones por tipo ('Suite'):")
    for hab in consultas.mostrar_habitaciones_por_tipo("Suite"):
        print(f"   - {hab}")

    # 5. Buscar reservaciones de un huésped
    print("\n5. Buscar reservaciones del huésped 'HUE-1001':")
    for res in consultas.buscar_reservaciones_de_huesped("HUE-1001"):
        print(f"   - {res} | Costo Calculado: ${res.calcularCosto():,.2f}")

    # 6. Mostrar reservaciones activas
    print("\n6. Mostrar reservaciones activas:")
    for res in consultas.mostrar_reservaciones_activas():
        print(f"   - {res}")

    # 7. Mostrar huéspedes que tienen reservaciones
    print("\n7. Mostrar huéspedes con reservaciones registradas:")
    for hue in consultas.mostrar_huespedes_con_reservaciones():
        print(f"   - {hue} (Total reservas: {len(hue.reservaciones)})")

    # 8. Mostrar habitaciones ocupadas
    print("\n8. Mostrar habitaciones ocupadas:")
    for hab in consultas.mostrar_habitaciones_ocupadas():
        print(f"   - {hab}")

    # 9. Calcular ingresos por reservaciones
    ingresos = consultas.calcular_ingresos_por_reservaciones()
    print(f"\n9. Ingresos totales acumulados por pagos: ${ingresos:,.2f}")

    # 10. Identificar habitaciones con mayor demanda
    print("\n10. Habitaciones con mayor número de reservaciones (Demanda):")
    for hab, total in consultas.identificar_habitaciones_mayor_demanda():
        print(f"   - Habitación {hab.numeroHabitacion} ({hab.tipo}): {total} reservación(es)")

    # 11. Mostrar reservaciones que incluyen servicios adicionales
    print("\n11. Reservaciones que incluyen servicios adicionales (consumos):")
    for res in consultas.mostrar_reservaciones_con_servicios_adicionales():
        print(f"   - {res.folio}: {res.consumos}")

    # 12. Consulta propuesta por el equipo
    promedio_noches = consultas.promedio_noches_estancia_por_huesped("HUE-1001")
    print(f"\n12. [Propuesta Equipo] Promedio de noches de estancia para 'HUE-1001': {promedio_noches:.1f} noche(s)")

    # Modificación de estado para probar mutabilidad persistente
    print("\n------------------------------------------------------------")
    print(" PRUEBA DE MODIFICACIÓN DE ESTADO EN OBJETOS PERSISTENTES ")
    print("------------------------------------------------------------")
    res_mod = root['reservaciones'].get("RES-2026-01")
    if res_mod:
        res_mod.finalizar()
        db_manager.commit()
        print(f"✓ La reservación {res_mod.folio} ha sido actualizada a estado: {res_mod.estado}")
        print(f"✓ La habitación {res_mod.habitacionRef.numeroHabitacion} se liberó a estado: {res_mod.habitacionRef.estado}")

    db_manager.close()


if __name__ == '__main__':
    paso_1_crear_y_persistir_datos()
    paso_2_recuperar_y_ejecutar_consultas()