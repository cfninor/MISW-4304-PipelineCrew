# PipelineCrew API - Blacklist Management

API REST desarrollada con Flask para gestionar una lista negra de correos electrónicos. El servicio permite registrar correos bloqueados, consultar si un correo existe en la blacklist y validar la disponibilidad de la aplicación y de la base de datos.

## Integrantes

| Nombre | Correo | Usuario Git |
| --- | --- | --- |
| Alejandra Bravo | a.bravo@uniandes.edu.co | [AlejandraBV](https://github.com/AlejandraBV) |
| Martin Flores | r.floresa@uniandes.edu.co | [mflores831](https://github.com/mflores831) |
| Carlos Niño | cf.ninor1@uniandes.edu.co | [cfninor](https://github.com/cfninor) |
| Juan Rodriguez | j.rodriguezg@uniandes.edu.co | [jrodrgom](https://github.com/jrodrgom) |

## Descripción

La solución expone endpoints protegidos con JWT para:

- agregar un correo a la blacklist;
- consultar si un correo ya fue bloqueado;

La persistencia se realiza sobre PostgreSQL y el despliegue reportado para la entrega fue ejecutado en AWS.

## Stack Tecnológico

- Python 3
- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Marshmallow
- Flask-JWT-Extended
- PostgreSQL
- Gunicorn
- Pytest

## Contenido del Repositorio

| Ruta | Descripción |
| --- | --- |
| `application.py` | Punto de entrada de la aplicación Flask. |
| `app/` | Código principal de la API: configuración, modelos, recursos y esquemas. |
| `init_db.py` | Script para crear la base de datos y las tablas en PostgreSQL. |
| `test_db.py` | Script simple para validar la conexión a PostgreSQL. |
| `generate_token.py` | Genera un token JWT de prueba para consumo local. |
| `tests.py` | Pruebas funcionales de los endpoints principales. |
| `Procfile` | Configuración del proceso web para despliegues tipo plataforma. |
| `PipelineCrew - Blacklist API.postman_collection.json` | Colección de Postman para probar la API. |
| `Entrega1/Proyecto 1 entrega 1 - Documento.docx` | Documento principal de la entrega con el detalle del despliegue en AWS. |
| `Entrega1/Evidencias/AWS_Beanstalk/` | Evidencias del despliegue y configuración en Elastic Beanstalk. |
| `Entrega1/Evidencias/AWS_RDS/` | Evidencias de configuración de Amazon RDS. |
| `README.md` | Borrador o versión previa de documentación. |

## Estructura General

```text
MISW-4304-PipelineCrew/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── resources.py
│   └── schemas.py
├── Entrega1/
│   ├── Evidencias/
│   │   ├── AWS_Beanstalk/
│   │   └── AWS_RDS/
│   └── Proyecto 1 entrega 1 - Documento.docx
├── application.py
├── demo.py
├── generate_token.py
├── init_db.py
├── PipelineCrew - Blacklist API.postman_collection.json
├── Procfile
├── quick_test.py
├── README.md
├── README-UPDATED.md
├── requirements.txt
├── test_db.py
└── tests.py
```

## Variables de Entorno

La aplicación toma la configuración desde variables de entorno. Si no se definen, utiliza valores por defecto pensados para desarrollo local.

Puede crear el archivo .env para que utilice las variables configuradas.

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/blacklist_db
JWT_SECRET_KEY=super-secret-key
JWT_ACCESS_TOKEN_EXPIRES=31536000
SQLALCHEMY_TRACK_MODIFICATIONS=False

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
```

## Ejecución Local

### Prerrequisitos

- Python 3.8 o superior
- PostgreSQL disponible localmente
- `pip`

### Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/cfninor/MISW-4304-PipelineCrew.git
cd MISW-4304-PipelineCrew
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Base de Datos

Crear la base de datos y las tablas:

```bash
python init_db.py
```

Si se desea validar conectividad antes de iniciar la aplicación:

```bash
python test_db.py
```

Si no se cuenta con PostgreSQL instalado localmente, se puede usar Docker:

```bash
docker run --name postgres-local \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=blacklist_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:16
```

### Levantar la API

Modo desarrollo:

```bash
python application.py
```

Con este comando la aplicación inicia en `http://localhost:5000`.

Modo Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 application:application
```

Este modo es útil si se quiere trabajar en `http://localhost:5000`, por ejemplo para usar herramientas o scripts auxiliares que asumen ese puerto.

## Endpoints

Los endpoints `POST /blacklists` y `GET /blacklists/<email>` requieren un token JWT en el header `Authorization: Bearer <token>`.

| Método | Endpoint | Descripción |
| --- | --- | --- |
| `GET` | `/generate-token` | Genera un token JWT para pruebas. |
| `POST` | `/blacklists` | Agrega un correo a la lista negra. |
| `GET` | `/blacklists/<email>` | Consulta si un correo existe en la lista negra. |
| `GET` | `/health` | Verifica el estado de la aplicación y de la base de datos. |

### Ejemplo de payload para `POST /blacklists`

```json
{
  "email": "usuario@test.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "fraude"
}
```

### Ejemplo de respuesta exitosa

```json
{
  "msg": "Email agregado exitosamente a la lista negra",
  "data": {
    "id": 1,
    "email": "usuario@test.com",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "blocked_reason": "fraude",
    "ip_address": "127.0.0.1",
    "created_at": "2026-04-12T10:00:00"
  }
}
```

## Pruebas

Pruebas funcionales automatizadas:

```bash
pytest tests.py -v
```

Pruebas manuales con Postman:

- Colección local: [`PipelineCrew - Blacklist API.postman_collection.json`](./PipelineCrew%20-%20Blacklist%20API.postman_collection.json)
- Documentación publicada en Postman: <https://documenter.getpostman.com/view/48225661/2sBXitD7Yb>

También se incluyen scripts auxiliares como `generate_token.py`, `quick_test.py` y `demo.py` para apoyo en validaciones locales.

## Despliegue en AWS

La ejecución reportada para esta entrega fue realizada en **AWS**, utilizando:

- **Elastic Beanstalk** para el despliegue de la aplicación Flask.
- **Amazon RDS for PostgreSQL** para la base de datos.

El objetivo de este README no es duplicar el paso a paso completo del aprovisionamiento y despliegue. Ese detalle quedó documentado en el archivo:

- [`Entrega1/Proyecto 1 entrega 1 - Documento.docx`](./Entrega1/Proyecto%201%20entrega%201%20-%20Documento.docx)

En ese documento se encuentran los pasos de:

- configuración de RDS;
- creación de roles en AWS;
- configuración del proyecto en Elastic Beanstalk;
- ajustes de health checks;
- despliegue y pruebas;
- estrategias de despliegue `All-at-once`, `Rolling`, `Rolling with additional batch` e `Immutable`.

Como respaldo adicional, el repositorio incluye evidencias visuales en:

- [`Entrega1/Evidencias/AWS_Beanstalk/`](./Entrega1/Evidencias/AWS_Beanstalk/)
- [`Entrega1/Evidencias/AWS_RDS/conf_RDS.png`](./Entrega1/Evidencias/AWS_RDS/conf_RDS.png)

## Notas

- `Procfile` está incluido para el proceso `web` usado en despliegue.
- La ruta `/health` permite validar rápidamente que la aplicación responde y que la base de datos está disponible.
- El modelo `Blacklist` registra correo, `app_uuid`, motivo de bloqueo, IP de origen y fecha de creación.
