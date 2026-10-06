from django.db import models


class TypeProjet(models.TextChoices):
    VILLA = 'villa', 'Villa individuelle'
    IMMEUBLE = 'immeuble', 'Immeuble locatif'
    REHABILITATION = 'rehabilitation', 'Réhabilitation'
    AUTRE = 'autre', 'Autre'


class StatutDemande(models.TextChoices):
    NOUVEAU = 'nouveau', 'Nouveau'
    EN_COURS = 'en_cours', 'En cours de traitement'
    TRAITE = 'traite', 'Traité'
    ARCHIVE = 'archive', 'Archivé'


class DemandeEtude(models.Model):
    """Formulaire « Démarrer une étude » — page Conception (pôle A)."""

    nom_complet = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    ville_terrain = models.CharField("Ville / localisation du terrain", max_length=150)
    superficie_terrain = models.CharField("Superficie du terrain", max_length=50, blank=True)
    type_projet = models.CharField(max_length=20, choices=TypeProjet.choices, default=TypeProjet.VILLA)
    message = models.TextField("Votre projet en quelques mots", blank=True)
    statut = models.CharField(max_length=20, choices=StatutDemande.choices, default=StatutDemande.NOUVEAU)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande d'étude"
        verbose_name_plural = "Demandes d'étude"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom_complet} — {self.get_type_projet_display()} ({self.ville_terrain})"


class PlanType(models.Model):
    """Plans-types / rendus 3D présentés en exemple sur la page Conception."""

    class TypeRendu(models.TextChoices):
        PLAN_2D = 'plan_2d', 'Plan 2D'
        RENDU_3D = 'rendu_3d', 'Rendu 3D'

    titre = models.CharField(max_length=150)
    type_rendu = models.CharField(max_length=10, choices=TypeRendu.choices, default=TypeRendu.PLAN_2D)
    superficie = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='conception/plans/')
    description = models.CharField(max_length=255, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Plan-type"
        verbose_name_plural = "Plans-types"
        ordering = ['ordre']

    def __str__(self):
        return self.titre
