
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.security import add_security_headers

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register security headers
    app.after_request(add_security_headers)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.website import website_bp
    from app.routes.preview import preview_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(website_bp)
    app.register_blueprint(preview_bp)
    
    return app