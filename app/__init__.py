from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.security import add_security_headers

jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # MongoDB setup
    mongo_uri = app.config.get("MONGO_URI")
    if not mongo_uri:
        raise ValueError("Missing MONGO_URI in config")

    mongo_client = MongoClient(mongo_uri)
    app.mongo_client = mongo_client
    app.db = mongo_client["growthzi"]  # your DB name

    # Attach to global scope via import
    from app.db import init_db
    init_db(app.db)

    # Initialize JWT and CORS
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.after_request(add_security_headers)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.website import website_bp
    from app.routes.preview import preview_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(website_bp)
    app.register_blueprint(preview_bp)

    return app