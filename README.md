# 🔐 Log Analyzer – Détection de logs suspects avec Machine Learning

> Application Django qui permet de **téléverser, analyser et visualiser des logs de sécurité** via un modèle SVM entraîné à l'avance avec scikit-learn.  

Ce projet combine **machine learning**, **analyse de texte**, **interface web intuitive**, et **visualisation de données** pour surveiller des logs systèmes.

---

## 🧠 Fonctionnalités

- 📂 Téléversement de fichiers CSV contenant des logs (logs Apache, systèmes, etc.)
- 🤖 Analyse automatique des logs via un **modèle SVM (pipeline TF-IDF + SVC)** pré-entraîné
- 📊 Tableau interactif des logs avec filtrage (Django Tables 2)
- 📈 Dashboard avec statistiques globales et graphiques
- 🔎 Détection automatique des logs malveillants (ex: `authentication-failed`, `connection-failed`, etc.)
- 💾 Stockage structuré des logs analysés dans la base de données
- ⚠️ Marquage des logs considérés comme "suspects" via un ensemble de catégories définies

---

## 🏗️ Architecture du projet
log_analyzer/
│
├── models/ # Modèle SVM sauvegardé (.pkl)
├── templates/log_analyzer/ # Templates HTML
├── static/ # CSS, JS, Chart.js
├── views.py # Logique backend (upload, analyse, dashboard)
├── utils.py # Fonctions de parsing, prétraitement, chargement modèle
├── tables.py # Définition du tableau de logs
├── models.py # Modèle AuthLog
└── ...

---

## 🚀 Lancer le projet en local

### 1. Prérequis

- Python 3.10+
- Django 5.x
- Pipenv ou venv recommandé

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

## Contributeur

Omar DIOP
Ndeye Mareme Gueye
