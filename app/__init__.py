from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/blacklist_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        False
    )
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "super-secret-key"
    )
    
    # Convertir a entero (segundos) desde string
    expires_seconds = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 31536000))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=expires_seconds)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    from app.resources import BlacklistResource, BlacklistEmailResource

    api.add_resource(BlacklistResource, "/blacklists")
    api.add_resource(BlacklistEmailResource, "/blacklists/<string:email>")

    with app.app_context():
        db.create_all()

    #print("DENTRO DE create_app:", app.url_map)
    return app