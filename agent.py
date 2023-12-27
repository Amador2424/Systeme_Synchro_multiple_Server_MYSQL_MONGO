import requests
import streamlit as st
import time
import requests
import pandas as pd
from requests.exceptions import ConnectionError, Timeout
URL_FLASK = 'http://127.0.0.1:5000/'  
URL_EXPRESS = 'http://localhost:3000/' 

def check_connection(url):
    try:
        response = requests.get(url, timeout=5) 
        if response.status_code == 200:
            return True
    except (requests.ConnectionError, requests.Timeout):
        return False
    return False

def update_client_in_mysql(email, id_mongo):
    try:
        response = requests.patch(URL_FLASK + 'update-client', json={"email": email, "id_mongo": id_mongo})
        return response.status_code == 200
    except (ConnectionError, Timeout):
        print("Erreur de connexion ou délai d'attente dépassé lors de la mise à jour du client dans MySQL.")
        return False

def update_client_in_mongo(email, id_mysql):
    try:
        response = requests.put(URL_EXPRESS + 'client/update-client', json={"email": email, "id_mysql": id_mysql})
        if response.status_code == 200:
            print(f"L'ID MySQL {id_mysql} a été mis à jour pour le client avec l'email {email}.")
            return True
        else:
            print(f"Échec de la mise à jour de l'ID MySQL pour le client avec l'email {email}. Statut: {response.status_code}, Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"Une exception s'est produite lors de la mise à jour: {e}")
        return False
def get_data_from_mysql():
    try:
        response = requests.get(URL_FLASK + 'clients')
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Impossible de récupérer les données de MySQL")
            return pd.DataFrame()
    except (ConnectionError, Timeout):
        st.error("Erreur de connexion ou délai d'attente dépassé lors de la récupération des données de MySQL.")
        return pd.DataFrame()

def get_data_from_mongo():
    try:
        response = requests.get(URL_EXPRESS + 'client/clients')
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Impossible de récupérer les données de MongoDB")
            return pd.DataFrame()
    except (ConnectionError, Timeout):
        st.error("Erreur de connexion ou délai d'attente dépassé lors de la récupération des données de MongoDB.")
        return pd.DataFrame()



def create_and_sync_clients(data):
    is_mysql_available = check_connection(URL_FLASK + 'statut_Con')
    is_mongo_available = check_connection(URL_EXPRESS + 'client/statut_Con')

    id_mysql, id_mongo = None, None

    if is_mysql_available:
        try:
            response_mysql = requests.post(URL_FLASK + 'client', json=data)
            if response_mysql.status_code == 201:
                id_mysql = response_mysql.json().get('id')
                requests.post(URL_FLASK + 'ajouter_journal', json={"type_modification": "INSERT", "id_client": id_mysql})
        except (ConnectionError, Timeout):
            print("Erreur de connexion ou délai d'attente dépassé lors de la création du client dans MySQL.")
            is_mysql_available = False

    if is_mongo_available:
        try:
            response_mongo = requests.post(URL_EXPRESS + 'client/client', json=data)
            if response_mongo.status_code == 201:
                id_mongo = response_mongo.json().get('id')
                requests.post(URL_EXPRESS + 'client/ajouter_journal', json={"typeModification": "INSERT", "id": id_mongo})
        except (ConnectionError, Timeout):
            print("Erreur de connexion ou délai d'attente dépassé lors de la création du client dans MongoDB.")
            is_mongo_available = False

    if is_mysql_available and is_mongo_available:
        if id_mysql and id_mongo:
            update_client_in_mysql(data['email'], id_mongo)
            update_client_in_mongo(data['email'], id_mysql)

    return is_mysql_available or is_mongo_available

def update_client(data):
    is_mysql_available = check_connection(URL_FLASK + 'statut_Con')
    is_mongo_available = check_connection(URL_EXPRESS + 'client/statut_Con')

    success_mysql, success_mongo = False, False

    if is_mysql_available:
        try:
            response_mysql = requests.put(URL_FLASK + 'Mettre_a_jour_client', json=data)
            if response_mysql.status_code == 200:
                response_id = requests.post(URL_FLASK + 'id', json={"email": data.get('email')})
                if response_id.status_code == 200:
                    id_mysql = response_id.json().get('id_client')
                    requests.post(URL_FLASK + 'ajouter_journal', json={"type_modification": "UPDATE", "id_client": id_mysql})
                    success_mysql = True
                else:
                    print("Erreur lors de la récupération de l'ID du client MySQL.")
            else:
                print("Erreur lors de la mise à jour du client dans MySQL.")
        except (ConnectionError, Timeout):
            print("Erreur de connexion ou délai d'attente dépassé lors de la mise à jour du client dans MySQL.")
            is_mysql_available = False
        

    if is_mongo_available:
        try:
            response_mongo = requests.put(URL_EXPRESS + 'client/mAjClient', json=data)
            if response_mongo.status_code == 200:
                requests.post(URL_EXPRESS + 'client/ajouter_journal', json={"typeModification": "UPDATE", "donnees": data})
                success_mongo = True
        except (ConnectionError, Timeout):
            print("Erreur de connexion ou délai d'attente dépassé lors de la mise à jour du client dans MongoDB.")
            is_mongo_available = False

    return success_mysql or success_mongo



def delete_user(email):
    is_mysql_available = check_connection(URL_FLASK + 'statut_Con')
    is_mongo_available = check_connection(URL_EXPRESS + 'client/statut_Con')

    success_mysql, success_mongo = False, False

    if is_mysql_available:
        try:
            response_mysql = requests.delete(URL_FLASK + f'deleteClient/{email}')      
            if response_mysql.status_code == 200:
                requests.post(URL_FLASK + 'ajouter_journal', json={"typeModification": "DELETE", "email": email})
                success_mysql = True
        except (ConnectionError, Timeout):
            print("Erreur de connexion ou délai d'attente dépassé lors de la suppression du client dans MySQL.")
            is_mysql_available = False

    if is_mongo_available:
        try:
            response_mongo = requests.delete(URL_EXPRESS + f'client/dltClient/{email}')
            if response_mongo.status_code == 200:
                requests.post(URL_EXPRESS + 'client/ajouter_journal', json={"typeModification": "DELETE", "email": email})
                success_mongo = True
        except (ConnectionError, Timeout):
            print("Erreur de connexion ou délai d'attente dépassé lors de la suppression du client dans MongoDB.")
            is_mongo_available = False


    return success_mysql or success_mongo



def synchroniser_clients():
    ids_deja_inseres = []
    a_jour = True

    try:
        reponse_historique = requests.get(URL_FLASK + 'obtenir_journal')
        historiques = reponse_historique.json()
        reponse_clients_mongo = requests.get(URL_EXPRESS + 'client/clients')
        clients_mongo = reponse_clients_mongo.json()

        for historique in historiques:
            if len(historique) > 2 :
                type_modification = historique[1]
                id_mysql = historique[2]
                if type_modification == 'insert' and id_mysql not in ids_deja_inseres:
                    reponse_client_mysql = requests.get(f'{URL_FLASK}GetClient/{id_mysql}')
                    if reponse_client_mysql.status_code == 200:
                        client_mysql = reponse_client_mysql.json()
                        nom, prenom, email = client_mysql[2], client_mysql[3], client_mysql[4]

                        if not any(client.get('id_mysql') == id_mysql for client in clients_mongo):
                            client_pour_mongo = {'nom': nom, 'prenom': prenom, 'email': email}
                            reponse_insertion = requests.post(URL_EXPRESS + 'client/client', json=client_pour_mongo)
                            if reponse_insertion.status_code == 201:
                                ids_deja_inseres.append(id_mysql)
                                print(f"Nouvelle insertion dans MongoDB pour le client {nom} {prenom}")
                                update_client_in_mongo(email, id_mysql)

                                reponse_clients_mongo = requests.get(URL_EXPRESS + 'client/clients')
                                clients_mongo = reponse_clients_mongo.json()
                                
                    else:
                        print("Erreur lors de la récupération des données du client MySQL:", reponse_client_mysql.status_code)
                        a_jour = False
                        break
                
                elif type_modification == 'update' and id_mysql not in ids_deja_inseres:

                    reponse_client_mysql = requests.get(f'{URL_FLASK}GetClient/{id_mysql}')
                    if reponse_client_mysql.status_code == 200:
                        client_mysql = reponse_client_mysql.json()
                        nom, prenom, email = client_mysql[2], client_mysql[3], client_mysql[4]
                        
                        client_mongo = next((client for client in clients_mongo if client.get('id_mysql') == id_mysql), None)
                        if client_mongo:
                            client_pour_mongo = {'nom': nom, 'prenom': prenom, 'email': email}
                            reponse_maj = requests.put(URL_EXPRESS + f'client/update-client/{client_mongo["_id"]}', json=client_pour_mongo)
                            if reponse_maj.status_code == 200:
                                print(f"Client mis à jour dans MongoDB pour {nom} {prenom}")
                            else:
                                print("Erreur lors de la mise à jour du client dans MongoDB:", reponse_maj.status_code)
                                a_jour = False
                                break
                        else:
                            print("Client correspondant à l'ID MySQL non trouvé dans MongoDB:", id_mysql)

                    else:
                        print("Erreur lors de la récupération des données du client MySQL pour mise à jour:", reponse_client_mysql.status_code)
                        a_jour = False
                        break
            response_suppression = requests.delete(URL_FLASK + 'supprimer_journal/' + str(id_mysql))
            if response_suppression.status_code == 200:
                print("Entrée de journal supprimée pour l'ID client:", id_mysql)
            else:
                print("Erreur lors de la suppression de l'entrée de journal pour l'ID client:", id_mysql)


        if a_jour:
            print("Toutes les données sont synchronisées et à jour.")
        else:
            print("Certaines données n'ont pas pu être synchronisées.")

    except ConnectionError:
        print("Erreur de connexion avec le serveur.")
        return False
    except Timeout:
        print("Délai d'attente dépassé lors de la connexion au serveur.")
        return False
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        return False
    return True



def main():
    while True:
        synchroniser_clients()
        time.sleep(5) 

if __name__ == "__main__":
    main()