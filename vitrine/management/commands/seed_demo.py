"""
Peuple la base avec le contenu de démonstration déjà présent dans la maquette
HTML (mêmes projets, biens, produits, témoignages, statistiques) — pratique
pour développer et présenter le back-office sans ressaisir de données.

Usage : python manage.py seed_demo [--flush]
"""
import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from realisations.models import Realisation, EtapeChantier
from gestion.models import Bien
from materiaux.models import CategorieProduit, Produit
from vitrine.models import Temoignage, ValeurEntreprise, StatistiqueCle


def _make_placeholder_bytes():
    """Génère un petit PNG uni (sable de la charte) en mémoire — à remplacer par de vraies photos."""
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (600, 400), (247, 244, 239)).save(buf, format="PNG")
    return buf.getvalue()


class Command(BaseCommand):
    help = "Peuple la base avec le contenu de démonstration de la maquette."

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help="Supprime les données de démo existantes avant de reseeder.")

    def handle(self, *args, **options):
        if options['flush']:
            Realisation.objects.all().delete()
            Bien.objects.all().delete()
            Produit.objects.all().delete()
            CategorieProduit.objects.all().delete()
            Temoignage.objects.all().delete()
            ValeurEntreprise.objects.all().delete()
            StatistiqueCle.objects.all().delete()
            self.stdout.write("Données de démo existantes supprimées.")

        self._seed_realisations()
        self._seed_biens()
        self._seed_materiaux()
        self._seed_temoignages()
        self._seed_valeurs()
        self._seed_stats()
        self.stdout.write(self.style.SUCCESS("Contenu de démonstration inséré avec succès."))

    def _image(self):
        # Nouvelle instance à chaque appel : un ImageField ne peut pas réutiliser un fichier déjà lu.
        return ContentFile(_make_placeholder_bytes(), name="placeholder.png")

    def _seed_realisations(self):
        projets = [
            ("Villa R+1 — 240 m²", "villa", "Cocody", 240, 500, 7, 2025,
             [("Étude & plans", "3 semaines"), ("Fondations", "5 semaines"), ("Gros œuvre", "12 semaines"), ("Finitions", "8 semaines")]),
            ("Résidence — 12 logements", "immeuble", "Yopougon", 980, 1200, 11, 2024, []),
            ("Rénovation villa familiale", "rehabilitation", "Marcory", 210, None, 3, 2025, []),
            ("Villa duplex — 310 m²", "villa", "Bingerville", 310, 600, 9, 2024, []),
            ("Résidence — 8 logements", "immeuble", "Cocody", 640, 900, 10, 2023, []),
            ("Villa contemporaine — 180 m²", "villa", "Riviera", 180, 400, 6, 2025, []),
        ]
        for titre, type_bien, ville, superficie, terrain, duree, annee, etapes in projets:
            r, created = Realisation.objects.get_or_create(
                titre=titre,
                defaults=dict(
                    type_bien=type_bien, ville=ville, superficie_m2=superficie,
                    superficie_terrain_m2=terrain, duree_mois=duree, annee_livraison=annee,
                    image_principale=self._image(), en_avant=(titre.startswith("Villa R+1")),
                ),
            )
            for ordre, (etitre, edur) in enumerate(etapes, start=1):
                EtapeChantier.objects.get_or_create(realisation=r, titre=etitre, defaults=dict(duree=edur, ordre=ordre))
        self.stdout.write(f"Réalisations : {Realisation.objects.count()}")

    def _seed_biens(self):
        biens = [
            ("Villa moderne 4 pièces", "villa", "louer", "Cocody", "Angré", 450000, 4, 220),
            ("Appartement standing", "appartement", "louer", "Marcory", "", 280000, 2, 85),
            ("Duplex meublé", "villa", "louer", "Riviera", "", 600000, 3, 160),
            ("Villa R+1 à vendre", "villa", "vendre", "Bingerville", "", 85000000, 4, 240),
            ("Terrain viabilisé + ACD", "terrain", "vendre", "Songon", "", 22000000, 0, 600),
            ("Immeuble R+2 de rapport", "immeuble", "vendre", "Yopougon", "", 120000000, 8, 420),
        ]
        for titre, type_bien, transaction, ville, quartier, prix, chambres, superficie in biens:
            Bien.objects.get_or_create(
                titre=titre,
                defaults=dict(
                    type_bien=type_bien, transaction=transaction, ville=ville, quartier=quartier,
                    prix=prix, chambres=chambres, superficie_m2=superficie,
                ),
            )
        self.stdout.write(f"Biens : {Bien.objects.count()}")

    def _seed_materiaux(self):
        categories = ["Gros œuvre", "Outillage", "Engins", "Équipements techniques"]
        cats = {nom: CategorieProduit.objects.get_or_create(nom=nom)[0] for nom in categories}

        produits = [
            ("Ciment (sac 50kg)", "Gros œuvre", "vente", "À partir de 4 500 F"),
            ("Fer à béton HA", "Gros œuvre", "vente", "Prix sur devis"),
            ("Carrelage & faïence", "Gros œuvre", "vente", "Prix sur devis"),
            ("Bétonnière 350L", "Outillage", "location", "25 000 F/jour"),
            ("Pelle mécanique", "Engins", "location", "Sur devis"),
            ("Grue de chantier", "Engins", "location", "Sur devis"),
            ("Peinture bâtiment", "Équipements techniques", "vente", "À partir de 12 000 F"),
            ("Groupe électrogène", "Équipements techniques", "location", "15 000 F/jour"),
        ]
        for nom, cat_nom, type_offre, prix in produits:
            Produit.objects.get_or_create(
                nom=nom, defaults=dict(categorie=cats[cat_nom], type_offre=type_offre, prix_indicatif=prix)
            )
        self.stdout.write(f"Produits : {Produit.objects.count()}")

    def _seed_temoignages(self):
        temoignages = [
            ("Koffi T.", "Propriétaire, Cocody",
             "Du terrain nu à la villa livrée, un seul interlocuteur a suivi tout le projet — les délais annoncés ont été tenus."),
            ("Aïcha D.", "Bailleuse, Yopougon",
             "Nous confions la gestion locative de trois immeubles depuis deux ans : les loyers arrivent, sans que nous ayons à gérer les locataires."),
            ("Sekou O.", "Chef de chantier",
             "Notre entreprise de BTP s'approvisionne désormais chez eux pour le matériel : livraison directe sur chantier, prix constants."),
        ]
        for ordre, (nom, role, texte) in enumerate(temoignages, start=1):
            Temoignage.objects.get_or_create(nom=nom, defaults=dict(role_client=role, texte=texte, ordre=ordre))
        self.stdout.write(f"Témoignages : {Temoignage.objects.count()}")

    def _seed_valeurs(self):
        valeurs = [
            ("Transparence", "Devis détaillés, délais annoncés et tenus, aucune surprise en cours de chantier."),
            ("Intégration", "Conception, réalisation, gestion et matériaux gérés par la même équipe, du début à la fin."),
            ("Exigence technique", "Conformité aux normes ivoiriennes à chaque étape, du sol aux finitions."),
        ]
        for ordre, (titre, desc) in enumerate(valeurs, start=1):
            ValeurEntreprise.objects.get_or_create(titre=titre, defaults=dict(description=desc, ordre=ordre))
        self.stdout.write(f"Valeurs : {ValeurEntreprise.objects.count()}")

    def _seed_stats(self):
        stats = [
            ("chantiers_livres", "120+", "Chantiers livrés"),
            ("m2_construits", "48 000", "m² construits"),
            ("annees_experience", "9", "Années d'expérience"),
            ("biens_gestion", "300+", "Biens en gestion"),
        ]
        for ordre, (cle, valeur, libelle) in enumerate(stats, start=1):
            StatistiqueCle.objects.get_or_create(cle=cle, defaults=dict(valeur=valeur, libelle=libelle, ordre=ordre))
        self.stdout.write(f"Statistiques : {StatistiqueCle.objects.count()}")
