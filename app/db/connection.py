from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
import os
load_dotenv()

class MongoDB:
    def __init__(self, uri):
        self.uri = uri
        self.client = None
        self.db = None

    def connect(self):
        """Establece la conexión con MongoDB."""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Realiza una operación rápida para verificar si hay conexión.
            self.client.admin.command('ping')
        except ServerSelectionTimeoutError:
            print("No se pudo conectar a MongoDB.")
            raise

    def get_db(self):
        db_name=os.getenv('MONGO_DB_NAME')
        """Obtiene una referencia a la base de datos."""
        if not self.client:
            raise Exception("La conexión a MongoDB no ha sido establecida. Llamar primero a connect().")
        self.db = self.client[db_name] if db_name else self.client.get_default_database()
        return self.db

# Uso de la clase MongoDB
mongo_uri = os.getenv('MONGO_URI')
mongo_db_name = os.getenv('MONGO_DB_NAME')

mongo_client = MongoDB(mongo_uri)
mongo_client.connect()
db = mongo_client.get_db()
