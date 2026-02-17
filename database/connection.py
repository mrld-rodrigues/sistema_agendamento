import mysql.connector
from mysql.connector import Error
from utils.config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        raise
