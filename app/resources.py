from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import re

from app import db
from app.models import Blacklist
from app.schemas import blacklist_schema

def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def is_valid_uuid(value):
    try:
        UUID(value)
        return True
    except ValueError:
        return False

class BlacklistResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            if not data:
                    return {"msg": "El body de la solicitud debe estar en formato JSON"}, 400


            email = data.get("email")
            app_uuid = data.get("app_uuid")
            blocked_reason = data.get("blocked_reason", "")
            
            #validacion de email
            if not email:
                return {"msg": "email es obligatorio"}, 400
            
            if not isinstance(email, str) or not is_valid_email(email):
                return {"msg": "email no tiene un formato válido"}, 400

            #validacion de app_uuid
            if not app_uuid:
                return {"msg": "app_uuid es obligatorio"}, 400
            
            if not isinstance(app_uuid, str) or not is_valid_uuid(app_uuid):
                return {"msg": "app_uuid no tiene un formato UUID válido"}, 400
        
            # Validación de blocked_reason
            if blocked_reason is None:
                blocked_reason = ""

            if not isinstance(blocked_reason, str):
                return {"msg": "blocked_reason debe ser texto"}, 400

            if len(blocked_reason) > 255:
                return {"msg": "blocked_reason no puede superar 255 caracteres"}, 400

            #validacion de duplicado
            existing = Blacklist.query.filter_by(email=email).first()
            if existing:
                return {"msg": "El email ya está en la lista negra"}, 409

            item = Blacklist(
                email=email,
                app_uuid=app_uuid,
                blocked_reason=blocked_reason,
                ip_address=request.remote_addr or "unknown"
            )

            db.session.add(item)
            db.session.commit()

            return {
                "msg": "Email agregado exitosamente a la lista negra",
                "data": blacklist_schema.dump(item)
            }, 201
            
        except SQLAlchemyError:
            db.session.rollback()
            return {"msg": "Error al guardar en la base de datos"}, 500

        except Exception:
            return {"msg": "Error interno del servidor"}, 500


class BlacklistEmailResource(Resource):
    def get(self, email):
        """Consultar si un email existe en la blacklist"""
        try:
            # Validar formato de email
            if not is_valid_email(email):
                return {"msg": "email no tiene un formato válido"}, 400

            # Buscar el email en la blacklist
            blacklist_item = Blacklist.query.filter_by(email=email).first()
            
            if blacklist_item:
                return {
                    "msg": "El email está en la lista negra",
                    "exists": True,
                    "blocked_reason": blacklist_item.blocked_reason,
                    "blocked_at": blacklist_item.created_at.isoformat(),
                    "app_uuid": blacklist_item.app_uuid
                }, 200
            else:
                return {
                    "msg": "El email no está en la lista negra",
                    "exists": False
                }, 200
                
        except Exception:
            return {"msg": "Error interno del servidor"}, 500


class TokenGeneratorResource(Resource):
    """Generar token JWT para usar en otros endpoints"""
    def get(self):
        try:
            token = create_access_token(identity="static-user")
            return {
                "msg": "Token generado exitosamente",
                "access_token": token
            }, 200
        except Exception:
            return {"msg": "Error al generar el token"}, 500
        