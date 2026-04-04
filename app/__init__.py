from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/blacklist_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    from app.resources import BlacklistResource#, BlacklistEmailResource, LoginResource

    #api.add_resource(LoginResource, "/login")
    api.add_resource(BlacklistResource, "/blacklists")
    #api.add_resource(BlacklistEmailResource, "/blacklists/<string:email>")

    with app.app_context():
        db.create_all()

    #print("DENTRO DE create_app:", app.url_map)
    return app