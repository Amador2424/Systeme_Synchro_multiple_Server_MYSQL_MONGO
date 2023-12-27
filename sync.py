import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from agent import (check_connection, get_data_from_mysql, create_and_sync_clients, get_data_from_mongo, update_client, delete_user, synchroniser_clients)
import threading
URL_FLASK = 'http://127.0.0.1:5000/'
URL_EXPRESS = 'http://localhost:3000/'

status_mysql = st.empty()
status_mongo = st.empty()



if synchroniser_clients():
        st.info("Synchronisation réussie.")
else:
        st.info("Un serveur est hors d'état")

if check_connection(URL_FLASK + "statut_Con"):
    status_mysql.markdown("MySQL: ![Active](https://img.shields.io/badge/status-active-green)")
else:
    status_mysql.markdown("MySQL: Problème de connexion ")

if check_connection(URL_EXPRESS + "client/statut_Con"):
    status_mongo.markdown("MongoDB: ![Active](https://img.shields.io/badge/status-active-green)")
else:
    status_mongo.markdown("MongoDB: Problème de connexion")

#obtenir_journal
st.title("Synchronisation des Clients entre MySQL et MongoDB")

with st.form(key='client_form'):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    submit_button = st.form_submit_button("Créer et Synchroniser")

    if submit_button and nom and prenom and email:
        success = create_and_sync_clients({"nom": nom, "prenom": prenom, "email": email})
        if success:
            st.success("Client créé et synchronisé avec succès.")
        else:
            st.error("Échec de la création ou de la synchronisation du client.")

def start_synchronisation():
    thread = threading.Thread(target=synchroniser_clients)
    thread.start()

# Dans votre application Streamlit
start_synchronisation()
if st.button("Voir les données MySQL"):
    df_mysql = get_data_from_mysql()
    st.write("Données MySQL:")
    st.dataframe(df_mysql)

if st.button("Voir les données MongoDB"):
    df_mongo = get_data_from_mongo()
    st.write("Données MongoDB:")
    st.dataframe(df_mongo)

st.title("Mise à jour des Clients dans MySQL et MongoDB")

with st.form(key='update_form'):
    email = st.text_input("Email du client (identifiant unique)")
    nom = st.text_input("Nouveau nom")
    prenom = st.text_input("Nouveau prénom")
    update_button = st.form_submit_button("Mettre à jour le client")

    if update_button and email:
        success = update_client({"email": email, "nom": nom, "prenom": prenom})
        if success:
            st.success("Client mis à jour avec succès dans les deux bases de données.")
        else:
            st.error("Échec de la mise à jour du client.")

st.title("Suppression d'un utilisateur dans MySQL et MongoDB")

email = st.text_input("Email de l'utilisateur à supprimer")
delete_button = st.button("Supprimer l'utilisateur")

if delete_button and email:
    success = delete_user(email)
    if success:
        st.success("Utilisateur supprimé avec succès dans les deux bases de données.")
    else:
        st.error("Échec de la suppression de l'utilisateur.")
