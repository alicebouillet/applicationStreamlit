# 📊 Projet Streamlit – Science de la Donnée

Application web interactive développée avec Streamlit pour l'analyse de données multi-formats (CSV, images, texte).

## 🎯 Objectif du Projet

Projet académique réalisé dans le cadre du cours d'INGÉ 2 à l'Université de Poitiers. L'application permet d'analyser différents types de données via une interface web intuitive.

## ✨ Fonctionnalités

- 📚 **Présentation du projet** : Introduction et contexte
- 📊 **Analyse CSV** : Visualisation et statistiques de fichiers CSV
- 🔎 **Analyse d'image** : Traitement et analyse d'images
- 📝 **Analyse de texte** : Traitement et analyse textuelle

## 🛠️ Technologies Utilisées

- **Streamlit** : Framework web
- **Pandas** : Manipulation de données
- **Matplotlib/Seaborn** : Visualisation
- **OpenCV/Pillow** : Traitement d'images
- **NumPy** : Calculs numériques

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone <URL_DU_REPO>
cd prog_objet/projet
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## ▶️ Lancement de l'Application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 📁 Structure du Projet

```
projet/
├── app.py                 # Point d'entrée de l'application
├── requirements.txt       # Dépendances Python
├── pagesWeb/             # Modules des différentes pages
│   ├── presentation.py
│   ├── csv.py
│   ├── image.py
│   └── texte.py
└── README.md
```

## 👥 Auteur

Projet réalisé par Alice – INGÉ 2, Université de Poitiers

## 📅 Date

Année académique 2025-2026