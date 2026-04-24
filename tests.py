"""
Tests funcionales para los endpoints de la API
Requisitos: pip install pytest pytest-flask
"""
import pytest
import json
from app import create_app, db
from app.models import Blacklist
from flask_jwt_extended import create_access_token
from datetime import timedelta
from uuid import uuid4

@pytest.fixture
def app():
    """Crear aplicación de prueba con base de datos en memoria para CI/CD"""
    app = create_app()
    app.config['TESTING'] = True
    # Importante: Usar SQLite en memoria para que el pipeline no dependa de un Postgres externo
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente para hacer requests HTTP"""
    return app.test_client()

@pytest.fixture
def token(app):
    """Generar token JWT válido para los tests que requieren @jwt_required"""
    with app.app_context():
        token = create_access_token(
            identity="test-user",
            expires_delta=timedelta(hours=1)
        )
        return token

class TestTokenGeneratorResource:
    """REQUERIMIENTO: Escenario de prueba para el endpoint /generate-token"""
    
    def test_generate_token_success(self, client):
        """Test: Validar que el endpoint genera un token correctamente"""
        response = client.get('/generate-token')
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert data['msg'] == 'Token generado exitosamente'

class TestBlacklistResource:
    """REQUERIMIENTO: Escenarios para POST /blacklists"""
    
    def test_post_valid_blacklist_entry(self, client, token):
        """Test: Agregar un email válido"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'test@example.com',
                'app_uuid': str(uuid4()),
                'blocked_reason': 'Actividad sospechosa'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['data']['email'] == 'test@example.com'

    def test_post_missing_email(self, client, token):
        """Test: Caso email vacío o faltante"""
        response = client.post(
            '/blacklists',
            json={'app_uuid': str(uuid4())},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400
        assert 'email es obligatorio' in response.get_json()['msg']

    def test_post_invalid_email_format(self, client, token):
        """Test: Formato de email no válido"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'esto-no-es-un-email',
                'app_uuid': str(uuid4())
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 400
        assert 'formato válido' in response.get_json()['msg']

    def test_post_duplicate_email(self, client, token, app):
        """Test: Evitar duplicados (Falla lógica)"""
        payload = {
            'email': 'dupe@test.com',
            'app_uuid': str(uuid4()),
            'blocked_reason': 'Spam'
        }
        # Primer registro
        client.post('/blacklists', json=payload, headers={'Authorization': f'Bearer {token}'})
        # Segundo intento
        response = client.post('/blacklists', json=payload, headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 409

class TestBlacklistEmailResource:
    """REQUERIMIENTO: Escenarios para GET /blacklists/<email>"""
    
    def test_get_existing_email(self, client, app, token):
        """Test: Consultar email existente"""
        email = 'found@test.com'
        with app.app_context():
            item = Blacklist(email=email, app_uuid=str(uuid4()), ip_address='127.0.0.1')
            db.session.add(item)
            db.session.commit()
        
        response = client.get(f'/blacklists/{email}', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert response.get_json()['exists'] is True

    def test_get_invalid_format(self, client, token):
        """Test: GET con formato de email inválido"""
        response = client.get('/blacklists/email-incorrecto', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 400

class TestSecurity:
    """Validación de seguridad para cumplimiento de integridad"""
    def test_unauthorized_access(self, client):
        """Test: Bloquear acceso sin token (si esto falla, el pipeline debe caer)"""
        response = client.post('/blacklists', json={})
        assert response.status_code == 401

if __name__ == '__main__':
    pytest.main([__file__, '-v'])