import persistent

class Habitacion(persistent.Persistent):
    def __init__(self, numero_habitacion: str, tipo: str, precio_por_noche: float, estado: str = "Disponible"):
        super().__init__()
        self.numeroHabitacion = str(numero_habitacion)
        self.tipo = tipo
        self.precioPorNoche = float(precio_por_noche)
        self.estado = estado  # "Disponible", "Ocupada", "Mantenimiento"

    def verificarDisponibilidad(self) -> bool:
        return self.estado == "Disponible"

    def ocupar(self):
        self.estado = "Ocupada"
        self._p_changed = True

    def liberar(self):
        self.estado = "Disponible"
        self._p_changed = True

    def ponerEnMantenimiento(self):
        self.estado = "Mantenimiento"
        self._p_changed = True
 
    def __repr__(self):
        return f"<Habitacion {self.numeroHabitacion} ({self.tipo}) - {self.estado}>"