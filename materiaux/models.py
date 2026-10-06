from django.db import models
from habitat.utils import slugify_fr


class CategorieProduit(models.Model):
    """Catégorie du catalogue import-export (pôle D) : Gros œuvre, Outillage, Engins, Équipements techniques."""

    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)

    class Meta:
        verbose_name = "Catégorie de produit"
        verbose_name_plural = "Catégories de produits"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_fr(self.nom)[:110]
        super().save(*args, **kwargs)


class TypeOffre(models.TextChoices):
    VENTE = 'vente', 'Vente'
    LOCATION = 'location', 'Location'


class Produit(models.Model):
    """Matériau, outil ou engin du catalogue import-export."""

    nom = models.CharField(max_length=150)
    categorie = models.ForeignKey(CategorieProduit, on_delete=models.PROTECT, related_name='produits')
    type_offre = models.CharField(max_length=10, choices=TypeOffre.choices)
    prix_indicatif = models.CharField(
        max_length=100, blank=True, help_text="Ex. « À partir de 4 500 F » ou « Sur devis »"
    )
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='materiaux/produits/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['categorie', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.get_type_offre_display()})"


class DemandeDevis(models.Model):
    """Formulaire « Demande de devis fournisseur » — page Import-export (pôle D)."""

    nom_entreprise = models.CharField("Nom / entreprise", max_length=150)
    telephone = models.CharField(max_length=30)
    produits_recherches = models.TextField("Produit(s) recherché(s)")
    quantite_estimee = models.CharField(max_length=100, blank=True)
    ville_livraison = models.CharField(max_length=100)
    statut = models.CharField(
        max_length=20,
        choices=[('nouveau', 'Nouveau'), ('en_cours', 'En cours'), ('traite', 'Traité')],
        default='nouveau',
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande de devis"
        verbose_name_plural = "Demandes de devis"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom_entreprise} — {self.ville_livraison}"
