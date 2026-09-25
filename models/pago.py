import persistent
import datetime

class Pago(persistent.Persistent):
    def __init__(self, id_pago: str, monto: float, metodo_pago: str):
        super().__init__()
        self.idPago = id_pago
        self.monto = float(monto)
        self.fechaPago = datetime.datetime.now()
        self.metodoPago = metodo_pago

    def registrarPago(self):
        if self.monto <= 0:
            raise ValueError("El monto debe ser superior a cero.")
        return True

    def consultarPago(self):
        return {
            "idPago": self.idPago,
            "monto": self.monto,
            "fechaPago": self.fechaPago,
            "metodoPago": self.metodoPago
        }

    def __repr__(self):
        return f"<Pago {self.idPago}: ${self.monto:.2f} ({self.metodoPago})>"