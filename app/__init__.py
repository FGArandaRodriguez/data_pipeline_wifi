from flask import Flask,jsonify
from flask_cors import CORS
from .utils.encoders import MongoJsonEncoder
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os

def create_app():
    app = Flask(__name__)
    app.json_encoder = MongoJsonEncoder

    CORS(app)

    # Configure Swagger UI
    SWAGGER_URL = '/swagger'
    API_URL = 'http://127.0.0.1:5000/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
    )

    from .api.routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    @app.route('/swagger.json')
    def swagger():
       CORS(app)
       dir_path = os.path.dirname(os.path.realpath(__file__))
       swagger_path = os.path.join(dir_path, 'swagger.json')
       with open(swagger_path, 'r') as f:
           return jsonify(json.load(f))

    return app
