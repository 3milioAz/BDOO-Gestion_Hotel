import persistent
import datetime
from models.pago import Pago

class Reservacion(persistent.Persistent):
    def __init__(self, folio: str, fecha_entrada: datetime.date, fecha_salida: datetime.date, huesped_ref, habitacion_ref=None):
        super().__init__()
        self.folio = folio
        self.fechaEntrada = fecha_entrada
        self.fechaSalida = fecha_salida
        self.estado = "Activa"  # "Activa", "Cancelada", "Finalizada"
        self.huespedRef = huesped_ref
        self.habitacionRef = habitacion_ref
        self.consumos = []
        self.pagos = []

        if self.habitacionRef and hasattr(self.habitacionRef, 'ocupar'):
            self.habitacionRef.ocupar()

    def calcularCosto(self) -> float:
        noches = max(1, (self.fechaSalida - self.fechaEntrada).days)
        costo_hospedaje = 0.0
        if self.habitacionRef:
            costo_hospedaje = noches * self.habitacionRef.precioPorNoche
        
        costo_consumos = sum(c.get('precio', 0.0) for c in self.consumos if isinstance(c, dict))
        return costo_hospedaje + costo_consumos

    def agregarConsumo(self, concepto: str, precio: float):
        self.consumos.append({"concepto": concepto, "precio": float(precio), "fecha": datetime.datetime.now()})
        self._p_changed = True

    def registrarPago(self, pago: Pago):
        pago.registrarPago()
        self.pagos.append(pago)
        self._p_changed = True

    def cancelar(self):
        self.estado = "Cancelada"
        if self.habitacionRef and hasattr(self.habitacionRef, 'liberar'):
            self.habitacionRef.liberar()
        self._p_changed = True

    def finalizar(self):
        self.estado = "Finalizada"
        if self.habitacionRef and hasattr(self.habitacionRef, 'liberar'):
            self.habitacionRef.liberar()
        self._p_changed = True

    def __repr__(self):
        return f"<Reservacion {self.folio} [{self.estado}] - Huésped: {self.huespedRef.nombre}>"