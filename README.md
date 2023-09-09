# STEGANO WEB APP

**Description :**  
Stegano Web App est une plateforme web moderne permettant aux utilisateurs de signer numériquement des images en utilisant l'art de la stéganographie. L'application utilise FastAPI pour le backend, React pour le frontend, et GraphQL pour la gestion des requêtes API. Elle comprend également des fonctionnalités avancées d'authentification et de sécurité.

---

## Table des Matières

1. [Titre et Description](#stegano-web-app)
2. [Configuration Initiale](#configuration-initiale)
    - [Prérequis](#prérequis)
    - [Installation des Dépendances](#installation-des-dépendances)
3. [Mise en Place de l'Application](#mise-en-place-de-lapplication)
    - [Clonage du Dépôt](#clonage-du-dépôt)
    - [Configuration de l'Environnement Virtuel](#configuration-de-lenvironnement-virtuel)
    - [Installation des Dépendances](#installation-des-dépendances)
4. [Stack Technique de l'API](#stack-techniques)
    - [FastAPI](#fastapi)
    - [SQLAlchemy](#sqlalchemy)
    - [GraphQL](#graphql)
    - [Strawberry](#strawberry)
    - [Autres outils et bibliothèques](#autres-outils)

--- 

## Configuration Initiale

### Prérequis

- **Python** : L'application nécessite Python 3.8 ou une version ultérieure.
- **Autres dépendances** : Toutes les dépendances nécessaires sont répertoriées dans le fichier `requirements.txt` du projet.

---

## Mise en Place de l'Application

### Clonage du Dépôt

Pour commencer, clonez le dépôt sur votre machine locale :

```bash
git clone [URL_DU_DEPOT_GIT]
```

### Configuration de l'Environnement Virtuel

Il est recommandé d'utiliser un environnement virtuel pour éviter les conflits de dépendances. Pour configurer et activer un environnement virtuel :

```bash
python -m venv env
source env/bin/activate  # Sur Linux/macOS
env\Scripts\activate     # Sur Windows
```

### Installation des Dépendances

Avec votre environnement virtuel activé, installez les dépendances :

```bash
pip install -r requirements.txt
```
---

## Stack Technique de l'API

### FastAPI

FastAPI est un framework web moderne, rapide (hautes performances) et basé sur des normes, pour construire des API avec Python 3.6+ basées sur des types d'indices standard.

- **Performances** : FastAPI est l'un des frameworks les plus rapides pour Python, seulement devancé par NodeJS et Go.
- **Validation automatique** : Grâce aux annotations de type Python, FastAPI génère automatiquement des validations pour les données entrantes.
- **Documentation interactive** : FastAPI génère une documentation interactive pour les API grâce à Swagger UI et ReDoc, permettant de tester les endpoints directement depuis le navigateur.
- **Dépendances** : FastAPI intègre un système de dépendances basé sur les fonctions Python qui permet une réutilisation et une séparation claire des préoccupations.

### SQLAlchemy

SQLAlchemy est une bibliothèque SQL et un ORM (Object-Relational Mapping) pour Python. Elle fournit des outils pour travailler efficacement avec des bases de données, permettant une abstraction du code SQL.

- **Flexibilité** : SQLAlchemy permet une utilisation de haut niveau avec un ORM mais donne également la possibilité de plonger dans des requêtes SQL brutes.
- **Support de multiples bases de données** : SQLAlchemy supporte une variété de bases de données relationnelles comme PostgreSQL, MySQL, SQLite, etc.
  
### GraphQL

GraphQL est une langue de requête pour votre API, et un environnement d'exécution côté serveur pour exécuter ces requêtes en utilisant un type de système que vous définissez pour vos données.

- **Requêtes sur mesure** : Contrairement à une API REST où l'endpoint détermine la structure des données renvoyées, avec GraphQL, le client spécifie exactement les données qu'il souhaite.
- **Évolutivité** : GraphQL permet d'ajouter de nouveaux champs et types à votre API sans impacter les requêtes existantes, évitant ainsi les versions majeures.

### Strawberry

Strawberry est une bibliothèque pour la création de serveurs GraphQL en Python. Elle utilise les dernières fonctionnalités de Python, y compris les annotations de type, pour définir le schéma GraphQL.

- **Sécurité** : Strawberry fournit une intégration directe avec FastAPI, offrant ainsi toutes les fonctionnalités de sécurité fournies par FastAPI.
- **Intégration avec ASGI** : Strawberry peut fonctionner avec n'importe quel serveur ASGI, permettant une flexibilité maximale dans le choix du serveur.

### Autres outils et bibliothèques

- **bcrypt** : Pour le hachage des mots de passe. Il est essentiel de ne jamais stocker les mots de passe en clair dans la base de données.
- **Pydantic** : Pour la validation des données et la sérialisation/désérialisation des modèles.

---