
import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION INITIALE ---
st.set_page_config(page_title='Bankily App', layout='wide')

# --- CHARGEMENT DES DONNÉES ---
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

# --- FONCTIONS DE TRADUCTION ---
def traduire(text, lang):
    trad = {
        "Connexion": {"fr": "Connexion", "ar": "تسجيل الدخول"},
        "Code d'accès": {"fr": "Code d'accès", "ar": "رمز الدخول"},
        "Accès refusé": {"fr": "Accès refusé", "ar": "تم رفض الوصول"},
        "Bienvenue": {"fr": "Bienvenue", "ar": "مرحبا"},
        "Saisie journalière": {"fr": "Saisie journalière", "ar": "الإدخال اليومي"},
        "Tableau de bord": {"fr": "Tableau de bord", "ar": "لوحة التحكم"},
    }
    return trad.get(text, {}).get(lang, text)

# --- INTERFACE DE CONNEXION ---
code_saisi = st.text_input("🔐 Code d'accès", type="password")
if code_saisi in users["code"].values:
    user_info = users[users["code"] == code_saisi].iloc[0]
    user_nom = user_info["nom"]
    user_lang = user_info["langue"]
    user_role = user_info["habilitation"]
    st.success(f"{traduire('Bienvenue', user_lang)} {user_nom} ({user_role})")

    # Charger les points associés à cet agent
    points_user = points if user_role == "Admin" else points[points["agent_code"] == code_saisi]

    # Choix de la section
    onglet = st.sidebar.radio("📂 Menu", [
        traduire("Saisie journalière", user_lang),
        traduire("Tableau de bord", user_lang)
    ])

    if onglet == traduire("Saisie journalière", user_lang):
        st.header(traduire("Saisie journalière", user_lang))
        # Formulaire à afficher ici...

    elif onglet == traduire("Tableau de bord", user_lang) and user_role == "Admin":
        st.header(traduire("Tableau de bord", user_lang))
        # Tableau d'administration à afficher ici...

else:
    if code_saisi != "":
        st.error("❌ Code invalide. " + traduire("Accès refusé", "fr"))
