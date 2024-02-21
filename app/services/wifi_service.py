from pymongo import MongoClient, GEOSPHERE
from ..db.connection import mongo_client
from bson.objectid import ObjectId
from bson.json_util import dumps
from functools import partial
from flask import jsonify
import json

# Establecer conexión a la base de datos como una función de orden superior
def with_db(func):
    def wrapper(*args, **kwargs):
        db = mongo_client.get_db()  # get_db es una función idempotente
        return func(db, *args, **kwargs)
    return wrapper

@with_db
def get_all_wifi_points(db):
    print("entrando")
    try:
        cursor = db['wifi_points'].find({}, {'_id': 0})
        
        wifi_points_text = dumps(cursor)
        wifi_points_json = json.loads(wifi_points_text)
        return wifi_points_json
    except Exception as e:
        return jsonify({"error": str(e)}),500

@with_db
def get_wifi_points(db, page=1, per_page=10):
    skips = per_page * (page - 1)
    wifi_points_text = dumps(db.wifi_points.find().skip(skips).limit(per_page))
    wifi_points_json = json.loads(wifi_points_text)
    return wifi_points_json

@with_db
def get_wifi_point_by_id(db, point_id):
    wifi_point_text = dumps(db.wifi_points.find_one({'_id': ObjectId(point_id)}))
    wifi_point_json = json.loads(wifi_point_text)
    return wifi_point_json

@with_db
def get_wifi_points_by_colonia(db, colonia, page=1, per_page=10):
    skips = per_page * (page - 1)
    return list(db.wifi_points.find({'colonia': colonia}).skip(skips).limit(per_page))

@with_db
def get_wifi_points_near(db, lat, lng, page=1, per_page=10):
    skips = per_page * (page - 1)
    return list(db.wifi_points.find({
        'location': {
            '$near': {
                '$geometry': {
                    'type': "Point",
                    'coordinates': [lng, lat]
                }
            }
        }
    }).skip(skips).limit(per_page))
