import streamlit as st
# Configuration de la page
st.set_page_config(
        page_title="Projet Streamlit – Science de la donnée",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def app():

    # Titre principal
    st.markdown(
        """
        <h1 style="text-align:center;">Projet Streamlit</h1>
        """,
        unsafe_allow_html=True
    )

    # Sous-titre
    st.markdown(
        """
        <h3 style="text-align:center; color:grey;">
        Projet académique – Deuxième année d'école d'ingénieur  
        <br>
        Cycle <b>Science de la donnée</b>
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Contexte
    st.markdown(
        """
        ### 📌 Contexte du projet

        Cette application a été développée dans le cadre du cours  
        **« Approfondissement Python »**, avec pour objectif de :

        - Mettre en pratique la programmation Python orientée données  
        - Découvrir le développement d’applications interactives avec **Streamlit**
        - Manipuler différents types de données : tabulaires, textuelles et visuelles
        """
    )

    st.divider()

    # Fonctionnalités
    st.markdown(
        """
        ### ⚙️ Fonctionnalités principales

        L’application est organisée autour de **trois modules indépendants**, accessibles via le menu latéral :
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            #### 📊 Analyse de données CSV
            - Import de fichiers CSV  
            - Validation des données
            - Statistiques descriptives  
            - Visualisations 
            - Filtres interactifs
            """
        )

    with col2:
        st.markdown(
            """
            #### 🖼️ Traitement d’image
            - Chargement d’images  
            - Affichage et métadonnées 
            - Transformations basiques
            """
        )

    with col3:
        st.markdown(
            """
            #### 📝 Traitement de texte
            - Import de fichiers texte  
            - Nettoyage et prétraitement
            - Statistiques textuelles
            - Analyse de sentiment
            """
        )

    st.divider()

    # Footer
    st.markdown(
        """
        <p style="text-align:center; color:grey;">
        Application développée avec <b>Python</b> et <b>Streamlit</b>  
        <br>
        © Projet étudiant – École d’ingénieur
        </p>
        """,
        unsafe_allow_html=True
    )
