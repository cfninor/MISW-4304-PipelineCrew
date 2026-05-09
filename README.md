# PipelineCrew API - Blacklist Management

API REST desarrollada con Flask para gestionar una lista negra de correos electrónicos. El servicio permite registrar correos bloqueados, consultar si un correo existe en la blacklist y validar la disponibilidad de la aplicación y de la base de datos.

## Integrantes

| Nombre | Correo | Usuario Git |
| --- | --- | --- |
| Alejandra Bravo | a.bravo@uniandes.edu.co | [AlejandraBV](https://github.com/AlejandraBV) |
| Martin Flores | r.floresa@uniandes.edu.co | [mflores831](https://github.com/mflores831) |
| Carlos Niño | cf.ninor1@uniandes.edu.co | [cfninor](https://github.com/cfninor) |
| Juan Rodriguez | j.rodriguezg@uniandes.edu.co | [jrodrgom](https://github.com/jrodrgom) |

## Entregables

| Entregable | Enlace |
|---|---|
| Video sustentación entrega 1 | [Ver video](https://youtu.be/jiFlagqQxyo) |
| Video sustentación entrega 2 | [Ver video](https://youtu.be/HmSQma7Fmjg) |
| Documento entrega 1 | [Entrega1/Proyecto 1 entrega 1 - Documento.pdf](./Entrega1/Proyecto%201%20entrega%201%20-%20Documento.pdf) |
| Documento entrega 2 | [Entrega2/Proyecto 1 entrega 2 - Documento.pdf](./Entrega2/Proyecto%201%20entrega%202%20-%20Documento.pdf) |
| Documento entrega 3 | [Entrega3/Proyecto 1 entrega 3 - Documento.pdf](./Entrega3/Proyecto%201%20entrega%203%20-%20Documento.pdf) |
| Documentación Postman | [Ver documentación](https://documenter.getpostman.com/view/48225661/2sBXitD7Yb) |
| Collection | [Ver collection](./PipelineCrew%20-%20Blacklist%20API.postman_collection.json) |
| Repositorio GitHub | [Ver repositorio](https://github.com/cfninor/MISW-4304-PipelineCrew) |

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
| `buildspec.yml` | Configuración de fases y comandos para la construcción automatizada en AWS CodeBuild (incluye pruebas unitarias, build y push de la imagen). |
| `Dockerfile` | Define la construcción de la imagen Docker del microservicio (runtime, dependencias y comando de ejecución). |
| `appspec.json` | Archivo de configuración para AWS CodeDeploy que define cómo se realiza el despliegue en ECS/Fargate. |
| `taskdef.json` | Definición de la tarea ECS (CPU, memoria, contenedor, imagen y variables de entorno) usada en el despliegue. |
| `PipelineCrew - Blacklist API.postman_collection.json` | Colección de Postman para probar la API. |
| `Entrega1/Proyecto 1 entrega 1 - Documento.docx` | Documento principal de la entrega con el detalle del despliegue en AWS. |
| `Entrega1/Evidencias/AWS_Beanstalk/` | Evidencias del despliegue y configuración en Elastic Beanstalk. |
| `Entrega1/Evidencias/AWS_RDS/` | Evidencias de configuración de Amazon RDS. |
| `Entrega2/` | Carpeta con los documentos correspondientes a la segunda entrega. |
| `Entrega2/Proyecto 1 entrega 2 - Documento.docx` | Documento principal de la entrega 2. |
| `Entrega3/Proyecto 1 entrega 3 - Documento.docx` | Documento principal de la entrega 3. |
| `README.md` | Documentación general del proyecto. |

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
├── Entrega2/
│   └── Proyecto 1 entrega 2 - Documento.docx
├── Entrega3/
│   └── Proyecto 1 entrega 3 - Documento.docx
├── application.py
├── appspec.json
├── buildspec.yml
├── demo.py
├── Dockerfile
├── generate_token.py
├── init_db.py
├── PipelineCrew - Blacklist API.postman_collection.json
├── Procfile
├── quick_test.py
├── README.md
├── requirements.txt
├── taskdef.json
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
- Documentación publicada en Postman: <https://documenter.getpostman.com/view/34079512/2sBXqNkxz8>

También se incluyen scripts auxiliares como `generate_token.py`, `quick_test.py` y `demo.py` para apoyo en validaciones locales.

## Integración Continua

El proyecto cuenta con un pipeline de integración continua configurado en **AWS CodePipeline** y **AWS CodeBuild**.

El pipeline se ejecuta automáticamente ante cambios en la rama `main` del repositorio y realiza las siguientes actividades:

- Instalación de dependencias del proyecto.
- Ejecución de pruebas automatizadas (pytest).
- Construcción de la imagen Docker del microservicio.
- Publicación de la imagen en **Amazon ECR (Elastic Container Registry)**.

La configuración de las fases de construcción se encuentra en:

- [`buildspec.yml`](./buildspec.yml)

Este proceso garantiza que solo versiones validadas del código continúen hacia el despliegue.


## Entrega Continua

Posterior a una ejecución exitosa del proceso de integración continua, el pipeline realiza el despliegue automático del microservicio utilizando:

- **AWS CodeDeploy**
- **Amazon ECS con Fargate**

El despliegue se realiza mediante una estrategia **blue/green**, permitiendo actualizar la aplicación sin afectar la disponibilidad del servicio.

Los archivos de configuración asociados al despliegue son:

- [`buildspec.yml`](./buildspec.yml): Define la configuración de la tarea ECS (contenedor, recursos, variables de entorno).
- [`appspec.json`](./appspec.json): Define el proceso de despliegue en CodeDeploy.
- [`Dockerfile`](./Dockerfile): Define la construcción de la imagen del contenedor.


## Despliegue en AWS

La solución desplegada en esta entrega utiliza los siguientes servicios de **AWS**:

- **Amazon ECS (Fargate)** para la ejecución del contenedor de la aplicación.
- **Amazon ECR** para el almacenamiento de la imagen Docker.
- **Application Load Balancer (ALB)** para exponer el servicio.
- **Amazon RDS for PostgreSQL** para la base de datos relacional.

A diferencia de la entrega 2, donde se utilizaba **Elastic Beanstalk** con despliegue basado en artefactos .zip, en esta versión se adopta una arquitectura basada en contenedores, lo que permite:

- Mayor portabilidad del microservicio.
- Despliegues más controlados y escalables.
- Separación clara entre build y runtime.
- Integración nativa con servicios modernos de AWS (ECS + Fargate).

El objetivo de este README no es duplicar el paso a paso completo del aprovisionamiento y despliegue. Dicho detalle, incluyendo la configuración inicial en AWS y la implementación del pipeline de integración continua, fue documentado en las entregas previas:

- [`Entrega2/Proyecto 1 entrega 2 - Documento.pdf`](./Entrega2/Proyecto%201%20entrega%202%20-%20Documento.pdf)
- [`Entrega1/Proyecto 1 entrega 1 - Documento.pdf`](./Entrega1/Proyecto%201%20entrega%201%20-%20Documento.pdf)

En este último documento se encuentran los pasos de:

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
- `buildspec.yml` define las fases de instalación, preconstrucción, construcción y posconstrucción para la automatización del pipeline.
- La ruta `/health` permite validar rápidamente que la aplicación responde y que la base de datos está disponible.
- El modelo `Blacklist` registra correo, `app_uuid`, motivo de bloqueo, IP de origen y fecha de creación.
