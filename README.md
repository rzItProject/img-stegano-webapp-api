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

D'accord, intégrons cela au README.

---

## Mise en place de PostgreSQL

La base de données choisie pour ce projet est PostgreSQL. Voici comment la configurer et la mettre en place sur Windows.

1. **Téléchargement et installation**:
   - Visitez le [site officiel de PostgreSQL](https://www.postgresql.org/download/windows/) pour télécharger l'installateur pour Windows.

2. **Démarrage du service PostgreSQL** :
   PostgreSQL s'installe en tant que service Windows qui démarre automatiquement. Vous pouvez le gérer depuis le panneau de configuration des services Windows.

3. **Connexion avec l'utilisateur par défaut** :
   - Ouvrez le terminal de commande (CMD) en tant qu'administrateur.
   - Accédez au répertoire `bin` de votre installation PostgreSQL ou modifier vos variables d'environnements pour rendre la commande `psql`. ([voir tuto](https://www.commandprompt.com/education/how-to-set-windows-path-for-postgres-tools/#:~:text=To%20set%20Windows%20PATH%20for%20PostgreSQL%20tools%2C%20firstly%2C%20open%20System,button%20to%20save%20all%20the))
   - Connectez-vous à PostgreSQL avec `psql -U postgres`.
   - Par défaut, l'utilisateur **postgres** est créé. Vous devrez peut-être définir un mot de passe pour cet utilisateur : `\password postgre`

### Quelques commandes à connaître :

1. **Création d'une nouvelle base de données** :
   ```sql
   CREATE DATABASE mon_nouvelle_base;
   ```

2. **Connexion à la nouvelle base de données** :
   ```bash
   \c mon_nouvelle_base
   ```

3. **Création d'un nouvel utilisateur et attribution des droits utilisateur** :
   ```sql
   CREATE USER mon_utilisateur WITH PASSWORD 'mon_mot_de_passe';
   GRANT ALL PRIVILEGES ON DATABASE mon_nouvelle_base TO mon_utilisateur;
   ```

4. **Connexion avec le nouvel utilisateur** :
   Quittez `psql` avec la commande `\q`, puis reconnectez-vous avec votre nouvel utilisateur :
   ```bash
   psql -U mon_utilisateur -d mon_nouvelle_base -W
   ```

5. **Suppression d'une base de données** :
   Pour supprimer une base de données, utilisez la commande :
   ```sql
   DROP DATABASE [NOM_BASE_DE_DONNEES]
   ```
   
6. **Changer le port et l'hôte** :
   Pour supprimer une base de données, utilisez la commande :
   ```bash
   psql -h [NOM_DU_SERVEUR] -p [NUMERO_DU_PORT] -U [NOM_UTILISATEUR] [NOM_BASE_DE_DONNEES]
   ```

Voici d'autres commandes courantes et utiles à utiliser dans le shell `psql` de PostgreSQL :

#### Commandes générales :

- `\q` : Quitter `psql`.
- `\h` : Afficher l'aide sur les commandes SQL.
- `\?` : Afficher l'aide sur les commandes `psql`.

#### Commandes relatives aux bases de données :

- `\l` ou `\list` : Lister toutes les bases de données.
- `\c [nom_base_de_donnees]` : Se connecter à une base de données.
- `\conninfo` : Afficher les informations de la connexion actuelle.

#### Commandes relatives aux tables :

- `\dt` : Lister toutes les tables de la base de données actuelle.
- `\d [nom_table]` : Afficher la structure d'une table.
- `\di` : Lister tous les index de la base de données actuelle.
- `\dv` : Lister toutes les vues de la base de données actuelle.
- `\df` : Lister toutes les fonctions de la base de données actuelle.

#### Commandes pour manipuler les résultats :

- `\a` : Basculer entre l'affichage aligné et non aligné.
- `\x` : Basculer entre l'affichage normal et l'affichage étendu.
- `\e` : Ouvrir la dernière commande exécutée dans un éditeur pour la modifier.
- `\s` : Afficher l'historique des commandes.
- `\s [nom_fichier]` : Sauvegarder l'historique des commandes dans un fichier.
- `\i [nom_fichier]` : Exécuter les commandes SQL depuis un fichier.

#### Autres commandes utiles :

- `\timing` : Mesurer et afficher le temps d'exécution des commandes.
- `\set` : Afficher toutes les variables `psql`.
- `\unset [nom_variable]` : Supprimer une variable.

---
