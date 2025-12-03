# Guide de Préparation PostgreSQL pour Django

Ce guide vous accompagne pour installer, configurer et utiliser PostgreSQL avec votre projet Django, en développement local et en production.

## 📋 Table des Matières

1. [Installation de PostgreSQL](#installation-de-postgresql)
2. [Configuration de la Base de Données](#configuration-de-la-base-de-données)
3. [Configuration Django](#configuration-django)
4. [Migration depuis SQLite](#migration-depuis-sqlite)
5. [Commandes Utiles PostgreSQL](#commandes-utiles-postgresql)
6. [Dépannage](#dépannage)

---

## 🔧 Installation de PostgreSQL

### Sur Windows

#### Option 1 : Installateur Officiel (Recommandé)

1. **Télécharger PostgreSQL** :
   - Visitez [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
   - Téléchargez la dernière version (PostgreSQL 15 ou 16)

2. **Installer PostgreSQL** :
   - Lancez l'installateur
   - Choisissez les composants :
     - ✅ PostgreSQL Server
     - ✅ pgAdmin 4 (interface graphique)
     - ✅ Command Line Tools
   - Définissez un **mot de passe** pour l'utilisateur `postgres` (notez-le !)
   - Port par défaut : `5432`
   - Locale : `French, France` ou `Default locale`

3. **Vérifier l'installation** :
```bash
psql --version
```

#### Option 2 : Via Chocolatey

Si vous avez Chocolatey installé :
```bash
choco install postgresql
```

### Sur Linux (Ubuntu/Debian)

```bash
# Mettre à jour les paquets
sudo apt update

# Installer PostgreSQL
sudo apt install postgresql postgresql-contrib

# Démarrer le service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Vérifier le statut
sudo systemctl status postgresql
```

### Sur macOS

#### Via Homebrew :
```bash
# Installer PostgreSQL
brew install postgresql@15

# Démarrer le service
brew services start postgresql@15
```

#### Via Postgres.app :
- Téléchargez [Postgres.app](https://postgresapp.com/)
- Glissez dans Applications et lancez

---

## 🗄️ Configuration de la Base de Données

### 1. Accéder à PostgreSQL

**Sur Windows :**
```bash
# Via psql (invite de commande PostgreSQL)
psql -U postgres
```

**Sur Linux :**
```bash
# Se connecter en tant qu'utilisateur postgres
sudo -u postgres psql
```

**Sur macOS :**
```bash
psql postgres
```

### 2. Créer la Base de Données et l'Utilisateur

Une fois dans le shell PostgreSQL (`postgres=#`), exécutez :

```sql
-- Créer un utilisateur pour Django
CREATE USER django_user WITH PASSWORD 'votre_mot_de_passe_securise';

-- Créer la base de données
CREATE DATABASE django_db OWNER django_user;

-- Accorder tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;

-- Pour PostgreSQL 15+, accorder les privilèges sur le schéma
\c django_db
GRANT ALL ON SCHEMA public TO django_user;
GRANT CREATE ON SCHEMA public TO django_user;

-- Quitter psql
\q
```

### 3. Vérifier la Création

```bash
# Lister les bases de données
psql -U postgres -c "\l"

# Se connecter à la base créée
psql -U django_user -d django_db
```

---

## ⚙️ Configuration Django

### 1. Installer le Driver PostgreSQL

Activez votre environnement virtuel et installez `psycopg2` :

**Sur Windows :**
```bash
source venv/Scripts/activate
pip install psycopg2-binary
```

**Sur Linux/macOS :**
```bash
source venv/bin/activate
pip install psycopg2-binary
```

### 2. Mettre à Jour `requirements.txt`

Ajoutez la dépendance :
```bash
pip freeze | grep psycopg2 >> requirements.txt
```

Ou ajoutez manuellement dans `requirements.txt` :
```
psycopg2-binary>=2.9.9
```

### 3. Configurer `settings.py`

#### Option A : Configuration Directe (Développement)

Modifiez `config/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'votre_mot_de_passe_securise',
        'HOST': 'localhost',  # ou '127.0.0.1'
        'PORT': '5432',
    }
}
```

#### Option B : Variables d'Environnement (Production - Recommandé)

1. **Installer `python-dotenv`** :
```bash
pip install python-dotenv
```

2. **Créer un fichier `.env`** à la racine du projet :
```env
# Base de données
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=votre_mot_de_passe_securise
DB_HOST=localhost
DB_PORT=5432

# Django
DEBUG=True
SECRET_KEY=django-insecure--d4(xlw5y!$@34ujxpz^4c-24+tl^g1kt%zlu=0q24qkw!m_l6
```

3. **Ajouter `.env` au `.gitignore`** :
```bash
echo ".env" >> .gitignore
```

4. **Modifier `config/settings.py`** :
```python
from pathlib import Path
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Base de données
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}
```

### 4. Appliquer les Migrations

```bash
# Créer les tables dans PostgreSQL
python manage.py migrate

# Créer un super utilisateur
python manage.py createsuperuser

# Charger les données d'exemple (si disponible)
python manage.py load_sample_quotes
```

---

## 🔄 Migration depuis SQLite

Si vous avez déjà des données dans SQLite et souhaitez migrer vers PostgreSQL :

### Méthode 1 : Avec `dumpdata` et `loaddata`

```bash
# 1. Sauvegarder les données SQLite
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude=contenttypes --exclude=auth.Permission \
  --indent=2 > datadump.json

# 2. Modifier settings.py pour utiliser PostgreSQL

# 3. Créer les tables PostgreSQL
python manage.py migrate

# 4. Charger les données
python manage.py loaddata datadump.json
```

### Méthode 2 : Avec `django-extensions` (Plus Robuste)

```bash
# 1. Installer django-extensions
pip install django-extensions

# 2. Ajouter à INSTALLED_APPS dans settings.py
# 'django_extensions',

# 3. Exporter depuis SQLite
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude=contenttypes --exclude=auth.Permission > data.json

# 4. Configurer PostgreSQL dans settings.py

# 5. Importer dans PostgreSQL
python manage.py migrate
python manage.py loaddata data.json
```

---

## 🛠️ Commandes Utiles PostgreSQL

### Commandes psql (Shell PostgreSQL)

```bash
# Se connecter à une base de données
psql -U django_user -d django_db

# Commandes dans psql :
\l                    # Lister toutes les bases de données
\c django_db          # Se connecter à une base
\dt                   # Lister les tables
\d nom_table          # Décrire une table
\du                   # Lister les utilisateurs
\q                    # Quitter
```

### Commandes SQL Utiles

```sql
-- Voir toutes les tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Compter les enregistrements d'une table
SELECT COUNT(*) FROM quotes_quote;

-- Voir les 5 dernières citations
SELECT * FROM quotes_quote ORDER BY id DESC LIMIT 5;

-- Supprimer toutes les données d'une table
TRUNCATE TABLE quotes_quote CASCADE;

-- Supprimer une base de données (depuis postgres)
DROP DATABASE django_db;
```

### Sauvegardes et Restaurations

```bash
# Créer une sauvegarde
pg_dump -U django_user -d django_db -F c -f backup.dump

# Restaurer une sauvegarde
pg_restore -U django_user -d django_db -c backup.dump

# Export en SQL
pg_dump -U django_user django_db > backup.sql

# Import SQL
psql -U django_user django_db < backup.sql
```

---

## 🔐 Sécurité et Bonnes Pratiques

### 1. Mot de Passe Sécurisé

Utilisez un mot de passe fort pour l'utilisateur PostgreSQL :
```bash
# Générer un mot de passe aléatoire (Linux/Mac)
openssl rand -base64 32
```

### 2. Configuration Production

Pour la production, dans `.env` :
```env
DEBUG=False
ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com
DB_HOST=localhost  # ou IP du serveur PostgreSQL
```

### 3. Connexions Limitées

Modifiez `/etc/postgresql/15/main/postgresql.conf` (Linux) :
```conf
max_connections = 100
shared_buffers = 256MB
```

### 4. Authentification

Configurez `/etc/postgresql/15/main/pg_hba.conf` (Linux) :
```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

---

## ❓ Dépannage

### Erreur : "psycopg2 not found"

**Solution :**
```bash
pip install psycopg2-binary
```

### Erreur : "FATAL: password authentication failed"

**Solutions :**
1. Vérifiez le mot de passe dans `.env` ou `settings.py`
2. Réinitialisez le mot de passe :
```sql
ALTER USER django_user WITH PASSWORD 'nouveau_mot_de_passe';
```

### Erreur : "could not connect to server"

**Solutions :**
1. Vérifiez que PostgreSQL est démarré :
```bash
# Windows
net start postgresql-x64-15

# Linux
sudo systemctl status postgresql
sudo systemctl start postgresql
```

2. Vérifiez le port (5432 par défaut) :
```bash
netstat -an | grep 5432
```

### Erreur : "database does not exist"

**Solution :**
```sql
-- Créer la base de données
CREATE DATABASE django_db OWNER django_user;
```

### Erreur : "permission denied for schema public"

**Solution (PostgreSQL 15+) :**
```sql
\c django_db
GRANT ALL ON SCHEMA public TO django_user;
GRANT CREATE ON SCHEMA public TO django_user;
```

### Performances Lentes

**Solutions :**
1. Créer des index sur les champs fréquemment recherchés
2. Analyser les requêtes avec `EXPLAIN ANALYZE`
3. Augmenter `shared_buffers` dans `postgresql.conf`

---

## 📊 Outils Graphiques

### pgAdmin 4 (Inclus avec PostgreSQL)

- Interface web complète pour gérer PostgreSQL
- Accès : http://localhost:5050 (ou via l'application)
- Permet de visualiser, éditer et gérer les bases de données

### DBeaver (Gratuit et Multi-plateforme)

- Téléchargement : [https://dbeaver.io/](https://dbeaver.io/)
- Support de multiples bases de données
- Interface intuitive

### DataGrip (JetBrains - Payant)

- IDE professionnel pour bases de données
- Excellent pour les développeurs

---

## 🚀 Configuration pour Production (Serveur Linux)

### Installation sur Ubuntu Server

```bash
# Installer PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Créer la base et l'utilisateur
sudo -u postgres psql << EOF
CREATE USER django_user WITH PASSWORD 'mot_de_passe_securise';
CREATE DATABASE django_db OWNER django_user;
GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;
\c django_db
GRANT ALL ON SCHEMA public TO django_user;
EOF

# Configurer l'accès distant (si nécessaire)
sudo nano /etc/postgresql/15/main/postgresql.conf
# Modifier : listen_addresses = '*'

sudo nano /etc/postgresql/15/main/pg_hba.conf
# Ajouter : host all all 0.0.0.0/0 md5

# Redémarrer PostgreSQL
sudo systemctl restart postgresql

# Autoriser le port dans le firewall
sudo ufw allow 5432/tcp
```

### Variables d'Environnement Production

Sur le serveur, créez `/home/ubuntu/app_django_dep/.env` :
```env
DEBUG=False
SECRET_KEY=generer-une-nouvelle-cle-secrete-unique
ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=mot_de_passe_tres_securise
DB_HOST=localhost
DB_PORT=5432
```

---

## 📚 Ressources Supplémentaires

- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Django + PostgreSQL](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

---

## ✅ Checklist de Configuration

- [ ] PostgreSQL installé et démarré
- [ ] Base de données `django_db` créée
- [ ] Utilisateur `django_user` créé avec mot de passe
- [ ] Privilèges accordés
- [ ] `psycopg2-binary` installé dans l'environnement virtuel
- [ ] `settings.py` configuré avec les bonnes informations
- [ ] `.env` créé et ajouté au `.gitignore`
- [ ] Migrations appliquées : `python manage.py migrate`
- [ ] Super utilisateur créé : `python manage.py createsuperuser`
- [ ] Application testée : `python manage.py runserver`

---

**Votre base de données PostgreSQL est maintenant prête ! 🎉**
