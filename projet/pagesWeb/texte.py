import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re
import string
from collections import Counter
from io import BytesIO
# Configuration de la page
st.set_page_config(
        page_title="Projet Streamlit – Analyse de Texte",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def app():

    # Titre principal
    st.markdown(
        """
        <h1 style="text-align:center;">📝 Analyse et Traitement de Texte</h1>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Instructions pour l'utilisateur
    st.markdown(
        """
        ### 📂 Importez votre texte

        Utilisez la zone de texte ci-dessous ou importez un fichier texte.  
        L'application analysera automatiquement le texte et vous fournira diverses statistiques et analyses.   
        Si aucun texte n'est fourni, un texte par défaut sera utilisé.
        """
    )
    
    # Import du texte
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input_method = st.radio("Méthode d'importation :", ["Saisie directe", "Fichier texte", "Texte par défaut"])
        
        # Initialiser text pour éviter UnboundLocalError
        text = ""
        
        if text_input_method == "Saisie directe":
            text = st.text_area("Entrez votre texte ici :", height=200, 
                               placeholder="Tapez ou collez votre texte ici...")
        elif text_input_method == "Fichier texte":
            uploaded_file = st.file_uploader("Choisissez un fichier texte", type=["txt"])
            if uploaded_file is not None:
                text = uploaded_file.read().decode("utf-8")
                st.text_area("Aperçu du texte importé :", text, height=200)
        else:
            text = """Les pommes sont vraiment délicieuses 😍😋 je pourrais en manger tous les jours 😄
Les fraises manquent parfois de goût 😕😒 ça me déçoit un peu 😞
J'adore les bananes, c'est pratique et toujours bon 😊👍
Les oranges sont trop acides à mon goût 😖😣 je n'aime pas trop 😩
Les mangues bien mûres sont incroyables 🤩😍 un vrai plaisir 😁
Les poires sont douces et juteuses, j'en raffole absolument 🤗💚
Les cerises en été c'est le bonheur total 😍🍒
Les kiwis sont bons mais parfois trop acides pour moi 😐
Les pêches bien mûres sont un délice, j'adore ça 😋🍑
Les raisins sont pratiques à manger mais pas exceptionnels 😐🍇"""
            st.text_area("Texte par défaut :", text, height=200, key="default_text_display")
    
    with col2:
        st.info("💡 **Astuce**\n\nVous pouvez importer des textes longs, des articles, des critiques de produits, etc.")

    if not text:
        st.warning("⚠️ Veuillez entrer ou importer un texte pour commencer l'analyse.")
        return
    
    # Toujours mettre à jour le texte original avec le texte actuel
    st.session_state.original_text = text
    
    # Afficher les données dans des onglets
    tab1, tab2, tab3, tab4 = st.tabs(["🧹 Nettoyage & Prétraitement", "📊 Statistiques textuelles", "😊 Analyse de sentiment", "💾 Exporter"])
    
    # TAB 1 : NETTOYAGE & PRÉTRAITEMENT
    
    with tab1:

        colA, colB = st.columns([1, 2])

        with colA:

            if st.button("🔄 Réinitialiser (texte naturel)"):
                for k in list(st.session_state.keys()):
                    if k.startswith("clean_"):
                        st.session_state[k] = False
                st.rerun()

            st.divider()

            lowercase = st.checkbox("Minuscules", True, key="clean_lower")
            urls = st.checkbox("Supprimer URLs", True, key="clean_urls")
            emails = st.checkbox("Supprimer emails", True, key="clean_emails")
            mentions = st.checkbox("Supprimer @mentions", True, key="clean_mentions")
            hashtags = st.checkbox("Supprimer #", True, key="clean_hashtags")
            punctuation = st.checkbox("Supprimer ponctuation et emojis", True, key="clean_punct")
            numbers = st.checkbox("Supprimer chiffres", False, key="clean_numbers")
            spaces = st.checkbox("Nettoyer espaces", True, key="clean_spaces")

            st.divider()

            stopwords_opt = st.checkbox("Supprimer les stop words", False, key="clean_stopwords")

        with colB:

            cleaned_text = st.session_state.original_text

            if lowercase:
                cleaned_text = cleaned_text.lower()

            if urls:
                cleaned_text = re.sub(r"http\S+|www\S+", "", cleaned_text)

            if emails:
                cleaned_text = re.sub(r"\S+@\S+", "", cleaned_text)

            if mentions:
                cleaned_text = re.sub(r"@\w+", "", cleaned_text)

            if hashtags:
                cleaned_text = re.sub(r"#(\w+)", r"\1", cleaned_text)

            if punctuation:
                cleaned_text = re.sub(
                    r"[^\w\sàâäéèêëîïôöùûüçœ]",
                    "",
                    cleaned_text
                )

            if numbers:
                cleaned_text = re.sub(r"\d+", "", cleaned_text)

            if spaces:
                cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

            if stopwords_opt:
                french_stopwords = {
                    "le","la","les","un","une","des","du","de","et","ou","mais","donc",
                    "or","ni","car","à","en","pour","dans","sur","avec","sans","ce",
                    "ces","cet","cette","je","tu","il","elle","nous","vous","ils","elles",
                    "ne","pas","plus","moins","très","bien","mal","comme","être","avoir",
                    "fait","faites","fait","est","sont","été","a","ont"
                }
                words = cleaned_text.split()
                cleaned_text = " ".join([w for w in words if w not in french_stopwords])

            st.text_area("Texte nettoyé :", cleaned_text, height=300)

            c1, c2 = st.columns(2)
            c1.metric("Mots (avant)", len(st.session_state.original_text.split()))
            c2.metric("Mots (après)", len(cleaned_text.split()))

    # TAB 2 : STATISTIQUES TEXTUELLES
    with tab2:
        st.subheader("📊 Statistiques textuelles")
        
        # Utiliser le texte nettoyé si disponible
        analysis_text = cleaned_text if 'cleaned_text' in locals() else text
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📈 Statistiques générales")
            
            # Calculs de base
            nb_chars = len(analysis_text)
            nb_chars_no_space = len(analysis_text.replace(" ", ""))
            words = analysis_text.split()
            nb_words = len(words)
            sentences = re.split(r'[.!?]+', analysis_text)
            nb_sentences = len([s for s in sentences if s.strip()])
            
            # Affichage
            st.metric("Nombre de caractères", nb_chars)
            st.metric("Caractères (sans espaces)", nb_chars_no_space)
            st.metric("Nombre de mots", nb_words)
            st.metric("Nombre de phrases", nb_sentences)
            
            if nb_words > 0:
                avg_word_length = nb_chars_no_space / nb_words
                st.metric("Longueur moyenne des mots", f"{avg_word_length:.2f}")
            
            if nb_sentences > 0:
                avg_sentence_length = nb_words / nb_sentences
                st.metric("Mots par phrase (moyenne)", f"{avg_sentence_length:.2f}")
        
        with col2:
            st.markdown("### 🔤 Mots les plus fréquents")
            
            # Compter les mots
            word_counts = Counter(words)
            top_words = word_counts.most_common(10)
            
            if top_words:
                # Créer un graphique
                fig, ax = plt.subplots(figsize=(10, 6))
                words_list = [w[0] for w in top_words]
                counts_list = [w[1] for w in top_words]
                
                ax.barh(words_list, counts_list, color='skyblue', edgecolor='navy', alpha=0.7)
                ax.set_xlabel('Fréquence', fontsize=12, fontweight='bold')
                ax.set_ylabel('Mots', fontsize=12, fontweight='bold')
                ax.set_title('Top 10 des mots les plus utilisés', fontsize=14, fontweight='bold', pad=20)
                ax.invert_yaxis()
                
                # Ajouter les valeurs sur les barres
                for i, (word, count) in enumerate(zip(words_list, counts_list)):
                    ax.text(count, i, f' {count}', va='center', fontsize=10)
                
                # Améliorer l'espacement et éviter les chevauchements
                plt.tight_layout()
                plt.subplots_adjust(left=0.2)
                st.pyplot(fig)
            else:
                st.info("Aucun mot à afficher")

    # TAB 3 : ANALYSE DE SENTIMENT
    with tab3:
        st.subheader("😊 Analyse de sentiment")
        
        st.markdown("""
        Cette analyse combine deux méthodes :
        - **Détection d'emojis** : identification des emojis et leur sentiment
        - **Mots-clés** : analyse des mots positifs et négatifs
        """)

        # =============================
        # TEXTES DE RÉFÉRENCE
        # =============================
        sentiment_text = cleaned_text.lower()  # pour les mots
        emoji_text_source = st.session_state.original_text  # pour les emojis

        # =============================
        # Dictionnaire emoji -> sentiment
        # =============================
        emoji_sentiment = {
            "😍": "positif", "😊": "positif", "😁": "positif", "🤩": "positif", 
            "😋": "positif", "😄": "positif", "👍": "positif", "🤗": "positif",
            "💚": "positif",
            "😢": "négatif", "😠": "négatif", "😡": "négatif", "😒": "négatif",
            "😞": "négatif", "😩": "négatif", "😣": "négatif", "😖": "négatif",
            "😕": "neutre", "😐": "neutre",
        }

        # =============================
        # Dictionnaires de mots-clés
        # =============================
        positive_words = [
            'bon','bien','super','excellent','génial','parfait','top','magnifique',
            'merveilleux','fantastique','incroyable','formidable','agréable','heureux',
            'content','satisfait','bravo','réussi','succès','qualité','beau','belle',
            'adore','aime','délicieux','frais','savoureux'
        ]

        negative_words = [
            'mauvais','mal','nul','horrible','terrible','médiocre','pire','décevant',
            'catastrophe','problème','défaut','erreur','triste','malheureux','insatisfait',
            'échec','raté','laid','sale','pauvre','faible','pourri','abîmé','immangeable'
        ]

        # =============================
        # ANALYSE DES EMOJIS
        # =============================
        emoji_positive = 0
        emoji_negative = 0
        emoji_neutral = 0

        for char in emoji_text_source:
            if char in emoji_sentiment:
                if emoji_sentiment[char] == "positif":
                    emoji_positive += 1
                elif emoji_sentiment[char] == "négatif":
                    emoji_negative += 1
                else:
                    emoji_neutral += 1

        # =============================
        # ANALYSE DES MOTS
        # =============================
        words_in_text = re.findall(r"\b\w+\b", sentiment_text)

        word_positive = sum(word in positive_words for word in words_in_text)
        word_negative = sum(word in negative_words for word in words_in_text)

        # =============================
        # SCORE GLOBAL
        # =============================
        total_positive = word_positive + emoji_positive
        total_negative = word_negative + emoji_negative
        total_neutral = emoji_neutral

        if total_positive > total_negative:
            sentiment = "Positif"
            emoji_display = "😊"
            color = "#4CAF50"
        elif total_negative > total_positive:
            sentiment = "Négatif"
            emoji_display = "😞"
            color = "#F44336"
        else:
            sentiment = "Neutre"
            emoji_display = "😐"
            color = "#FFC107"

        # =============================
        # AFFICHAGE
        # =============================
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown(f"### Sentiment global : {emoji_display}")
            st.markdown(f"<h2 style='color:{color};'>{sentiment}</h2>", unsafe_allow_html=True)

            st.divider()

            st.markdown("#### 😊 Emojis")
            st.metric("Positifs", emoji_positive)
            st.metric("Négatifs", emoji_negative)
            st.metric("Neutres", emoji_neutral)

            st.divider()

            st.markdown("#### 🔤 Mots")
            st.metric("Mots positifs", word_positive)
            st.metric("Mots négatifs", word_negative)

        with col2:
            st.markdown("### Distribution des sentiments")

            fig, ax = plt.subplots(figsize=(8, 6))
            labels = [
                f"Positif 😊 ({total_positive})",
                f"Négatif 😞 ({total_negative})",
                f"Neutre 😐 ({total_neutral})"
            ]
            sizes = [
                total_positive or 0.1,
                total_negative or 0.1,
                total_neutral or 0.1
            ]
            colors = ['#4CAF50', '#F44336', '#FFC107']
            explode = (0.1, 0.1, 0)

            ax.pie(
                sizes,
                labels=labels,
                colors=colors,
                explode=explode,
                autopct='%1.1f%%',
                startangle=90,
                shadow=True,
                textprops={'fontsize': 10}
            )
            ax.axis('equal')
            st.pyplot(fig)

            st.divider()

            emojis_found = [char for char in emoji_text_source if char in emoji_sentiment]
            if emojis_found:
                st.markdown("#### Emojis détectés")
                st.markdown(
                    f"<div style='font-size:30px'>{' '.join(emojis_found)}</div>",
                    unsafe_allow_html=True
                )

    # TAB 4 : EXPORTER
    with tab4:
        st.subheader("💾 Exporter les résultats")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Texte nettoyé")
            if 'cleaned_text' in locals():
                st.download_button(
                    label="📥 Télécharger le texte nettoyé",
                    data=cleaned_text,
                    file_name="texte_nettoye.txt",
                    mime="text/plain",
                    key="download_cleaned"
                )
        
        with col2:
            st.markdown("### Statistiques")
            if 'word_counts' in locals() and 'nb_words' in locals():
                # Créer un rapport
                report = f"""RAPPORT D'ANALYSE DE TEXTE
=====================================

STATISTIQUES GÉNÉRALES:
- Nombre de caractères: {nb_chars}
- Nombre de mots: {nb_words}
- Nombre de phrases: {nb_sentences}

ANALYSE DE SENTIMENT:
- Sentiment global: {sentiment} {emoji_display}
- Emojis positifs: {emoji_positive}
- Emojis négatifs: {emoji_negative}
- Emojis neutres: {emoji_neutral}
- Mots positifs: {word_positive}
- Mots négatifs: {word_negative}
- Score total positif: {total_positive}
- Score total négatif: {total_negative}

MOTS LES PLUS FRÉQUENTS:
"""
                for word, count in top_words:
                    report += f"- {word}: {count}\n"
                
                st.download_button(
                    label="📥 Télécharger le rapport",
                    data=report,
                    file_name="rapport_analyse.txt",
                    mime="text/plain",
                    key="download_report"
                )
        
        
