import os
import transaction
from ZODB import FileStorage, DB

class ZODBManager:
    def __init__(self, db_path=os.path.join('datos', 'hotel_vista_bosque.fs')):
        self.db_path = db_path
        self.storage = None
        self.db = None
        self.connection = None
        self.root = None

    def open(self):
        # Crear la carpeta datos/ si no existe en la raíz del proyecto
        folder = os.path.dirname(self.db_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        self.storage = FileStorage.FileStorage(self.db_path)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        # Inicialización de colecciones en la raíz de ZODB
        if 'huespedes' not in self.root:
            self.root['huespedes'] = {}
        if 'habitaciones' not in self.root:
            self.root['habitaciones'] = {}
        if 'reservaciones' not in self.root:
            self.root['reservaciones'] = {}

        return self.root

    def commit(self):
        transaction.commit()

    def close(self):
        if self.connection:
            self.connection.close()
        if self.db:
            self.db.close()
        if self.storage:
            self.storage.close()