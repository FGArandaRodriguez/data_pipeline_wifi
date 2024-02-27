from pymongo import MongoClient, GEOSPHERE
from ..db.connection import mongo_client
from bson.objectid import ObjectId
from bson.json_util import dumps
from functools import wraps
from flask import jsonify
import json
from dotenv import load_dotenv
import os
import logging
from ..db.connection import mongo_client
# Cargar variables de entorno para acceder a configuraciones sensibles y específicas del entorno.
load_dotenv(override=True)
# Configuración básica del logging para registrar información importante y errores.
logging.basicConfig(level=logging.INFO)

def with_db(func):
    """
    Este decorador automatiza la obtención de la colección de MongoDB, simplificando las funciones
    que realizan operaciones sobre la base de datos. Extrae el nombre de la colección de las variables
    de entorno y utiliza la instancia global `mongo_client` para acceder a la base de datos.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = mongo_client.get_db()
        return func(db, *args, **kwargs)
    return wrapper

# Función decorada con `with_db` para obtener todos los puntos WiFi de la colección.
@with_db
def get_all_wifi_points(db):
    """
    Obtiene todos los puntos WiFi almacenados en la colección especificada, excluyendo
    el campo '_id' para simplificar el resultado. Retorna una lista de puntos WiFi en formato JSON.
    """
    try:
        cursor = db[os.getenv('MONGO_COLLECTION_NAME')].find({}, {'_id': 0})
        return json.loads(dumps(cursor))
    except Exception as e:
        logging.error(f"Error al obtener todos los puntos WiFi: {e}")
        return jsonify({"error": str(e)}), 500

# Función para obtener puntos WiFi de manera paginada.
@with_db
def get_wifi_points(db, page=1, per_page=10):
    """
    Obtiene puntos WiFi de la colección de manera paginada. Utiliza los parámetros `page` y `per_page`
    para determinar el conjunto de resultados a retornar.
    """
    skips = per_page * (page - 1)
    cursor = db[os.getenv('MONGO_COLLECTION_NAME')].find().skip(skips).limit(per_page)
    return json.loads(dumps(cursor))

# Función para obtener puntos WiFi por colonia.
@with_db
def get_wifi_points_by_colonia(db, colonia, page=1, per_page=10):
    """
    Realiza una búsqueda de puntos WiFi por el nombre de la colonia. Soporta paginación de resultados.
    Es útil para filtrar puntos WiFi dentro de una ubicación específica.
    """
    skips = per_page * (page - 1)
    cursor = db[os.getenv('MONGO_COLLECTION_NAME')].find({'colonia': colonia}).skip(skips).limit(per_page)
    return json.loads(dumps(cursor))

# Función para buscar puntos WiFi cercanos a una ubicación geográfica dada.
@with_db
def get_wifi_points_near(db, lat, lng, page=1, per_page=10):
    """
    Utiliza una consulta geoespacial para encontrar puntos WiFi cercanos a una ubicación dada
    especificada por latitud y longitud. Soporta paginación para limitar el número de resultados.
    """
    skips = per_page * (page - 1)
    cursor = db[os.getenv('MONGO_COLLECTION_NAME')].find({
        'location': {
            '$near': {
                '$geometry': {
                    'type': "Point",
                    'coordinates': [lng, lat]
                }
            }
        }
    }).skip(skips).limit(per_page)
    return json.loads(dumps(cursor))

# Función para obtener un punto WiFi específico por su ID.
@with_db
def get_wifi_point_by_id(db, point_id):
    """
    Busca un punto WiFi específico utilizando su ObjectId. Esto permite recuperar detalles
    completos de un punto WiFi individual basado en su identificador único.
    """
    wifi_point = db[os.getenv('MONGO_COLLECTION_NAME')].find_one({'_id': ObjectId(point_id)})
    return json.loads(dumps(wifi_point))