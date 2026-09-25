from models.huesped import Huesped
from models.habitacion import Habitacion
from models.reservacion import Reservacion
from models.pago import Pago

class HotelService:
    def __init__(self, db_root):
        """
        Recibe la raíz (root) de la base de datos ZODB para manipular
        los diccionarios y colecciones persistentes.
        """
        self.huespedes = db_root['huespedes']
        self.habitaciones = db_root['habitaciones']
        self.reservaciones = db_root['reservaciones']

    def registrar_huesped(self, id_huesped: str, nombre: str, telefono: str, correo: str) -> Huesped:
        """Crea y registra un nuevo huésped en el sistema."""
        if id_huesped in self.huespedes:
            raise ValueError(f"El huésped con ID {id_huesped} ya se encuentra registrado.")
        
        huesped = Huesped(id_huesped, nombre, telefono, correo)
        self.huespedes[id_huesped] = huesped
        return huesped

    def registrar_habitacion(self, numero: str, tipo: str, precio: float) -> Habitacion:
        """Crea y registra una nueva habitación en el hotel."""
        num_str = str(numero)
        if num_str in self.habitaciones:
            raise ValueError(f"La habitación {num_str} ya existe.")
        
        habitacion = Habitacion(num_str, tipo, precio)
        self.habitaciones[num_str] = habitacion
        return habitacion

    def crear_reservacion(self, folio: str, fecha_in, fecha_out, id_huesped: str, num_hab: str) -> Reservacion:
        """Crea una nueva reservación asociando un huésped y una habitación disponible."""
        huesped = self.huespedes.get(id_huesped)
        num_str = str(num_hab)
        habitacion = self.habitaciones.get(num_str)

        if not huesped:
            raise ValueError(f"No se encontró el huésped con ID {id_huesped}.")
        if not habitacion:
            raise ValueError(f"No se encontró la habitación número {num_str}.")

        if not habitacion.verificarDisponibilidad():
            raise ValueError(f"La habitación {num_str} no se encuentra disponible (Estado: {habitacion.estado}).")

        # Crear reservación y asociar relaciones
        res = Reservacion(folio, fecha_in, fecha_out, huesped, habitacion)
        huesped.registrarReservacion(res)
        self.reservaciones[folio] = res
        return res

    def agregar_pago_a_reserva(self, folio: str, id_pago: str, monto: float, metodo: str) -> Pago:
        """Registra un pago y lo asocia a una reservación existente."""
        res = self.reservaciones.get(folio)
        if not res:
            raise ValueError(f"No se encontró la reservación con folio {folio}.")
        
        pago = Pago(id_pago, monto, metodo)
        res.registrarPago(pago)
        return pago

    def agregar_consumo_a_reserva(self, folio: str, concepto: str, precio: float):
        """Registra un servicio adicional o consumo dentro de una reservación."""
        res = self.reservaciones.get(folio)
        if not res:
            raise ValueError(f"No se encontró la reservación con folio {folio}.")
        
        res.agregarConsumo(concepto, precio)

    def cancelar_reservacion(self, folio: str):
        """Cancela una reservación y libera la habitación asociada."""
        res = self.reservaciones.get(folio)
        if not res:
            raise ValueError(f"No se encontró la reservación con folio {folio}.")
        
        res.cancelar()

    def finalizar_reservacion(self, folio: str):
        """Finaliza una estancia (Check-out) y libera la habitación para nuevas reservas."""
        res = self.reservaciones.get(folio)
        if not res:
            raise ValueError(f"No se encontró la reservación con folio {folio}.")
        
        res.finalizar()