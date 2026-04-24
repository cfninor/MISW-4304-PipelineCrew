from flask import Flask
from sqlalchemy import text
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

    # Priorizar la URL de la base de datos de las variables de entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/blacklist_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    from app.resources import BlacklistResource, BlacklistEmailResource, TokenGeneratorResource
    api.add_resource(TokenGeneratorResource, "/generate-token")
    api.add_resource(BlacklistResource, "/blacklists")
    api.add_resource(BlacklistEmailResource, "/blacklists/<string:email>")

    # No ejecutar db.create_all() si se está en TESTING
    # Los tests se encargan de crear sus propias tablas en memoria
    if not app.config.get('TESTING'):
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                print(f"Error inicializando DB: {e}")

    return app