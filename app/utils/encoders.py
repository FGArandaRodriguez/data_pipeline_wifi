import json
from bson import ObjectId

class MongoJsonEncoder(json.JSONEncoder):
    """
    Un codificador JSON personalizado para extender json.JSONEncoder, permitiendo
    la serialización de tipos adicionales no soportados por defecto.
    
    Este codificador se enfoca en convertir instancias de ObjectId, utilizadas por MongoDB
    para identificadores únicos de documentos, a strings para una correcta serialización a JSON.
    Esto es especialmente útil cuando se trabaja con Flask y MongoDB, donde los ObjectId
    necesitan ser convertidos a JSON para enviarlos en respuestas HTTP.
    """

    def default(self, obj):
        """
        Sobrescribe el método default para manejar la serialización de tipos adicionales.
        
        :param obj: El objeto a serializar.
        :return: Una representación serializable del objeto, o llama al método default
                 del padre para tipos soportados por defecto.
        """
        # Verifica si el objeto es una instancia de ObjectId.
        if isinstance(obj, ObjectId):
            # Convierte ObjectId a string para serialización JSON.
            return str(obj)
        
        # Para cualquier otro tipo, delega la serialización al método default del padre,
        # esto asegura que la extensión del codificador se mantenga compatible con
        # los tipos que el codificador predeterminado ya puede manejar.
        return super().default(obj)
