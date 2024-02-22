from app.pipelines.csv_to_db_pipeline import load_data_to_mongodb
from app.db.connection import mongo_client

"""
Clase para ejecutar el pipeline que carga datos desde un archivo CSV a MongoDB. 
"""
if __name__ == '__main__':
    db = mongo_client.get_db()
    csv_file_path = './data/csv/2024-01-18-puntos_de_acceso_wifi.csv'
    load_data_to_mongodb(csv_file_path,db)
