from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
import os
import logging

# Carga las variables de entorno desde el archivo .env
load_dotenv()

class MongoDB:
    def __init__(self, uri):
        """
        Inicializa la instancia MongoDB con la URI proporcionada.
        :param uri: URI de conexión a MongoDB.
        """
        self.uri = uri
        self.client = None
        self.db = None

    def connect(self):
        """
        Establece la conexión con MongoDB.
        """
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Realiza una operación rápida para verificar la conexión.
            self.client.admin.command('ping')
            logging.info("Conexión a MongoDB establecida exitosamente.")
        except ServerSelectionTimeoutError:
            logging.error("No se pudo conectar a MongoDB.")
            raise

    def get_db(self):
        """
        Obtiene una referencia a la base de datos especificada en la variable de entorno MONGO_DB_NAME.
        :return: Instancia de la base de datos.
        """
        db_name = os.getenv('MONGO_DB_NAME')
        if not self.client:
            logging.error("La conexión a MongoDB no ha sido establecida. Llamar primero a connect().")
            raise Exception("La conexión a MongoDB no ha sido establecida. Llamar primero a connect().")
        self.db = self.client[db_name] if db_name else self.client.get_default_database()
        return self.db

# Configura el logging
logging.basicConfig(level=logging.INFO)

# Uso de la clase MongoDB
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    logging.error("La URI de MongoDB no está definida en las variables de entorno.")
    raise Exception("La URI de MongoDB no está definida en las variables de entorno.")

mongo_client = MongoDB(mongo_uri)
mongo_client.connect()
db = mongo_client.get_db()
