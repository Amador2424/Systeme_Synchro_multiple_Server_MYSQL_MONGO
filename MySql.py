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
            cursor = connection.cursor()
            return connection, cursor
    except Error as e:
        print("Erreur lors de la connexion à MySQL", e)
        return None, None

connection, cursor = connect_to_mysql('localhost', 'root', '','RCS')

if connection is not None and cursor is not None:
    try:
        cursor = connection.cursor()
        #cursor.execute("CREATE DATABASE RCS")
        print("Base de données créée avec succès")

        cursor.execute("USE RCS")

        cursor.execute("""
            CREATE OR REPLACE TABLE Clients (
                ID_Client INT AUTO_INCREMENT PRIMARY KEY,
                ID_MongoClient VARCHAR(255),
                Nom VARCHAR(255),
                Prenom VARCHAR(255),
                Email VARCHAR(255),
                Statut INT,
                date_création TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE OR REPLACE TABLE Commandes (
                ID_Commande INT AUTO_INCREMENT PRIMARY KEY,
                ID_MongoCommande VARCHAR(255),     
                ID_Client INT,
                Date_Commande DATE,
                Total DECIMAL(10, 2),
                FOREIGN KEY (ID_Client) REFERENCES Clients(ID_Client),
                Statut INT,
                date_création TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE OR REPLACE TABLE Produits (
                ID_Produit INT AUTO_INCREMENT PRIMARY KEY,
                ID_MongoProduit VARCHAR(255),                       
                Nom_Produit VARCHAR(255),
                Prix DECIMAL(10, 2),
                Categorie VARCHAR(255),
                Statut INT,
                date_création TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE OR REPLACE TABLE CommandeProduits (
                ID_Commande INT,
                ID_Produit INT,
                Quantite INT,
                FOREIGN KEY (ID_Commande) REFERENCES Commandes(ID_Commande),
                FOREIGN KEY (ID_Produit) REFERENCES Produits(ID_Produit),
                date_création TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE Historique (
                ID_Journal INT AUTO_INCREMENT PRIMARY KEY,
                Type_Modification ENUM('insert', 'update', 'delete'),
                ID_Client INT,
              
                Date_Modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("Tables créées avec succès")

    except mysql.connector.Error as err:
        print("Erreur lors de la création des tables: {}".format(err))

    finally:
        cursor.close()
        connection.close()
        print("Connexion MySQL est fermée")
