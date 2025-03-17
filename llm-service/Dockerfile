# Utiliser une image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du service LLM
COPY . /app

# Installer les dépendances spécifiques au service LLM
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel le service LLM écoute
EXPOSE 5001

# Commande pour lancer le service LLM
CMD ["python", "main.py"]
