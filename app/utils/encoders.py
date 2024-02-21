import json
from bson import ObjectId

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        # Delega el resto de la serialización para el tipo predeterminado
        return super().default(obj)
