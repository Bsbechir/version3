import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import os

# Configuration de la page
st.set_page_config(page_title="Bankily App", layout="wide")

# Connexion à la base SQLite
conn = sqlite3.connect("bankily.db")
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    login INTEGER PRIMARY KEY,
    code TEXT,
    nom TEXT,
    langue TEXT,
    habilitation TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS points (
    nom_point TEXT,
    agent_code TEXT,
    capital REAL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS saisies (
    date TEXT,
    nom_point TEXT,
    agent_code TEXT,
    liquidite REAL,
    portefeuille REAL,
    gain_perte REAL,
    statut TEXT,
    statut_couleur TEXT
)''')
conn.commit()

# Chargement des données
def load_data():
    users = pd.read_sql_query("SELECT * FROM users", conn)
    points = pd.read_sql_query("SELECT * FROM points", conn)
    saisies = pd.read_sql_query("SELECT * FROM saisies", conn)
    return users, points, saisies

users, points, saisies = load_data()

# Interface de connexion
st.sidebar.image("bankily.JPG", width=150)
st.sidebar.title("🔐 Connexion")

login_input = st.sidebar.text_input("Identifiant (login)", max_chars=10)
password_input = st.sidebar.text_input("Mot de passe (code)", type="password")

if login_input and password_input:
    try:
        login_int = int(login_input)
        user_row = users[(users["login"] == login_int) & (users["code"] == password_input)]
        if not user_row.empty:
            user = user_row.iloc[0]
            nom = user["nom"]
            langue = user["langue"]
            role = user["habilitation"]
            code = user["code"]

            st.success(f"Bienvenue {nom} ({role})")

            # Récupérer les points associés
            user_points = points[points["agent_code"] == code]

            if role == "Utilisateur":
                st.header("📋 Saisie quotidienne")
                if user_points.empty:
                    st.warning("Aucun point associé à ce compte.")
                else:
                    point = user_points.iloc[0]
                    st.subheader(f"Point : {point['nom_point']}")

                    with st.form("form_saisie"):
                        date_saisie = st.date_input("Date", value=date.today())
                        liquidite = st.number_input("Liquidité", min_value=0.0, step=100.0)
                        portefeuille = st.number_input("Portefeuille", min_value=0.0, step=100.0)
                        gain_perte = st.number_input("Gain / Perte", step=100.0)
                        submit = st.form_submit_button("Valider")

                    if submit:
                        capital = point["capital"]
                        total = liquidite + portefeuille
                        statut = "OK" if total == capital else "Erreur"
                        couleur = "🟢" if statut == "OK" else "🔴"

                        cursor.execute('''INSERT INTO saisies VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                            str(date_saisie), point["nom_point"], code, liquidite, portefeuille, gain_perte, statut, couleur
                        ))
                        conn.commit()
                        st.success(f"Saisie enregistrée ({statut} {couleur})")

                    # Affichage des saisies précédentes
                    st.markdown("### 📊 Historique des saisies")
                    saisies = pd.read_sql_query("SELECT * FROM saisies WHERE agent_code=?", conn, params=(code,))
                    st.dataframe(saisies)

            elif role == "Admin":
                st.header("👨‍💼 Tableau de bord Admin")
                st.subheader("Utilisateurs")
                st.dataframe(users)
                st.subheader("Points")
                st.dataframe(points)
                st.subheader("Saisies")
                st.dataframe(saisies)

        else:
            st.error("Identifiants incorrects.")
    except ValueError:
        st.error("Identifiant invalide.")
else:
    st.info("Veuillez saisir vos identifiants pour accéder.")

