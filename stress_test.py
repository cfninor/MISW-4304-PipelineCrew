import asyncio
import aiohttp
import time

# localmente: http://localhost:5000
# AWS
BASE_URL = "http://LB-python-app-1781400546.us-east-2.elb.amazonaws.com" 
DURATION = 45  # Duración ráfagas en segundos
CONCURRENT_REQUESTS = 15  # Peticiones por ráfaga

async def send_traffic(session, token):
    headers = {"Authorization": f"Bearer {token}"}
    email_de_prueba = "test_stress@uniandes.edu.co"
    
    try:
        # Consulta a la lista negra
        async with session.get(f"{BASE_URL}/blacklists/{email_de_prueba}", headers=headers, timeout=5) as resp:
            pass
            
        # Verificación de salud
        async with session.get(f"{BASE_URL}/", timeout=5) as resp:
            pass
            
    except Exception:
        pass

async def main():
    print("Obteniendo Token JWT de pruebas...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/generate-token", timeout=5) as response:
                if response.status != 200:
                    print("No se pudo obtener el token de /generate-token.")
                    return
                data = await response.json()
                token = data.get("access_token")
        except Exception as e:
            print(f"Error conectando al servidor local: {e}")
            return

        print(f"Iniciando ráfagas hacia '/' y '/blacklists' durante {DURATION} segundos")
        timeout = time.time() + DURATION
        
        while time.time() < timeout:
            tasks = [send_traffic(session, token) for _ in range(CONCURRENT_REQUESTS)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)
            
    print("Prueba de estrés finalizada con éxito, revisar tablero de New Relic para métricas.")

if __name__ == "__main__":
    asyncio.run(main())