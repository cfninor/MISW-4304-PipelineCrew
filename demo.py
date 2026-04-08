#!/usr/bin/env python
"""
Script de demostración de uso de la API
Simula diferentes casos de uso
"""

import requests
import json
from uuid import uuid4

# Configuración
BASE_URL = "http://localhost:5000"

# Colores para la consola
class Colors:
    OK = '\033[92m'
    ERROR = '\033[91m'
    INFO = '\033[94m'
    WARNING = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_title(text):
    print(f"\n{Colors.BOLD}{Colors.INFO}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.OK}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.ERROR}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.INFO}ℹ {text}{Colors.RESET}")

def get_token():
    """Obtener token JWT"""
    import subprocess
    try:
        result = subprocess.run(
            ['python', 'generate_token.py'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print_error(f"No se pudo generar token: {e}")
    return None

def demo_case_1(token):
    """Caso 1: Agregar un email sospechoso a la blacklist"""
    print_title("CASO 1: Agregar email a blacklist (POST)")
    
    email = "malware@suspicious.ru"
    app_uuid = str(uuid4())
    
    print_info(f"Email: {email}")
    print_info(f"App UUID: {app_uuid}")
    print_info(f"Motivo: Detectada distribución de malware")
    
    payload = {
        "email": email,
        "app_uuid": app_uuid,
        "blocked_reason": "Detectada distribución de malware"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/blacklists",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success("Email agregado a la blacklist")
            print(f"  ID: {data['data']['id']}")
            print(f"  Email: {data['data']['email']}")
            print(f"  IP: {data['data']['ip_address']}")
            return email
        else:
            print_error(f"Error {response.status_code}: {response.json()['msg']}")
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")
    
    return None

def demo_case_2(token, email=None):
    """Caso 2: Consultar si un email está en la blacklist"""
    print_title("CASO 2: Consultar email en blacklist (GET)")
    
    if not email:
        email = "attacker@malicious.com"
        print_info(f"Usando email de ejemplo: {email}")
    else:
        print_info(f"Consultando email agregado anteriormente")
    
    try:
        response = requests.get(
            f"{BASE_URL}/blacklists/{email}",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['exists']:
                print_error(f"ALERTA: Email ({email}) está en la blacklist")
                print(f"  Motivo: {data['blocked_reason']}")
                print(f"  Fecha: {data['blocked_at']}")
                print(f"  App: {data['app_uuid']}")
            else:
                print_success(f"Email ({email}) no está en la blacklist")
        else:
            print_error(f"Error {response.status_code}: {response.json()['msg']}")
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")

def demo_case_3(token):
    """Caso 3: Intentar agregar email duplicado"""
    print_title("CASO 3: Validación - Email duplicado")
    
    email = "spam@phishing.net"
    app_uuid = str(uuid4())
    
    payload = {
        "email": email,
        "app_uuid": app_uuid,
        "blocked_reason": "Primera adición"
    }
    
    # Primera adición
    print_info("Primer intento: agregando email...")
    try:
        response = requests.post(
            f"{BASE_URL}/blacklists",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 201:
            print_success("Email agregado")
        else:
            print_error(f"Error: {response.json()['msg']}")
            return
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")
        return
    
    # Segundo intento (duplicado)
    print_info("Segundo intento: intentando agregar el mismo email...")
    payload["blocked_reason"] = "Intento de duplicado"
    
    try:
        response = requests.post(
            f"{BASE_URL}/blacklists",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 409:
            print_success("Validación correcta - Duplicado rechazado")
            print(f"  Mensaje: {response.json()['msg']}")
        else:
            print_error(f"Error: Debería haber sido 409 pero fue {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")

def demo_case_4(token):
    """Caso 4: Validaciones de entrada"""
    print_title("CASO 4: Validaciones de entrada")
    
    # Test 1: Email inválido
    print_info("Test 1: Email con formato inválido")
    payload = {
        "email": "invalidemail",
        "app_uuid": str(uuid4()),
        "blocked_reason": "Test"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/blacklists",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 400:
            print_success(f"Validación correcta: {response.json()['msg']}")
        else:
            print_error(f"Error: Debería rechazar email inválido")
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")
    
    # Test 2: UUID inválido
    print_info("Test 2: UUID con formato inválido")
    payload = {
        "email": "test@valid.com",
        "app_uuid": "not-a-uuid",
        "blocked_reason": "Test"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/blacklists",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        if response.status_code == 400:
            print_success(f"Validación correcta: {response.json()['msg']}")
        else:
            print_error(f"Error: Debería rechazar UUID inválido")
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión: {e}")

def main():
    """Ejecutar demostración completa"""
    print(f"\n{Colors.BOLD}{Colors.INFO}")
    print("╔────────────────────────────────────────────────────────╗")
    print("║  DEMOSTRACIÓN DE API - BLACKLIST MANAGEMENT             ║")
    print("║  MISW-4304 Pipeline Crew - Persona 2                   ║")
    print("╚────────────────────────────────────────────────────────╝")
    print(f"{Colors.RESET}")
    
    # Verificar si servidor está corriendo
    print_info("Verificando conexión al servidor...")
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
    except requests.exceptions.ConnectionError:
        print_error(f"No se puede conectar a {BASE_URL}")
        print_info("¿Está corriendo la aplicación?")
        print_info("Ejecuta: python application.py")
        return
    except Exception:
        pass  # El servidor puede retornar 404, eso es OK
    
    print_success(f"Conectado a {BASE_URL}")
    
    # Generar token
    print_info("Generando token JWT...")
    token = get_token()
    if not token:
        print_error("No se pudo generar el token")
        print_info("Asegúrate de tener generate_token.py disponible")
        return
    print_success("Token generado")
    
    # Ejecutar casos de demostración
    email_agregado = demo_case_1(token)
    demo_case_2(token, email_agregado)
    demo_case_3(token)
    demo_case_4(token)
    
    # Resumen final
    print_title("DEMOSTRACIÓN COMPLETADA")
    print(f"{Colors.OK}✓ Todos los casos fueron ejecutados{Colors.RESET}\n")
    print("Endpoints disponibles:")
    print(f"  {Colors.INFO}POST /blacklists{Colors.RESET}         - Agregar email a blacklist (requiere JWT)")
    print(f"  {Colors.INFO}GET /blacklists/<email>{Colors.RESET}  - Consultar si email está en blacklist\n")

if __name__ == "__main__":
    main()
