import mysql.connector
from mysql.connector import Error

def connect_to_mysql(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Bon")

            return connection  # Retourne seulement l'objet connection
    except Error as e:
        print("Erreur lors de la connexion à MySQL", e)
        return None
