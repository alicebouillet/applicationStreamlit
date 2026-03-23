import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def app():
    # Titre principal
    st.markdown(
        """
        <h1 style="text-align:center;">Analyse d'un fichier CSV</h1>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Instructions pour l'utilisateur
    st.markdown(
        """
        ### 📂 Importez votre fichier CSV

        Utilisez le sélecteur de fichiers ci-dessous pour importer un fichier CSV.  
        L'application analysera automatiquement les données et affichera des statistiques descriptives ainsi que des visualisations interactives.     
        Si aucun fichier n'est importé, un jeu de données par défaut sera utilisé.
        """
    )
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

    # si pas de fichier se servir de docs/fruits_legumes.csv
    if uploaded_file is not None:
        # Lire le fichier CSV
        df = pd.read_csv(uploaded_file)
    else :
        df = pd.read_csv("projet/docs/fruits_legumes.csv", sep =";", decimal=",")

    # Afficher les données dans des onglets
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Apercu des données", "Validation des données", "Statistiques descriptives", "Visualisations", "Filtres interactifs"])
        
    with tab1:
        st.subheader("Aperçu des données")
        st.dataframe(df)
        # afficher les catégories de chaque colonne
        st.markdown("**Types de données par colonne :**")
        dtypes = pd.DataFrame(df.dtypes, columns=["Type de données"])
        st.dataframe(dtypes)
    
    with tab2:
        st.subheader("Vérification de la qualité des données")
        st.markdown("**Informations sur les données :**")

        #valeurs manquantes
        st.markdown("**Valeurs manquantes par colonne :**")
        missing_values = df.isnull().sum()
        st.dataframe(missing_values)

        #choix de gérer les valeurs manquantes
        st.markdown("**Gérer les valeurs manquantes :**")
        missing_option = st.selectbox("Choisissez une option", ["Aucune", "Supprimer les lignes avec valeurs manquantes", "Remplir avec la moyenne (numérique) ou 'Inconnu' (catégorique)"])
        if missing_option == "Supprimer les lignes avec valeurs manquantes":
            df = df.dropna()
            st.write("Lignes avec valeurs manquantes supprimées.")
        elif missing_option == "Remplir avec la moyenne (numérique) ou 'Inconnu' (catégorique)":
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    df[col].fillna('Inconnu', inplace=True)
            st.write("Valeurs manquantes remplies.")
        st.divider()

        #doublons
        st.markdown("**Nombre de doublons :**")
        num_duplicates = df.duplicated().sum()
        st.write(num_duplicates)

        #choix de gérer les doublons
        st.markdown("**Gérer les doublons :**")
        duplicate_option = st.selectbox("Choisissez une option pour les doublons", ["Aucune", "Supprimer les doublons"])
        if duplicate_option == "Supprimer les doublons":
            df = df.drop_duplicates()
            st.write("Doublons supprimés.")

        st.divider()

        # exporter les données nettoyées
        st.markdown("**Exporter les données nettoyées :**")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données nettoyées au format CSV",
            data=csv,
            file_name='donnees_nettoyees.csv',
            mime='text/csv'
        )

    with tab3:
        st.subheader("Statistiques descriptives")
        st.write(df.describe())
        
    # Analyser les données et afficher les résultats dans l'onglet "Analyse"
    with tab4:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        #Histogrammes des variables numériques
        if len(numeric_cols) > 0:
            st.markdown("### 📊 Distribution des variables numériques")
            
            # Sélection des colonnes à afficher
            selected_numeric = st.multiselect(
                "Sélectionnez les variables numériques à visualiser",
                numeric_cols,
                default=numeric_cols[:min(4, len(numeric_cols))]
            )

            if selected_numeric:
                # Créer une grille de graphiques
                num_graphs = len(selected_numeric)
                cols_per_row = 2
                rows = (num_graphs + cols_per_row - 1) // cols_per_row
                
                for i in range(rows):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        idx = i * cols_per_row + j
                        if idx < num_graphs:
                            with cols[j]:
                                col = selected_numeric[idx]
                                fig, ax = plt.subplots(figsize=(6, 4))
                                sns.histplot(df[col], kde=True, ax=ax, color='steelblue')
                                ax.set_title(f'Distribution de {col}', fontsize=12, fontweight='bold')
                                ax.set_xlabel(col, fontsize=10)
                                ax.set_ylabel('Fréquence', fontsize=10)
                                st.pyplot(fig)
                                plt.close()

        st.divider()

        # Ligne 3 : Boxplots et variables catégorielles
        col_left, col_right = st.columns(2)

        with col_left:
            if len(numeric_cols) > 0:
                st.markdown("### 📦 Boxplot")
                selected_box = st.selectbox("Variable numérique", numeric_cols, key="boxplot")
                
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.boxplot(data=df, y=selected_box, ax=ax, color='lightcoral')
                ax.set_title(f'Boxplot de {selected_box}', fontsize=12, fontweight='bold')
                st.pyplot(fig)
                plt.close()

        with col_right:
            if len(categorical_cols) > 0:
                st.markdown("### 📊 Répartition catégorique")
                selected_cat = st.selectbox("Variable catégorique", categorical_cols, key="barplot")
                
                fig, ax = plt.subplots(figsize=(6, 4))
                df[selected_cat].value_counts().head(10).plot(kind='bar', ax=ax, color='mediumseagreen')
                ax.set_title(f'Top 10 - {selected_cat}', fontsize=12, fontweight='bold')
                ax.set_xlabel(selected_cat, fontsize=10)
                ax.set_ylabel('Comptage', fontsize=10)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                st.pyplot(fig)
                plt.close()

        st.divider()

        # Ligne 4 : Corrélation et Scatter plot
        if len(numeric_cols) >= 2:
            st.markdown("### 🔗 Analyses croisées")
            
            col_corr, col_scatter = st.columns(2)
            
            with col_corr:
                st.markdown("#### Matrice de corrélation")
                selected_corr = st.multiselect(
                    "Variables pour la corrélation",
                    numeric_cols,
                    default=numeric_cols[:min(5, len(numeric_cols))],
                    key="corr"
                )
                
                if len(selected_corr) >= 2:
                    fig, ax = plt.subplots(figsize=(6, 5))
                    correlation = df[selected_corr].corr()
                    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax, fmt='.2f', linewidths=0.5, cbar_kws={'shrink': 0.8})
                    ax.set_title('Corrélation', fontsize=12, fontweight='bold')
                    st.pyplot(fig)
                    plt.close()

            with col_scatter:
                st.markdown("#### Nuage de points")
                x_var = st.selectbox("Variable X", numeric_cols, key="scatter_x")
                y_var = st.selectbox("Variable Y", numeric_cols, key="scatter_y")
                
                fig, ax = plt.subplots(figsize=(6, 5))
                sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax, color='darkviolet', alpha=0.6)
                ax.set_title(f'{y_var} vs {x_var}', fontsize=12, fontweight='bold')
                ax.set_xlabel(x_var, fontsize=10)
                ax.set_ylabel(y_var, fontsize=10)
                st.pyplot(fig)
                plt.close()

    with tab5:
        st.subheader("🔍 Filtres interactifs")
        st.markdown("Filtrez les données selon vos critères.")
        
        # Filtres pour variables numériques
        if len(numeric_cols) > 0:
            st.markdown("#### Filtres numériques")
            for col in numeric_cols:
                min_val = float(df[col].min())
                max_val = float(df[col].max())
                selected_range = st.slider(
                    f"Plage pour {col}",
                    min_val,
                    max_val,
                    (min_val, max_val)
                )
                df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]
        
        # Filtres pour variables catégorielles
        if len(categorical_cols) > 0:
            st.markdown("#### Filtres catégoriels")
            for col in categorical_cols:
                unique_values = df[col].unique().tolist()
                selected_values = st.multiselect(
                    f"Sélectionner {col}",
                    unique_values,
                    default=unique_values
                )
                df = df[df[col].isin(selected_values)]
        
        st.markdown("#### Données filtrées")
        st.dataframe(df)
        st.markdown(f"**{len(df)} lignes** après filtrage")
        # exporter les données filtrées
        st.markdown("**Exporter les données filtrées :**")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données filtrées au format CSV",
            data=csv,
            file_name='donnees_filtrees.csv',
            mime='text/csv'
        )
