# PipelineCrew - Blacklist Management API

API para gestionar una lista negra de emails con persistencia en PostgreSQL.

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio y configurar el entorno

```bash
cd MISW-4304-PipelineCrew
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar PostgreSQL

Asegurate que PostgreSQL esté corriendo en tu máquina. Puedes verificar la conexión:

```bash
python test_db.py
```

### 4. Inicializar la base de datos

```bash
python init_db.py
```

Esto creará:
- La base de datos `blacklist_db`
- La tabla `blacklists`
- Datos de prueba (opcional)

## Utilización

### 1. Generar token JWT

```bash
python generate_token.py
```

Esto imprimirá un token válido para usar en los requests.

### 2. Iniciar la aplicación

```bash
python application.py
```

La API estará disponible en `http://localhost:5000`

### 3. Probar los endpoints

#### Opción A: Prueba rápida automática

```bash
python quick_test.py
```

#### Opción B: Usar curl manualmente

```bash
# Generar token
TOKEN=$(python generate_token.py)

# POST: Agregar email a blacklist
curl -X POST http://localhost:5000/blacklists \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "attacker@suspicious.com",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "blocked_reason": "Actividad maliciosa"
  }'

# GET: Verificar si email está en blacklist
curl http://localhost:5000/blacklists/attacker@suspicious.com

# GET: Verificar email que no existe
curl http://localhost:5000/blacklists/validemail@example.com
```

#### Opción C: Usar Postman/Insomnia

1. Importar las URL de los endpoints
2. Agregar header: `Authorization: Bearer <token>`
3. Para POST: agregar body JSON con `email`, `app_uuid` y `blocked_reason`

## Endpoints

### POST /blacklists

Agregar un email a la lista negra.

**Requiere:** Token JWT

**Body:**
```json
{
  "email": "attacker@suspicious.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Actividad maliciosa"
}
```

**Respuestas:**
- `201`: Email agregado exitosamente
- `400`: Validación fallida (email/uuid inválidos)
- `409`: Email ya existe en la blacklist
- `500`: Error de base de datos

### GET /blacklists/<email>

Consultar si un email existe en la blacklist.

**Respuestas:**
- `200`: OK
  ```json
  {
    "msg": "El email está en la lista negra",
    "exists": true,
    "blocked_reason": "Actividad maliciosa",
    "blocked_at": "2024-01-15T10:30:00.123456",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
  O si no existe:
  ```json
  {
    "msg": "El email no está en la lista negra",
    "exists": false
  }
  ```
- `400`: Formato de email inválido

## Pruebas unitarias

Ejecutar las pruebas funcionales:

```bash
# Instalar pytest
pip install pytest pytest-flask

# Ejecutar tests
pytest tests.py -v
```

## Estructura del proyecto

```
.
├── application.py           # Punto de entrada
├── generate_token.py        # Generador de tokens JWT
├── init_db.py              # Inicializador de BD
├── quick_test.py           # Pruebas rápidas
├── test_db.py              # Verificación de conexión
├── tests.py                # Tests unitarios
├── requirements.txt        # Dependencias
├── .env                    # Configuración de entorno
├── .gitignore             # Archivos ignorados por git
├── README.md              # Este archivo
└── app/
    ├── __init__.py        # Inicializador (crea la app Flask)
    ├── models.py          # Modelo de datos (Blacklist)
    ├── resources.py       # Recursos/endpoints
    └── schemas.py         # Esquemas Marshmallow
```

## Configuración

### Variables de entorno (.env)

```
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blacklist_db
JWT_SECRET_KEY=super-secret-key
```

## Troubleshooting

### Error: "No module named 'app'"
- Asegúrate de estar en el directorio raíz del proyecto
- Ejecuta: `python -m venv venv` y activa el entorno

### Error: "connection refused" a PostgreSQL
- Verifica que PostgreSQL está corriendo
- Ejecuta: `python test_db.py`
- Ajusta las credenciales en `.env`

### Error: "Token expired"
- Genera un nuevo token: `python generate_token.py`

## Características implementadas

✅ Modelo de datos de blacklist en PostgreSQL  
✅ Endpoint POST para agregar emails  
✅ Endpoint GET para consultar existencia y motivo  
✅ Validación de formato de email y UUID  
✅ Autenticación con JWT  
✅ Manejo de errores y excepciones  
✅ Tests funcionales completos  
✅ Script de inicialización de BD  
✅ Documentación completa  

## Despliegue en AWS

1. Crear una instancia RDS de PostgreSQL
2. Configurar Security Groups para permitir conexiones
3. Actualizar `.env` con las credenciales de RDS
4. Ejecutar: `python init_db.py`
5. Desplegar con Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 application:application`

## Licencia

Este proyecto es parte del curso MISW-4304
