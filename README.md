# PipelineCrew API - Blacklist Management

## Integrantes
| Nombre | Correo | Usuario Git |
|--------| ------- | ------------- |
| Alejandra Bravo | a.bravo@uniandes.edu.co | [AlejandraBV](https://github.com/AlejandraBV) |
| Martin Flores | r.floresa@uniandes.edu.co | [mflores831](https://github.com/mflores831)
| Carlos Niño | cf.ninor1@uniandes.edu.co | [cfninor](https://github.com/cfninor)|
| Juan Rodriguez | j.rodriguezg@uniandes.edu.co | [jrodrgom](https://github.com/jrodrgom)

## Descripción

Esta es una API REST desarrollada con Flask para la gestión de listas negras de correos electrónicos. Permite agregar correos a una lista negra con razones de bloqueo y consultar si un correo está bloqueado. Utiliza autenticación JWT para proteger los endpoints y PostgreSQL como base de datos.

## Objetivo

El objetivo de este proyecto es proporcionar una solución segura y eficiente para gestionar listas negras de correos electrónicos en aplicaciones, permitiendo bloquear usuarios por razones como fraude, spam u otras políticas de seguridad.

## Características

- **Autenticación JWT**: Protección de endpoints con tokens JWT.
- **Gestión de Blacklist**: Agregar y consultar correos en la lista negra.
- **Validaciones**: Validación de formato de email y UUID.
- **Base de Datos**: PostgreSQL para persistencia de datos.
- **API RESTful**: Endpoints bien definidos con respuestas JSON.

## Prerrequisitos

- Python 3.8 o superior
- PostgreSQL instalado y ejecutándose
- Git

## Instalación

1. **Clonación del proyecto**:
   ```bash
   git clone https://github.com/cfninor/MISW-4304-PipelineCrew.git
   cd MISW-4304-PipelineCrew
   ```

2. **Creación del entorno virtual**:
   ```bash
   python -m venv env
   source env/bin/activate  # En macOS/Linux
   # env\Scripts\activate  # En Windows
   ```

3. **Instalación de dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración de la base de datos**:
   - Asegúrate de que PostgreSQL esté ejecutándose.
   - Crea una BD con el nombre: blacklist_db
   - Si tienes docker y no tienes PostgreSQL, puedes usar el siguiente comando:
   ```bash
    docker run --name postgres-local \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=blacklist_db \
    -p 5432:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    -d postgres:16
   ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables (opcional, usa valores por defecto si no se especifican):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blacklist_db
JWT_SECRET_KEY=mi-clave-super-segura-devops-entrega-1-2026
JWT_ACCESS_TOKEN_EXPIRES=31536000
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
```

## Ejecución de la Aplicación

1. **Modo desarrollo**:
   ```bash
   python application.py
   ```
   La aplicación se ejecutará en `http://localhost:5000`.

2. **Modo producción** (con Gunicorn):
   ```bash
   gunicorn --bind 0.0.0.0:5000 application:application
   ```

## Endpoints de la API

### Generar Token JWT
- **GET** `/generate-token`
- Descripción: Genera un token de acceso para usar en otros endpoints.
- Respuesta:
  ```json
  {
    "msg": "Token generado exitosamente",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

### Agregar a Blacklist
- **POST** `/blacklists`
- Headers: `Authorization: Bearer <token>`
- Body:
  ```json
  {
    "email": "usuario@test.com",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "blocked_reason": "fraude"
  }
  ```
- Respuesta exitosa (201):
  ```json
  {
    "msg": "Email agregado exitosamente a la lista negra",
    "data": {
      "id": 1,
      "email": "usuario@test.com",
      "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
      "blocked_reason": "fraude",
      "ip_address": "127.0.0.1",
      "created_at": "2023-10-01T12:00:00"
    }
  }
  ```

### Consultar Blacklist por Email
- **GET** `/blacklists/<email>`
- Headers: `Authorization: Bearer <token>`
- Respuesta si existe:
  ```json
  {
    "msg": "El email está en la lista negra",
    "exists": true,
    "blocked_reason": "fraude",
    "blocked_at": "2023-10-01T12:00:00",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- Respuesta si no existe:
  ```json
  {
    "msg": "El email no está en la lista negra",
    "exists": false
  }
  ```

## Pruebas

### Ejecutar Tests
```bash
pytest tests.py -v
```

### Prueba con Postman
1. Importa la colección `PipelineCrew-API.postman_collection.json` en Postman.
2. Genera un token usando el endpoint `/generate-token`.
3. El token generado ya se utilizará en los headers por medio de una variable.

Ejemplo de request POST:
- URL: `http://localhost:5001/blacklists`
- Headers: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Body: JSON como arriba.

Token estático de ejemplo:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTkzMTU2MCwianRpIjoiOGMxYTZiYzQtYWFiNy00OGVhLThlODMtYWU5ZTY0ODJmY2FhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InN0YXRpYy11c2VyIiwibmJmIjoxNzc1OTMxNTYwLCJjc3JmIjoiMmMzOTU5Y2MtNWFmZC00ODI2LWExMjctYmY2ZjlkNTg1YWMwIiwiZXhwIjoxODA3NDY3NTYwfQ.FygqAdIliS2H4tysNWpZgj7k_yg7XwxdCt2JQeHTTks
```

## Estructura del Proyecto

```
MISW-4304-PipelineCrew/
├── application.py          # Punto de entrada de la app
├── init_db.py              # Script de inicialización de BD
├── requirements.txt        # Dependencias
├── Procfile                
├── app/
│   ├── __init__.py         # Configuración de Flask
│   ├── models.py           # Modelos de BD
│   ├── resources.py        # Endpoints de la API
│   └── schemas.py          # Esquemas de serialización
├── tests.py                # Tests unitarios
└── README.md               # Este archivo
```