# MISW-4304-PipelineCrew

1. Clonación de proyecto:

git clone https://github.com/cfninor/MISW-4304-PipelineCrew.git

2. Habilitación de entorno:

python -m venv env
env\Scripts\activate

3. Instalación de dependencias:

pip install -r requirements.txt

4. Creación de BD local blacklist_db

5. Ejecución de app: python application.py

6. Prueba en Postman:
POST http://localhost:5000/blacklists

Con bearer token:
token estático:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NTE4NzUzMywianRpIjoiYjRkMjAzZGEtNzM5Mi00OWY5LWFhZGQtNmY3ODc1MjE4NjQ2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InN0YXRpYy11c2VyIiwibmJmIjoxNzc1MTg3NTMzLCJjc3JmIjoiMjUzZTA3NjEtMDlhNy00OWNjLWE2MTAtODU0MGZiMzEwNWVmIiwiZXhwIjoxODA2NzIzNTMzfQ.RKunSY35dD-hsplYVSjYpn1TQirg4sLpu41knn2xHBI

Body de ejemplo:

{
  "email": "usuario@test.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "fraude"
}