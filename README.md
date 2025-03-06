# toDys

**toDys** est une application web légère conçue pour aider les enseignants à transformer des documents pédagogiques en versions adaptées aux enfants dyslexiques. L'application permet de télécharger un fichier, de le transformer, puis de le télécharger à nouveau dans un format plus accessible.

## Table des Matières

- [toDys](#todys)
  - [Table des Matières](#table-des-matières)
  - [Fonctionnalités](#fonctionnalités)
  - [Stack Technique](#stack-technique)
  - [Installation](#installation)
  - [Contribuer](#contribuer)
  - [Licence](#licence)

## Fonctionnalités

- **Téléchargement de Fichiers** : Téléchargez des fichiers PDF, Word, etc.
- **Transformation de Documents** : Transformez les documents en un format adapté aux dyslexiques.
- **Interface Utilisateur Intuitive** : Une interface simple et intuitive pour une utilisation facile.
- **Rapidité et Efficacité** : Transformation rapide des documents sans stockage durable des fichiers.

## Stack Technique

- **Frontend** :
  - **HTMX** : Pour l'interactivité sans rechargement de page.
  - **Alpine.js** : Pour une réactivité légère et simple.
  - **Tailwind CSS** : Pour un style flexible et rapide.

- **Backend** :
  - **FastAPI** : Pour créer une API rapide et performante avec Python.

- **Pipeline IA** :
  - **LLM** : Utilisation d'un LLM pour la transformation de texte.

- **Stockage** :
  - **Supabase** : Pour un stockage temporaire des fichiers.

- **Déploiement** :
  - **Vercel** : Pour un déploiement facile et une intégration continue.

## Installation

Pour installer et exécuter toDys localement, suivez ces étapes :

1. **Cloner le Dépôt** :
   ```bash
   git clone https://github.com/BenjaminSiret/toDys.git
   cd toDys

. **Installer les Dépendances** :
   - **Frontend** :
     ```bash
     npm install
     ```
   - **Backend** :
     ```bash
     pip install -r requirements.txt
     ```

3. **Configurer l'environnement**:
   - Créer un fichier .env pour configurer les variables d'environnement nécessaires.

## Contribuer

Pour l'instant les contributions ne sont pas ouvertes, cela viendra dans un futur proche.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.




