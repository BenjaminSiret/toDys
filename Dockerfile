# Utiliser une image de base Python
FROM python:3.11-slim

# Installer les dépendances système nécessaires pour python-magic
RUN apt-get update && apt-get install -y libmagic1 && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application écoute
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "-m", "app.main"]
