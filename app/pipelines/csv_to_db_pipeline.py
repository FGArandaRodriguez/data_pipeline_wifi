from pymongo import GEOSPHERE
from pymongo.errors import CollectionInvalid, BulkWriteError
import pandas as pd
import os
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

# Configura el logging
logging.basicConfig(level=logging.INFO)

def load_data_to_mongodb(csv_file_path, db):
    """
    Carga datos de un archivo CSV a MongoDB y crea un índice geoespacial.

    :param csv_file_path: Ruta al archivo CSV.
    :param db: Instancia de la base de datos de MongoDB.
    :return: Un diccionario con el recuento de documentos insertados, si se creó el índice y errores si ocurren.
    """
    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    if not collection_name:
        logging.error("El nombre de la colección no está especificado en las variables de entorno.")
        raise ValueError("El nombre de la colección es requerido.")

    try:
        db.create_collection(collection_name)
        logging.info(f"Colección '{collection_name}' creada exitosamente.")
    except CollectionInvalid:
        logging.info(f"La colección '{collection_name}' ya existe.")
        return

    collection = db[collection_name]

    try:
        data = pd.read_csv(csv_file_path)
        data['latitud'] = pd.to_numeric(data['latitud'], errors='coerce')
        data['longitud'] = pd.to_numeric(data['longitud'], errors='coerce')
        data.dropna(subset=['latitud', 'longitud'], inplace=True)
        
        data = data[(data['latitud'].between(-90, 90)) & (data['longitud'].between(-180, 180))]

        # Convierte los datos a formato GeoJSON.
        data['location'] = data.apply(lambda row: {'type': 'Point', 'coordinates': [row['longitud'], row['latitud']]}, axis=1)

        # Inserta los datos en la colección.
        result = collection.insert_many(data.to_dict('records'))
        inserted_count = len(result.inserted_ids)
        logging.info(f"Insertados {inserted_count} documentos en '{collection_name}'.")

        # Crea un índice 2dsphere si aún no existe.
        if 'location' not in collection.index_information():
            collection.create_index([("location", GEOSPHERE)])
            logging.info("Índice 2dsphere creado exitosamente en 'location'.")
        return {"inserted_count": inserted_count, "index_created": True, "error": None}
    except BulkWriteError as bwe:
        logging.error(f"Error al insertar los documentos: {bwe.details}")
        return {"inserted_count": 0, "index_created": False, "error": str(bwe.details)}
    except Exception as e:
        logging.error(f"Ocurrió un error: {e}")
        return {"inserted_count": 0, "index_created": False, "error": str(e)}