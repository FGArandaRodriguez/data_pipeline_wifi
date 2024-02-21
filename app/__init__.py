from flask import Flask
from flask_cors import CORS
from .utils.encoders import MongoJsonEncoder

def create_app():
    app = Flask(__name__)
    app.json_encoder = MongoJsonEncoder
    CORS(app)

    from .api.routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
