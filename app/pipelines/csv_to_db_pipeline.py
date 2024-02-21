from pymongo import GEOSPHERE
from pymongo.errors import CollectionInvalid
import pandas as pd
from pymongo.errors import BulkWriteError

def load_data_to_mongodb(csv_file_path, db):
    collection_name = 'wifi_points'
    try:
        db.create_collection(collection_name)
        print(f"Colección '{collection_name}' creada exitosamente.")
    except CollectionInvalid:
        print(f"La colección '{collection_name}' ya existe.")
    collection = db['wifi_points']

    # Lectura del archivo CSV
    data = pd.read_csv(csv_file_path)

    # Ajustamos el formato a formato GeoJSON
    data['location'] = data.apply(lambda row: {'type': 'Point', 'coordinates': [row['longitud'], row['latitud']]}, axis=1)

    # Conversión del DataFrame a un formato de diccionario para su inserción en MongoDB
    data_dict = data.to_dict("records")

    response = {
        "inserted_count": 0,
        "index_created": False,
        "error": None
    }

    try:
        # Inserción de los datos en MongoDB
        result = collection.insert_many(data_dict)
        response["inserted_count"] = len(result.inserted_ids)
        
        # Crear un índice 2dsphere para consultas geoespaciales
        collection.create_index([("location", GEOSPHERE)])
        response["index_created"] = True
    except BulkWriteError as bwe:
        response["error"] = "Error al insertar los documentos: " + str(bwe.details)
    except Exception as e:
        response["error"] = "Ocurrió un error: " + str(e)

    return response