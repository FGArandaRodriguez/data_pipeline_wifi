from pymongo import GEOSPHERE
from pymongo.errors import CollectionInvalid
import pandas as pd
from pymongo.errors import BulkWriteError
from dotenv import load_dotenv
import os

def load_data_to_mongodb(csv_file_path, db):
    load_dotenv()
    collection_name = os.getenv('MONGO_COLLECTION_NAME')
    try:
        db.create_collection(collection_name)
        print(f"Colección '{collection_name}' creada exitosamente.")
    except CollectionInvalid:
        print(f"La colección '{collection_name}' ya existe.")
        return CollectionInvalid
        
    collection = db[os.getenv('MONGO_COLLECTION_NAME')]

    # Lectura del archivo CSV
    data = pd.read_csv(csv_file_path)

    data['longitud'] = pd.to_numeric(data['longitud'], errors='coerce')
    data['latitud'] = pd.to_numeric(data['latitud'], errors='coerce')
    data['longitud'] = data['longitud'].to_dict()
    data['latitud'] = data['latitud'].to_dict()

    data = data.dropna(subset=['latitud', 'longitud'])
    # Validar y filtrar los datos para asegurar que las coordenadas están dentro de los rangos válidos
    data = data[(data['latitud'].between(-90, 90)) & (data['longitud'].between(-180, 180))]

    # creamos los Ajustamos el formato a formato GeoJSON
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
        try:
            # Crear un índice 2dsphere para consultas geoespaciales
            resp = collection.create_index([("location", GEOSPHERE)])
            response["index_created"] = True
        except Exception as e:
            print({"error":e})
            
    except BulkWriteError as bwe:
        response["error"] = "Error al insertar los documentos: " + str(bwe.details)
    except Exception as e:
        response["error"] = "Ocurrió un error: " + str(e)

    return response