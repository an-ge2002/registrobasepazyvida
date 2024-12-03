import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crea una conexión a la base de datos MySQL."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost', 
            user='root',  
            password='',  
            database='registrobasepazyvida' 
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return connection