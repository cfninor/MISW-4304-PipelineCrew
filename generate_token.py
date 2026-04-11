from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "mi-clave-super-segura-devops-entrega-1-2026"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365)

jwt = JWTManager(app)

with app.app_context():
    token = create_access_token(identity="static-user")
    print(token)