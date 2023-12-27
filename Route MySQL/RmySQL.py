from conn import connect_to_mysql, Error
from flask import Flask, request, jsonify
import json
app = Flask(__name__)
@app.route('/client', methods=['POST'])
def ajouter_client():
    data = request.json
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            sql = "INSERT INTO Clients (Nom, Prenom, Email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['nom'], data['prenom'], data['email']))
            connection.commit()
            return jsonify({'message': 'Client ajouté avec succès', 'id': cursor.lastrowid}), 201
    except Exception as e:
        print("Erreur lors de l'opération sur la base de données:", e)
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/clients', methods=['GET'])
def obtenir_clients():
    try:
        connection = connect_to_mysql('localhost','user', '', 'RCS')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Clients")
            clients = cursor.fetchall()
            return jsonify(clients), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération des clients: {e}"}), 500
    finally:
        connection.close()

@app.route('/Mettre_a_jour_client', methods=['PUT'])
def update_client():
    data = request.json
    email = data.get('email')
    nom = data.get('nom')
    prenom = data.get('prenom')

    if not all([email, nom, prenom]):
        return jsonify({'error': 'Données manquantes'}), 400

    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            # Assurez-vous que la requête SQL est correctement formatée
            sql = "UPDATE Clients SET Nom = %s, Prenom = %s WHERE Email = %s"
            cursor.execute(sql, (nom, prenom, email))
        connection.commit()
        return jsonify({'message': 'Client mis à jour avec succès'}), 200
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/deleteClient/<Email>', methods=['DELETE'])
def supprimer_client(Email):
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Clients WHERE Email = %s", (Email,))
        connection.commit()
        return jsonify({'message': 'Client supprimé'}), 200
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"message": f"Erreur lors de la suppression du client: {e}"}), 500
    finally:
        if connection:
            connection.close()

@app.route('/supprimer_tous_les_clients', methods=['DELETE'])
def supprimer_tous_les_clients():
    connection = None
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Clients")
        connection.commit()
        return jsonify({"message": "Tous les clients ont été supprimés"}), 200
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"message": f"Erreur lors de la suppression des clients: {e}"}), 500
    finally:
        if connection:
            connection.close()

@app.route('/id', methods=['POST'])
def obtenir_client_id():
    data = request.get_json()
    email = data.get('email')
    try:
        connection = connect_to_mysql('localhost', 'user','', 'RCS')
        with connection.cursor() as cursor:
            sql = "SELECT ID_Client FROM Clients WHERE Email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            if result:
                return jsonify({'id_client': result[0]}), 200
            else:
                return jsonify({'message': 'Client non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()
@app.route('/update-client', methods=['PATCH'])
def update_client_in_mysql():
    data = request.json
    email = data.get('email')
    id_mongo = data.get('id_mongo')
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            sql = "UPDATE Clients SET ID_MongoClient = %s WHERE Email = %s"
            cursor.execute(sql, (id_mongo, email))
        connection.commit()
        return jsonify({'message': 'Client mis à jour avec succès'}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/statut_Con', methods=['GET'])
def statut_check():
    return jsonify({"status": "ok"}), 200

@app.route('/ajouter_journal', methods=['POST'])
def ajouter_journal():
    data = request.json
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            sql = "INSERT INTO historique (Type_Modification, ID_Client) VALUES (%s, %s)"
            cursor.execute(sql, (data['type_modification'], data['id_client']))
        connection.commit()
        return jsonify({'message': 'Entrée de journal ajoutée'}), 201
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/obtenir_journal', methods=['GET'])
def obtenir_journal():
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM historique")
            journal = cursor.fetchall()
        return jsonify(journal), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/supprimer_journal', methods=['DELETE'])
def supprimer_journal():
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM historique") 
            connection.commit()  
        return jsonify({"message": "Journal supprimé avec succès"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/GetClient/<int:id_client>', methods=['GET'])
def obtenir_client(id_client):
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            query = "SELECT * FROM Clients WHERE ID_Client = %s"
            cursor.execute(query, (id_client,))
            client = cursor.fetchone()
            if client:
                return jsonify(client), 200
            else:
                return jsonify({"message": "Client non trouvé"}), 404
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération du client: {e}"}), 500
    finally:
        if connection:
            connection.close()

@app.route('/supprimer_journal/<int:id_client>', methods=['DELETE'])
def supprimer_journal_par_id(id_client):
    try:
        connection = connect_to_mysql('localhost', 'user', '', 'RCS')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM historique WHERE id_client = %s", (id_client,))
            connection.commit()
        return jsonify({"message": "Entrée de journal supprimée avec succès pour l'ID client: " + str(id_client)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)