"""
Script rápido para probar los endpoints localmente
Uso: python quick_test.py
"""
import requests
import json
from uuid import uuid4

BASE_URL = "http://localhost:5000"

def get_token():
    """Generar un token JWT ejecutando generate_token.py"""
    import subprocess
    result = subprocess.run(['python', 'generate_token.py'], capture_output=True, text=True)
    token = result.stdout.strip()
    return token

def test_api():
    """Ejecutar pruebas rápidas de los endpoints"""
    
    print("\n" + "="*60)
    print("PRUEBAS RÁPIDAS DE API")
    print("="*60 + "\n")
    
    # Obtener token
    print("1. Generando token JWT...")
    try:
        token = get_token()
        if not token:
            print("   ✗ No se pudo generar el token")
            return
        print(f"   ✓ Token generado: {token[:30]}...")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: POST - Agregar email a blacklist
    print("\n2. POST /blacklists - Agregar email a blacklist")
    test_email = "attacker@suspicious.com"
    test_uuid = str(uuid4())
    
    payload = {
        "email": test_email,
        "app_uuid": test_uuid,
        "blocked_reason": "Actividad maliciosa detectada"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/blacklists",
            json=payload,
            headers=headers,
            timeout=5
        )
        if response.status_code == 201:
            data = response.json()
            print(f"   ✓ Email agregado: {data['data']['email']}")
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ✗ Error de conexión: {e}")
        print("      ¿Está corriendo: python application.py?")
        return
    
    # Test 2: GET - Verificar si email existe
    print(f"\n3. GET /blacklists/{test_email} - Consultar si existe en blacklist")
    try:
        response = requests.get(
            f"{BASE_URL}/blacklists/{test_email}",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data['exists']:
                print(f"   ✓ Email EN BLACKLIST")
                print(f"     Motivo: {data['blocked_reason']}")
            else:
                print(f"   ✓ Email NO está en blacklist")
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ✗ Error de conexión: {e}")
        return
    
    # Test 3: GET - Email que no existe
    print(f"\n4. GET /blacklists/validemail@example.com - Email válido pero no en blacklist")
    try:
        response = requests.get(
            f"{BASE_URL}/blacklists/validemail@example.com",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data['exists']:
                print(f"   ✓ Email EN BLACKLIST")
            else:
                print(f"   ✓ Email NO está en blacklist")
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ✗ Error de conexión: {e}")
        return
    
    # Test 4: Error - Email inválido
    print(f"\n5. GET /blacklists/invalidemail - Email con formato inválido")
    try:
        response = requests.get(
            f"{BASE_URL}/blacklists/invalidemail",
            timeout=5
        )
        if response.status_code == 400:
            print(f"   ✓ Validación correcta: {response.json()['msg']}")
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ✗ Error de conexión: {e}")
        return
    
    print("\n" + "="*60)
    print("✓ Pruebas completadas exitosamente")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_api()
