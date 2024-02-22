from flask import Flask
from flask_cors import CORS
from .utils.encoders import MongoJsonEncoder
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.json_encoder = MongoJsonEncoder
    api = Api(app, version='1.0', title='API de Puntos WiFi',
          description='Una API para gestionar puntos de acceso WiFi.')
    CORS(app)

    from .api.routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
