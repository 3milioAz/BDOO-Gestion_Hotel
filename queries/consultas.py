class ConsultasHotel:
    def __init__(self, db_root):
        """
        Recibe la raíz (root) de la base de datos ZODB para acceder
        a los diccionarios/colecciones persistentes del hotel.
        """
        self.huespedes = db_root.get('huespedes', {})
        self.reservaciones = db_root.get('reservaciones', {})
        self.habitaciones = db_root.get('habitaciones', {})

    # 1. Listar todas las habitaciones
    def listar_todas_las_habitaciones(self):
        """Devuelve la lista de todas las habitaciones registradas en el hotel."""
        return list(self.habitaciones.values())

    # 2. Buscar una habitación mediante su identidad
    def buscar_habitacion_por_numero(self, numero_habitacion: str):
        """Busca y devuelve una habitación por su numeroHabitacion (identificador único)."""
        return self.habitaciones.get(str(numero_habitacion), None)

    # 3. Mostrar habitaciones disponibles
    def mostrar_habitaciones_disponibles(self):
        """Devuelve la lista de habitaciones cuyo estado es 'Disponible'."""
        return [h for h in self.habitaciones.values() if h.estado == "Disponible"]

    # 4. Mostrar habitaciones por tipo
    def mostrar_habitaciones_por_tipo(self, tipo: str):
        """Devuelve la lista de habitaciones filtradas por su tipo (e.g. 'Sencilla', 'Doble', 'Suite')."""
        return [h for h in self.habitaciones.values() if h.tipo.lower() == tipo.lower()]

    # 5. Buscar reservaciones de un huésped
    def buscar_reservaciones_de_huesped(self, id_huesped: str):
        """Devuelve el historial de reservaciones realizadas por un huésped en particular."""
        huesped = self.huespedes.get(id_huesped, None)
        if huesped:
            return huesped.consultarHistorial()
        return []

    # 6. Mostrar reservaciones activas
    def mostrar_reservaciones_activas(self):
        """Devuelve la lista de todas las reservaciones que tienen estado 'Activa'."""
        return [r for r in self.reservaciones.values() if r.estado == "Activa"]

    # 7. Mostrar huéspedes que tienen reservaciones
    def mostrar_huespedes_con_reservaciones(self):
        """Devuelve la lista de huéspedes que tienen al menos una reservación registrada."""
        return [h for h in self.huespedes.values() if len(h.reservaciones) > 0]

    # 8. Mostrar habitaciones ocupadas
    def mostrar_habitaciones_ocupadas(self):
        """Devuelve la lista de habitaciones cuyo estado actual es 'Ocupada'."""
        return [h for h in self.habitaciones.values() if h.estado == "Ocupada"]

    # 9. Calcular ingresos por reservaciones
    def calcular_ingresos_por_reservaciones(self):
        """Suma el total de todos los pagos registrados en todas las reservaciones del sistema."""
        total_ingresos = 0.0
        for r in self.reservaciones.values():
            for p in r.pagos:
                total_ingresos += p.monto
        return total_ingresos

    # 10. Identificar las habitaciones con mayor número de reservaciones
    def identificar_habitaciones_mayor_demanda(self):
        """
        Cuenta cuántas reservaciones ha tenido cada habitación a lo largo del tiempo
        y devuelve una lista ordenada de mayor a menor con el formato: (Habitacion, total_reservas).
        """
        conteo = {}
        for r in self.reservaciones.values():
            if r.habitacionRef:
                num = r.habitacionRef.numeroHabitacion
                conteo[num] = conteo.get(num, 0) + 1

        # Ordenar por el número de reservaciones descendente
        conteo_ordenado = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
        
        # Mapear los números de habitación de regreso a objetos Habitacion
        resultado = []
        for num, total in conteo_ordenado:
            hab_obj = self.habitaciones.get(num)
            if hab_obj:
                resultado.append((hab_obj, total))
        return resultado

    # 11. Mostrar reservaciones que incluyen servicios adicionales
    def mostrar_reservaciones_con_servicios_adicionales(self):
        """Devuelve las reservaciones que cuentan con al menos un consumo/servicio registrado."""
        return [r for r in self.reservaciones.values() if len(r.consumos) > 0]

    # 12. Consulta propuesta por el equipo: Promedio de estancia (noches) por huésped
    def promedio_noches_estancia_por_huesped(self, id_huesped: str):
        """
        Consulta Propuesta: Calcula el promedio de noches reservadas por un huésped específico.
        Permite analizar el perfil de estancia de los clientes frecuentes.
        """
        reservas = self.buscar_reservaciones_de_huesped(id_huesped)
        if not reservas:
            return 0.0

        total_noches = sum(
            max(1, (r.fechaSalida - r.fechaEntrada).days) for r in reservas
        )
        return total_noches / len(reservas)