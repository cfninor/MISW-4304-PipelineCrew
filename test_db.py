import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="blacklist_db",
        user="postgres",
        password="postgres"
    )
    print("Conexión OK")
    conn.close()
except Exception as e:
    print("Error:", repr(e))