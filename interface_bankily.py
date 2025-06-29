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

# Interface de connexion
st.sidebar.image("bankily.JPG", width=150)
st.sidebar.title("🔐 Connexion")

login_input = st.sidebar.text_input("Identifiant (login)", max_chars=10)
password_input = st.sidebar.text_input("Mot de passe (code)", type="password")

if login_input and password_input:
    try:
        login_int = int(login_input)
        cursor.execute("SELECT * FROM users WHERE login=? AND code=?", (login_int, password_input))
        user_data = cursor.fetchone()

        if user_data:
            login, code, nom, langue, role = user_data
            st.success(f"Bienvenue {nom} ({role})")

            if role == "Utilisateur":
                st.header("📋 Saisie quotidienne")
                cursor.execute("SELECT * FROM points WHERE agent_code=?", (code,))
                point_data = cursor.fetchone()

                if point_data:
                    nom_point, agent_code, capital = point_data
                    st.subheader(f"Point : {nom_point}")

                    with st.form("form_saisie"):
                        date_saisie = st.date_input("Date", value=date.today())
                        liquidite = st.number_input("Liquidité", min_value=0.0, step=100.0)
                        portefeuille = st.number_input("Portefeuille", min_value=0.0, step=100.0)
                        gain_perte = st.number_input("Gain / Perte", step=100.0)
                        submit = st.form_submit_button("Valider")

                    if submit:
                        total = liquidite + portefeuille
                        statut = "OK" if total == capital else "Erreur"
                        couleur = "🟢" if statut == "OK" else "🔴"

                        cursor.execute('''INSERT INTO saisies VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                            str(date_saisie), nom_point, code, liquidite, portefeuille, gain_perte, statut, couleur
                        ))
                        conn.commit()
                        st.success(f"Saisie enregistrée ({statut} {couleur})")

                    # Affichage des saisies précédentes
                    st.markdown("### 📊 Historique des saisies")
                    df = pd.read_sql_query("SELECT * FROM saisies WHERE agent_code=?", conn, params=(code,))
                    st.dataframe(df)
                else:
                    st.warning("Aucun point associé à ce compte.")

            elif role == "Admin":
                st.header("👨‍💼 Tableau de bord Admin")
                st.subheader("Utilisateurs")
                df_users = pd.read_sql_query("SELECT * FROM users", conn)
                st.dataframe(df_users)

                st.subheader("Points")
                df_points = pd.read_sql_query("SELECT * FROM points", conn)
                st.dataframe(df_points)

                st.subheader("Saisies")
                df_saisies = pd.read_sql_query("SELECT * FROM saisies", conn)
                st.dataframe(df_saisies)

        else:
            st.error("Identifiants incorrects.")

    except ValueError:
        st.error("Identifiant invalide.")
else:
    st.info("Veuillez saisir vos identifiants pour accéder.")
