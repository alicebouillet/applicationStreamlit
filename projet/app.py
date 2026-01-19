import streamlit as st

# Configuration de la page 
st.set_page_config(
    page_title="Projet Streamlit – Science de la donnée",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports des pages
from pagesWeb import presentation, csv, image, texte

# Barre latérale
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("Sélectionnez un module :")

onglet = st.sidebar.radio(
    "",
    [
        "📚 Présentation du projet",
        "📊 Analyse d'un fichier CSV",
        "🔎 Analyse d'image",
        "📝 Analyse de texte"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Projet académique – INGÉ 2")

# Routing
if onglet == "📚 Présentation du projet":
    presentation.app()

elif onglet == "📊 Analyse d'un fichier CSV":
    csv.app()

elif onglet == "🔎 Analyse d'image":
    image.app()

elif onglet == "📝 Analyse de texte":
    texte.app()
