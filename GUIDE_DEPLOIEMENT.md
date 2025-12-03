# Guide de Déploiement Django en Production

Ce guide détaille les étapes pour déployer une application Django sur un serveur Linux (Ubuntu 20.04/22.04).

## 1. Préparation du Serveur

Connectez-vous à votre serveur via SSH et mettez à jour les paquets :

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip python3-venv nginx curl
```

## 2. Configuration du Projet

### Cloner le projet
```bash
cd /home/ubuntu
git clone <votre-repo-url> app_django_dep
cd app_django_dep
```

### Créer l'environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Collecter les fichiers statiques
Assurez-vous que `STATIC_ROOT` est configuré dans `settings.py`.
```bash
python manage.py collectstatic
```

### Migrer la base de données
```bash
python manage.py migrate
```

## 3. Configuration de Gunicorn

Gunicorn servira l'application Python. Nous allons utiliser `systemd` pour le gérer comme un service.

1. Editez le fichier de service fourni dans `deployment/gunicorn.service` pour correspondre à vos chemins (remplacez `/home/ubuntu/app_django_dep` par votre chemin réel).
2. Copiez le fichier vers systemd :
```bash
sudo cp deployment/gunicorn.service /etc/systemd/system/
```
3. Démarrez et activez le service :
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
4. Vérifiez le statut :
```bash
sudo systemctl status gunicorn
```

## 4. Configuration de Nginx

Nginx agira comme reverse proxy et servira les fichiers statiques.

1. Editez le fichier `deployment/nginx_site.conf` :
   - Remplacez `your_domain_or_ip` par votre domaine ou IP.
   - Vérifiez les chemins vers `/static/`.
2. Copiez la configuration :
```bash
sudo cp deployment/nginx_site.conf /etc/nginx/sites-available/app_django_dep
```
3. Activez le site :
```bash
sudo ln -s /etc/nginx/sites-available/app_django_dep /etc/nginx/sites-enabled
```
4. Testez la configuration et redémarrez Nginx :
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 5. Sécurisation (HTTPS)

Utilisez Certbot pour obtenir un certificat SSL gratuit Let's Encrypt.

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votredomaine.com
```

## 6. Variables d'Environnement

Pour la production, ne laissez jamais `DEBUG=True` et ne stockez pas les clés secrètes dans le code.
Utilisez des variables d'environnement ou un fichier `.env` (avec `python-dotenv`).

Dans `settings.py` :
```python
import os
DEBUG = os.environ.get('DEBUG') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
```

## 7. Firewall (UFW)

N'oubliez pas d'autoriser le trafic HTTP/HTTPS :
```bash
sudo ufw allow 'Nginx Full'
```
