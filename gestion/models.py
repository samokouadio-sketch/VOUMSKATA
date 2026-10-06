from django.db import models


class Proprietaire(models.Model):
    """Propriétaire ayant confié un bien en gestion (pôle C)."""

    nom_complet = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Propriétaire"
        verbose_name_plural = "Propriétaires"

    def __str__(self):
        return self.nom_complet


class TypeBienGestion(models.TextChoices):
    VILLA = 'villa', 'Villa'
    APPARTEMENT = 'appartement', 'Appartement'
    IMMEUBLE = 'immeuble', 'Immeuble'
    TERRAIN = 'terrain', 'Terrain'


class Transaction(models.TextChoices):
    LOUER = 'louer', 'À louer'
    VENDRE = 'vendre', 'À vendre'


class StatutBien(models.TextChoices):
    DISPONIBLE = 'disponible', 'Disponible'
    RESERVE = 'reserve', 'Réservé'
    LOUE = 'loue', 'Loué'
    VENDU = 'vendu', 'Vendu'


class Bien(models.Model):
    """Bien immobilier proposé à la location ou à la vente."""

    titre = models.CharField(max_length=150)
    type_bien = models.CharField(max_length=20, choices=TypeBienGestion.choices)
    transaction = models.CharField(max_length=10, choices=Transaction.choices)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100, blank=True)
    prix = models.DecimalField(max_digits=12, decimal_places=0, help_text="En FCFA (par mois si location)")
    chambres = models.PositiveSmallIntegerField(default=0)
    superficie_m2 = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image_principale = models.ImageField(upload_to='gestion/biens/', blank=True, null=True)
    statut = models.CharField(max_length=15, choices=StatutBien.choices, default=StatutBien.DISPONIBLE)
    proprietaire = models.ForeignKey(
        Proprietaire, on_delete=models.SET_NULL, null=True, blank=True, related_name='biens'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bien"
        verbose_name_plural = "Biens"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} — {self.get_transaction_display()} — {self.ville}"


class ObjectifGestion(models.TextChoices):
    LOUER = 'louer', 'Louer'
    VENDRE = 'vendre', 'Vendre'
    LES_DEUX = 'les_deux', 'Les deux'
    ENTRETIEN = 'entretien', 'Entretien seul'


class DemandeGestion(models.Model):
    """Formulaire « Confier mon bien » — page Gestion (pôle C)."""

    nom_complet = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    type_bien = models.CharField(max_length=20, choices=TypeBienGestion.choices)
    objectif = models.CharField(max_length=15, choices=ObjectifGestion.choices)
    adresse_bien = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    statut = models.CharField(
        max_length=20,
        choices=[('nouveau', 'Nouveau'), ('en_cours', 'En cours'), ('traite', 'Traité')],
        default='nouveau',
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande de gestion"
        verbose_name_plural = "Demandes de gestion"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom_complet} — {self.get_objectif_display()} ({self.adresse_bien})"
