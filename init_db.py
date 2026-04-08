"""
Script para inicializar la base de datos de PostgreSQL
Crea la base de datos, las tablas y agrega datos de prueba
"""
import os
import sys
import psycopg2
from psycopg2 import sql
from app import create_app, db

def create_database():
    """Crear la base de datos en PostgreSQL"""
    try:
        # Conectar a PostgreSQL por defecto
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'blacklist_db'")
        if not cursor.fetchone():
            print("Creando base de datos 'blacklist_db'...")
            cursor.execute("CREATE DATABASE blacklist_db")
            print("✓ Base de datos creada exitosamente")
        else:
            print("✓ Base de datos 'blacklist_db' ya existe")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"✗ Error conectando a PostgreSQL: {e}")
        sys.exit(1)

def initialize_tables():
    """Crear las tablas en la base de datos"""
    try:
        app = create_app()
        
        with app.app_context():
            print("Creando tablas...")
            db.create_all()
            print("✓ Tablas creadas exitosamente")
            
    except Exception as e:
        print(f"✗ Error creando las tablas: {e}")
        sys.exit(1)

def seed_database():
    """Agregar datos de prueba a la base de datos (opcional)"""
    try:
        app = create_app()
        
        with app.app_context():
            from app.models import Blacklist
            
            # Verificar si ya existen datos de prueba
            count = Blacklist.query.count()
            if count == 0:
                print("Agregando datos de prueba...")
                
                test_data = [
                    {
                        "email": "spam@example.com",
                        "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
                        "blocked_reason": "Envío de spam",
                        "ip_address": "192.168.1.1"
                    },
                    {
                        "email": "malicious@example.com",
                        "app_uuid": "550e8400-e29b-41d4-a716-446655440001",
                        "blocked_reason": "Actividad maliciosa detectada",
                        "ip_address": "192.168.1.2"
                    }
                ]
                
                for item in test_data:
                    blacklist_item = Blacklist(**item)
                    db.session.add(blacklist_item)
                
                db.session.commit()
                print("✓ Datos de prueba agregados")
            else:
                print(f"✓ Base de datos ya contiene {count} registros")
                
    except Exception as e:
        print(f"✗ Error agregando datos de prueba: {e}")
        db.session.rollback()

def main():
    """Ejecutar la inicialización completa"""
    print("\n" + "="*50)
    print("INICIALIZACIÓN DE BASE DE DATOS")
    print("="*50 + "\n")
    
    create_database()
    initialize_tables()
    
    # Descomentar para agregar datos de prueba
    # seed_database()
    
    print("\n" + "="*50)
    print("✓ Inicialización completada")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
