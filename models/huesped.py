import persistent
from models.reservacion import Reservacion

class Huesped(persistent.Persistent):
    def __init__(self, id_huesped: str, nombre: str, telefono: str, correo: str):
        super().__init__()
        self.idHuesped = id_huesped
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.reservaciones = []

    def registrarReservacion(self, reservacion: Reservacion):
        self.reservaciones.append(reservacion)
        self._p_changed = True

    def consultarReservaciones(self):
        return [r for r in self.reservaciones if r.estado == "Activa"]

    def consultarHistorial(self):
        return list(self.reservaciones)

    def __repr__(self):
        return f"<Huesped {self.idHuesped}: {self.nombre}>"