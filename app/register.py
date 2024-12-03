import bcrypt
import mysql.connector
from mysql.connector import Error
from db_connector import create_connection

def login(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insertar el nuevo usuario en la base de datos
    sql = "INSERT INTO login (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (username, hashed_password))
        connection.commit()
        print("Usuario registrado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Ejemplo de uso
if __name__ == "__main__":
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    login(username, password)