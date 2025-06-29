import streamlit as st
import pandas as pd
from datetime import date

# Configuration de la page
st.set_page_config(page_title="Bankily App", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    users = pd.read_csv("user.csv")
    points = pd.read_csv("point.csv")
    try:
        saisies = pd.read_csv("saisies.csv")
    except:
        saisies = pd.DataFrame(columns=[
            "date", "nom_point", "agent_code", "liquidite",
            "portefeuille", "gain_perte", "statut", "statut_couleur"
        ])
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

                        new_row = {
                            "date": str(date_saisie),
                            "nom_point": point["nom_point"],
                            "agent_code": code,
                            "liquidite": liquidite,
                            "portefeuille": portefeuille,
                            "gain_perte": gain_perte,
                            "statut": statut,
                            "statut_couleur": couleur
                        }
                        saisies = pd.concat([saisies, pd.DataFrame([new_row])], ignore_index=True)
                        saisies.to_csv("saisies.csv", index=False)
                        st.success(f"Saisie enregistrée ({statut} {couleur})")

                    # Affichage des saisies précédentes
                    st.markdown("### 📊 Historique des saisies")
                    st.dataframe(saisies[saisies["agent_code"] == code])

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




    
