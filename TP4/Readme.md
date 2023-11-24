# TP 4 : API d'Indicateurs Financiers avec Gestion des Niveaux d'Accès
Matthieu Monnot, Guillaume Sima & Cyprien Tardivel

Cette application FastAPI permet de recupérer des données de marché Binance, pour le calcul du Rendement, du Money Flow Classique, du RSI, du MACD et du SMA, d'un symbol donné. 
Les données sont extraites de l'API Binance, et les résultats sont mis en cache pour optimiser les performances.

## Prérequis
Package à installer :
    - pip install fastapi requests

Exécutez l'application : 
    - uvicorn main:app --reload

Accédez à la documentation FastAPI à l'adresse http://127.0.0.1:8000/docs

Pour s'authentifier, voir la base de donnée 'db_users.json' ou bien créer un nouvel utilisateur. 

## Fonctions
### Rendement
 - Point d'accès : '/rendement'
 - Accès : Tout le monde
 - Paramètres :
      - symbol (str) : Symbole de la cryptomonnaie (par exemple, BTCUSDT).
      - loadcash (bool) : Spécifiez s'il faut charger depuis le cache (True/False).
- Description : Calcule et renvoie le Rendement pour le symbole de cryptomonnaie spécifié.

### Money Flow Classique
- Point d'accès : '/moneyflowclassique'
- Accès : Abonnment Gratuit
- Paramètres :
    - symbol (str) : Symbole de la cryptomonnaie (par exemple, BTCUSDT).
    - loadcash (bool) : Spécifiez s'il faut charger depuis le cache (True/False).
- Description : Calcule et renvoie le Money Flow Classique pour le symbole de cryptomonnaie spécifié.

### RSI (Relative Strength Index)
- Point d'accès : '/rsi'
- Accès : Abonnment Premium
- Paramètres :
    - symbol (str) : Symbole de la cryptomonnaie (par exemple, BTCUSDT). 
    - loadcash (bool) : Spécifiez s'il faut charger depuis le cache (True/False).
- Description : Calcule et renvoie le RSI (Relative Strength Index) pour le symbole de cryptomonnaie spécifié.

### MACD (Moving Average Convergence Divergence)
- Point d'accès : '/macd'
- Accès : Abonnment Company
- Paramètres :
    - symbol (str) : Symbole de la cryptomonnaie (par exemple, BTCUSDT).
    - loadcash (bool) : Spécifiez s'il faut charger depuis le cache (True/False).
- Description : Calcule et renvoie le MACD (Moving Average Convergence Divergence) pour le symbole de cryptomonnaie spécifié.

### SMA (Simple Moving Average)
- Point d'accès : '/sma'
- Accès : Abonnment Premium et Company
- Paramètres :
    - symbol (str) : Symbole de la cryptomonnaie (par exemple, BTCUSDT). 
    - loadcash (bool) : Spécifiez s'il faut charger depuis le cache (True/False).
- Description : Calcule et renvoie la SMA (Simple Moving Average) pour le symbole de cryptomonnaie spécifié.

### Token
- Point d'accès : '/token'
- Paramètres :
    - form_data (OAuth2PasswordRequestForm) : Données du formulaire contenant le nom d'utilisateur et le mot de passe.
- Description : Génère et renvoie un jeton d'accès pour le nom d'utilisateur et le mot de passe fournis.

### Profil
- Point d'accès : '/profil'
- Accès : Utilisateur avec un login
- Description : Récupère le profil de l'utilisateur en fonction du jeton d'accès fourni.

### Mettre à jour l'abonnement
- Point d'accès : '/updateSubscription'
- Accès : Utilisateur avec un login
- Paramètres :
    - SubscriptionUpdate (str) : Nouveau type d'abonnement.
- Description : Met à jour le type d'abonnement de l'utilisateur.

### S'inscrire
- Point d'accès : '/register'
- Accès : Utilisateur sans login
- Paramètres :
    - username (str) : Nom d'utilisateur de l'utilisateur. 
    - password (str) : Mot de passe de l'utilisateur. 
    - full_name (str) : Nom complet de l'utilisateur. 
    - email (str) : E-mail de l'utilisateur. 
    - abonement (str) : Type d'abonnement de l'utilisateur.
- Description : Enregistre un nouvel utilisateur avec les informations fournies.
Les utilasteurs déjà enregistraient ne peuvent pas s'enregistrer de nouveau. 

### Supprimer un utilisateur
- Point d'accès : '/delete_user'
- Accès : Utilisateur avec un login
- Paramètres :
    - username (str) : Nom d'utilisateur de l'utilisateur à supprimer. 
- Description : Supprime l'utilisateur connecté actuel avec le nom d'utilisateur spécifié.

### Rate limiting
Un système de rate limiting a été implémenté permettant de contrôler le nombre maximum de requête par route et par minute 
La fonction rate_limit_middleware est un intermédiaire dans le protocol HTTP du server de l'API qui gère cette fonctionnalité.

## Structure du dossier
- main.py : lance l'app grâce à l'import 
- app.py : server et fonctions
- Authentification.py : contient des fonctions qui gérent l'authentifications des utilisateurs, le chargement du fichier json, création et suppression d'utilisateurs 
- db_users.json : contient les informations des utilisateurs sous forme de dictionnaire
- cache_directory : répertoire pour stocker les fichiers de cache.