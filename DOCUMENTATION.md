# Documentation Technique & Guide d'Utilisation — HABITAT Construction Sarl

Ce document fournit la documentation complète du projet : architecture, fonctionnement en local, administration des données et procédure étape par étape pour le déploiement sur **Supabase** et **Vercel**.

---

## 1. Vue d'ensemble de l'Architecture

Le projet **HABITAT Construction Sarl** associe un backend **Django 5.0** découplé par pôles d'activité avec un frontend dynamisé basé sur le moteur de templates de Django.

```
VOUMSKATA/
├── api/
│   └── index.py            # Point d'entrée WSGI Serverless Vercel
├── habitat/                # Configuration principale Django (settings, urls, wsgi, __init__)
├── accounts/               # Authentification et rôles administrateurs
├── actualites/             # Modèle Article, vues et actualités
├── conception/             # Pôle A : PlanType, DemandeEtude
├── realisations/           # Pôle B : Realisation, EtapeChantier, GalerieImage
├── gestion/                # Pôle C : Proprietaire, Bien, DemandeGestion
├── materiaux/              # Pôle D : CategorieProduit, Produit, DemandeDevis
├── contact/                # MessageContact (routage par pôle)
├── vitrine/                # Temoignage, ValeurEntreprise, Certification, StatistiqueCle, seed_demo
├── static/                 # Fichiers statiques (CSS, JS, images de la maquette)
├── templates/              # Templates HTML dynamisés (base.html + 22 pages)
├── media/                  # Fichiers médias téléversés
├── manage.py               # Script de gestion Django
├── vercel.json             # Descripteur de déploiement Vercel
├── build.sh                # Script de build (collectstatic)
├── requirements.txt        # Dépendances Python du projet
└── .env.example            # Modèle de variables d'environnement
```

---

## 2. Guide d'Exécution en Local

### Prérequis
- Python 3.10 ou supérieur.

### Étapes d'installation
1. Ouvrez un terminal dans le dossier du projet (`VOUMSKATA`).
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Exécutez les migrations de base de données :
   ```bash
   python manage.py migrate
   ```
4. Peuplez la base de données avec le contenu de démonstration de la maquette :
   ```bash
   python manage.py seed_demo
   ```
5. Créez un compte administrateur (Back-office) :
   ```bash
   python manage.py createsuperuser
   ```
6. Lancez le serveur de développement local :
   ```bash
   python manage.py runserver
   ```
7. Accédez au site sur `http://127.0.0.1:8000/` et à l'administration sur `http://127.0.0.1:8000/admin/`.

---

## 3. Formulaires & Gestion des Données

Chaque formulaire de la maquette enregistre automatiquement les demandes en base de données et affiche un message de confirmation au visiteur :

| Formulaire | URL Frontend | Modèle Django | Champs principaux enregistrés |
|---|---|---|---|
| **Démarrer une étude** | `/conception/` | `DemandeEtude` | Nom, Téléphone, Email, Ville du terrain, Superficie, Type de projet, Message |
| **Confier mon bien** | `/gestion/` | `DemandeGestion` | Nom, Téléphone, Email, Type de bien, Objectif (louer/vendre), Adresse, Précisions |
| **Demande de devis** | `/import-export/` | `DemandeDevis` | Nom/Entreprise, Téléphone, Produits recherchés, Quantité estimée, Ville de livraison |
| **Contact Général** | `/contact/` | `MessageContact` | Nom, Téléphone, Email, Sujet (pôle), Message |

---

## 4. Administration des Données (Back-Office)

L'administration Django (`/admin/`) permet de :
1. **Consulter et traiter les demandes** reçues depuis les 4 formulaires métier (changement de statut : *Nouveau*, *En cours*, *Traité*).
2. **Ajouter/modifier des réalisations** (avec étapes de chantier et galerie photos).
3. **Gérer le catalogue immobilier** (biens à louer ou à vendre, prix, superficies, statut disponible/loué/vendu).
4. **Mettre à jour le catalogue import-export** (catégories, produits, tarifs indicatifs, disponibilité).
5. **Gérer le contenu du site** (articles de blog, témoignages, chiffres clés, membres d'équipe).

---

## 5. Déploiement étape par étape sur Supabase & Vercel

### Étape A : Base de données Supabase (PostgreSQL)
1. Créez un projet sur [Supabase](https://supabase.com/).
2. Accédez à **Project Settings > Database**.
3. Sous **Connection String**, copiez la chaîne au format **URI** :
   ```text
   postgres://postgres.[PROJECT_REF]:[MOT_DE_PASSE]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

### Étape B : Dépôt GitHub
1. Initialisez Git et poussez le code sur GitHub :
   ```bash
   git init
   git add .
   git commit -m "Site HABITAT Construction dynamisé"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/habitat-construction.git
   git push -u origin main
   ```

### Étape C : Hébergement Vercel
1. Importez votre dépôt GitHub sur [Vercel](https://vercel.com/).
2. Définissez les **Environment Variables** :
   - `DATABASE_URL` = *(l'URI Supabase copiée à l'étape A)*
   - `DJANGO_SECRET_KEY` = `votre_cle_secrete_production`
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` = `.vercel.app`
3. Lancez le déploiement (**Deploy**).

### Étape D : Migration & Seeding de la base de production
Depuis votre terminal local, configurez temporairement la variable `DATABASE_URL` pointant vers Supabase et exécutez :
```powershell
# Windows PowerShell
$env:DATABASE_URL="postgres://postgres.xxxx:mot_de_passe@aws-0-xxxx.pooler.supabase.com:6543/postgres"

python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
```

---

## 6. Commandes utiles de Maintenance

- **Vérification de configuration** : `python manage.py check`
- **Re-seeder les données de démo (réinitialisation)** : `python manage.py seed_demo --flush`
- **Exécution de la suite de tests** : `python manage.py test`
- **Collecte des statiques (WhiteNoise)** : `python manage.py collectstatic --noinput`
