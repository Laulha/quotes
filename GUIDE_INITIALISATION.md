# Guide d'Initialisation du Projet Django

Ce guide vous accompagne pour configurer et lancer le projet Django en développement local.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- **Python 3.8+** ([Télécharger Python](https://www.python.org/downloads/))
- **Git** ([Télécharger Git](https://git-scm.com/downloads))
- Un éditeur de code (VS Code, PyCharm, etc.)

Pour vérifier les installations :
```bash
python --version
git --version
```

## 🚀 Installation et Configuration

### 1. Cloner le Projet

Si vous n'avez pas encore le projet, clonez-le :
```bash
git clone <url-du-repo>
cd app_django_dep
```

Si vous avez déjà le projet, naviguez simplement dans le dossier :
```bash
cd d:\Pdosiq\projet_deploiement\app_django_dep
```

### 2. Créer l'Environnement Virtuel

L'environnement virtuel isole les dépendances du projet.

**Sur Windows :**
```bash
python -m venv venv
```

**Sur Linux/Mac :**
```bash
python3 -m venv venv
```

### 3. Activer l'Environnement Virtuel

**Sur Windows (Git Bash ou PowerShell) :**
```bash
source venv/Scripts/activate
```

**Sur Windows (CMD) :**
```cmd
venv\Scripts\activate.bat
```

**Sur Linux/Mac :**
```bash
source venv/bin/activate
```

Vous devriez voir `(venv)` apparaître au début de votre ligne de commande.

### 4. Installer les Dépendances

```bash
pip install -r requirements.txt
```

Cette commande installe Django et toutes les bibliothèques nécessaires.

### 5. Configurer la Base de Données

Appliquer les migrations pour créer les tables de la base de données :
```bash
python manage.py migrate
```

### 6. Charger les Données d'Exemple (Optionnel)

Pour avoir des citations d'exemple dans l'application :
```bash
python manage.py load_sample_quotes
```

### 7. Créer un Super Utilisateur (Optionnel)

Pour accéder à l'interface d'administration Django :
```bash
python manage.py createsuperuser
```

Suivez les instructions pour définir :
- Nom d'utilisateur
- Adresse email (optionnel)
- Mot de passe

## ▶️ Lancer le Serveur de Développement

Une fois tout configuré, lancez le serveur :

```bash
python manage.py runserver
```

Le serveur démarre par défaut sur **http://127.0.0.1:8000/**

### Accéder à l'Application

- **Page d'accueil** : http://127.0.0.1:8000/
- **Interface d'administration** : http://127.0.0.1:8000/admin/
  - Connectez-vous avec le super utilisateur créé à l'étape 7

## 🛠️ Commandes Utiles

### Arrêter le Serveur
Appuyez sur `Ctrl + C` dans le terminal où le serveur tourne.

### Désactiver l'Environnement Virtuel
```bash
deactivate
```

### Créer une Nouvelle Application Django
```bash
python manage.py startapp nom_app
```

### Créer de Nouvelles Migrations
Après avoir modifié les modèles dans `models.py` :
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecter les Fichiers Statiques
Pour la production ou pour tester :
```bash
python manage.py collectstatic
```

### Lancer les Tests
```bash
python manage.py test
```

### Ouvrir le Shell Django
Pour interagir avec la base de données via Python :
```bash
python manage.py shell
```

## 📁 Structure du Projet

```
app_django_dep/
├── config/              # Configuration principale du projet
│   ├── settings.py      # Paramètres Django
│   ├── urls.py          # Routes principales
│   └── wsgi.py          # Point d'entrée WSGI
├── quotes/              # Application de citations
│   ├── models.py        # Modèles de données
│   ├── views.py         # Vues/Contrôleurs
│   ├── urls.py          # Routes de l'app
│   ├── forms.py         # Formulaires
│   ├── templates/       # Templates HTML
│   └── static/          # Fichiers statiques (CSS, JS, images)
├── deployment/          # Fichiers de déploiement
├── venv/                # Environnement virtuel (ignoré par git)
├── db.sqlite3           # Base de données SQLite
├── manage.py            # Script de gestion Django
└── requirements.txt     # Dépendances Python
```

## 🔧 Configuration Avancée

### Variables d'Environnement

Pour un environnement de développement plus sécurisé, vous pouvez utiliser un fichier `.env` :

1. Installer `python-dotenv` :
```bash
pip install python-dotenv
```

2. Créer un fichier `.env` à la racine :
```env
DEBUG=True
SECRET_KEY=votre-clé-secrète-ici
DATABASE_URL=sqlite:///db.sqlite3
```

3. Modifier `config/settings.py` pour charger ces variables.

### Changer le Port du Serveur

Par défaut, le serveur tourne sur le port 8000. Pour utiliser un autre port :
```bash
python manage.py runserver 8080
```

Ou pour rendre accessible depuis d'autres machines sur le réseau :
```bash
python manage.py runserver 0.0.0.0:8000
```

## ❓ Dépannage

### Erreur : "No module named django"
- Vérifiez que l'environnement virtuel est activé (`(venv)` visible)
- Réinstallez les dépendances : `pip install -r requirements.txt`

### Erreur : "Port already in use"
- Un autre processus utilise le port 8000
- Arrêtez l'autre serveur ou utilisez un autre port : `python manage.py runserver 8080`

### Erreur de Migration
- Supprimez `db.sqlite3` et le dossier `quotes/migrations/` (sauf `__init__.py`)
- Recréez les migrations :
```bash
python manage.py makemigrations quotes
python manage.py migrate
```

### Les Fichiers Statiques ne se Chargent pas
- Vérifiez que `DEBUG=True` dans `settings.py` pour le développement
- Ou exécutez : `python manage.py collectstatic`

## 📚 Ressources Supplémentaires

- [Documentation Django](https://docs.djangoproject.com/)
- [Guide de Déploiement](./GUIDE_DEPLOIEMENT.md) - Pour mettre en production
- [Django Girls Tutorial](https://tutorial.djangogirls.org/fr/)

## 🎯 Prochaines Étapes

Maintenant que votre environnement est configuré :

1. **Explorez l'application** : Naviguez sur http://127.0.0.1:8000/
2. **Consultez le code** : Examinez `quotes/views.py` et `quotes/models.py`
3. **Modifiez les templates** : Personnalisez `quotes/templates/`
4. **Ajoutez des fonctionnalités** : Créez de nouvelles vues et modèles
5. **Consultez le guide de déploiement** : Quand vous êtes prêt pour la production

---

**Bon développement ! 🚀**
