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
    """Crear aplicación de prueba"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente para hacer requests"""
    return app.test_client()

@pytest.fixture
def token(app):
    """Generar token JWT válido"""
    with app.app_context():
        token = create_access_token(
            identity="test-user",
            expires_delta=timedelta(hours=1)
        )
        return token

class TestBlacklistResource:
    """Tests para POST /blacklists"""
    
    def test_post_valid_blacklist_entry(self, client, token):
        """Test: Agregar un email válido a la blacklist"""
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
        assert data['msg'] == 'Email agregado exitosamente a la lista negra'
        assert data['data']['email'] == 'test@example.com'

    def test_post_missing_email(self, client, token):
        """Test: Falta email obligatorio"""
        response = client.post(
            '/blacklists',
            json={
                'app_uuid': str(uuid4()),
                'blocked_reason': 'Spam'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert 'email es obligatorio' in response.get_json()['msg']

    def test_post_invalid_email_format(self, client, token):
        """Test: Formato de email inválido"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'invalid-email',
                'app_uuid': str(uuid4()),
                'blocked_reason': 'Spam'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert 'email no tiene un formato válido' in response.get_json()['msg']

    def test_post_missing_app_uuid(self, client, token):
        """Test: Falta app_uuid obligatorio"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'test@example.com',
                'blocked_reason': 'Spam'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert 'app_uuid es obligatorio' in response.get_json()['msg']

    def test_post_invalid_uuid_format(self, client, token):
        """Test: Formato UUID inválido"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'test@example.com',
                'app_uuid': 'not-a-uuid',
                'blocked_reason': 'Spam'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert 'UUID válido' in response.get_json()['msg']

    def test_post_blocked_reason_too_long(self, client, token):
        """Test: blocked_reason supera 255 caracteres"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'test@example.com',
                'app_uuid': str(uuid4()),
                'blocked_reason': 'x' * 256
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400
        assert '255 caracteres' in response.get_json()['msg']

    def test_post_duplicate_email(self, client, token, app):
        """Test: No se puede agregar un email duplicado"""
        with app.app_context():
            # Agregar el primer email
            response1 = client.post(
                '/blacklists',
                json={
                    'email': 'duplicate@example.com',
                    'app_uuid': str(uuid4()),
                    'blocked_reason': 'Spam'
                },
                headers={'Authorization': f'Bearer {token}'}
            )
            assert response1.status_code == 201
            
            # Intentar agregar el mismo email
            response2 = client.post(
                '/blacklists',
                json={
                    'email': 'duplicate@example.com',
                    'app_uuid': str(uuid4()),
                    'blocked_reason': 'Otro motivo'
                },
                headers={'Authorization': f'Bearer {token}'}
            )
            assert response2.status_code == 409
            assert 'ya está en la lista negra' in response2.get_json()['msg']

    def test_post_without_token(self, client):
        """Test: No permitir POST sin token JWT"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'test@example.com',
                'app_uuid': str(uuid4()),
                'blocked_reason': 'Spam'
            }
        )
        
        assert response.status_code == 401

    def test_post_empty_body(self, client, token):
        """Test: Body vacío"""
        response = client.post(
            '/blacklists',
            json={},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 400


class TestBlacklistEmailResource:
    """Tests para GET /blacklists/<email>"""
    
    def test_get_existing_email(self, client, app, token):
        """Test: Obtener email que existe en blacklist"""
        with app.app_context():
            # Agregar un email a la base de datos
            blacklist_item = Blacklist(
                email='existing@example.com',
                app_uuid='550e8400-e29b-41d4-a716-446655440000',
                blocked_reason='Envío de spam',
                ip_address='192.168.1.1'
            )
            db.session.add(blacklist_item)
            db.session.commit()
        
        response = client.get('/blacklists/existing@example.com',  headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['exists'] is True
        assert data['blocked_reason'] == 'Envío de spam'

    def test_get_non_existing_email(self, client, token):
        """Test: Email que no existe en blacklist"""
        response = client.get('/blacklists/nonexisting@example.com',  headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['exists'] is False

    def test_get_invalid_email_format(self, client, token):
        """Test: Formato de email inválido en GET"""
        response = client.get('/blacklists/invalid-email',  headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 400
        assert 'email no tiene un formato válido' in response.get_json()['msg']

    def test_get_without_token(self, client):
        """Test: No permitir GET sin token JWT"""
        response = client.get('/blacklists/test@example.com')
        
        assert response.status_code == 401


class TestDatabasePersistence:
    """Tests para verificar la persistencia en base de datos"""
    
    def test_data_persists_after_commit(self, client, token, app):
        """Test: Los datos se persisten en la BD después del commit"""
        # Agregar un email
        response = client.post(
            '/blacklists',
            json={
                'email': 'persist@example.com',
                'app_uuid': str(uuid4()),
                'blocked_reason': 'Test persistencia'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 201
        
        # Verificar que existe en la BD
        with app.app_context():
            item = Blacklist.query.filter_by(email='persist@example.com').first()
            assert item is not None
            assert item.blocked_reason == 'Test persistencia'

    def test_ip_address_is_recorded(self, client, token, app):
        """Test: La dirección IP se registra correctamente"""
        response = client.post(
            '/blacklists',
            json={
                'email': 'iptest@example.com',
                'app_uuid': str(uuid4()),
                'blocked_reason': 'Test IP'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        with app.app_context():
            item = Blacklist.query.filter_by(email='iptest@example.com').first()
            assert item.ip_address is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
