# HABITAT Construction Sarl — Backend Django

Base de données et back-office (Django Admin) pour le site HABITAT Construction
Sarl. Un app Django par pôle métier, conforme à l'arborescence validée dans le
cahier des charges (§5) et à l'option technique A (§6).

## Structure

```
habitat_backend/
├── habitat/            Réglages du projet (settings, urls, utils)
├── accounts/           Rôles back-office (admin, commercial, gestionnaire)
├── conception/         A — Demandes d'étude, plans-types
├── realisations/       B — Réalisations, étapes de chantier, galerie
├── gestion/             C — Biens (location/vente), propriétaires, demandes
├── materiaux/           D — Catégories, produits, demandes de devis
├── actualites/          Articles / blog
├── contact/             Messages de contact (routés par pôle)
├── vitrine/              Témoignages, valeurs, équipe, certifications,
│                         statistiques clés + commande `seed_demo`
├── requirements.txt
├── .env.example
└── manage.py
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # puis renseigner vos identifiants MySQL
```

Créer la base MySQL (une fois, en dehors de Django) :

```sql
CREATE DATABASE habitat_construction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'habitat_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON habitat_construction.* TO 'habitat_user'@'localhost';
```

Puis :

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Back-office disponible sur `http://127.0.0.1:8000/admin/`.

> Le projet utilise **PyMySQL** (driver MySQL pur Python, activé dans
> `habitat/__init__.py`) plutôt que `mysqlclient`, pour éviter d'avoir à
> compiler une dépendance native en développement. En production, vous pouvez
> retirer ces 2 lignes et installer `mysqlclient` à la place (plus rapide).

## Peupler avec le contenu de démonstration de la maquette

```bash
python manage.py seed_demo
```

Insère les 6 réalisations, 6 biens, 8 produits, 3 témoignages, 3 valeurs et 4
statistiques déjà utilisés dans la maquette HTML — pratique pour développer
sans ressaisir de données, ou pour une démo. Option `--flush` pour vider les
tables concernées avant de reseeder.

## Modèles principaux

| App | Modèles |
|---|---|
| accounts | `Profil` (rôle : admin / commercial / gestionnaire) |
| conception | `DemandeEtude`, `PlanType` |
| realisations | `Realisation`, `EtapeChantier`, `GalerieImage` |
| gestion | `Proprietaire`, `Bien`, `DemandeGestion` |
| materiaux | `CategorieProduit`, `Produit`, `DemandeDevis` |
| actualites | `Article` |
| contact | `MessageContact` |
| vitrine | `Temoignage`, `ValeurEntreprise`, `MembreEquipe`, `Certification`, `StatistiqueCle` |

Chaque formulaire du site (maquette HTML) correspond à un modèle de demande
(`DemandeEtude`, `DemandeGestion`, `DemandeDevis`, `MessageContact`) — reste à
brancher les vues/API qui les enregistrent lors de l'intégration du front-end.

## Prochaines étapes suggérées

- Vues + endpoints (Django REST Framework ou vues classiques + templates) pour
  connecter le site HTML/CSS/JS déjà livré à cette base.
- Upload et redimensionnement automatique des images (`Pillow` déjà en place).
- Permissions par rôle dans l'admin (actuellement tous les modèles sont
  visibles par tout superuser ; à affiner selon `Profil.role` si plusieurs
  comptes non-superuser doivent accéder à l'admin).
- Déploiement : `DEBUG=False`, `DJANGO_ALLOWED_HOSTS` renseigné, fichiers
  statiques servis via `collectstatic` + un serveur web (nginx, whitenoise…).
