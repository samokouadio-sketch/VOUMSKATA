from django.db import models
from habitat.utils import slugify_fr


class TypeBien(models.TextChoices):
    VILLA = 'villa', 'Villa'
    IMMEUBLE = 'immeuble', 'Immeuble'
    REHABILITATION = 'rehabilitation', 'Réhabilitation'


class Realisation(models.Model):
    """Projet livré, affiché dans le portfolio (pôle B — Réalisation)."""

    titre = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    type_bien = models.CharField(max_length=20, choices=TypeBien.choices)
    ville = models.CharField(max_length=100)
    superficie_m2 = models.PositiveIntegerField("Superficie (m²)")
    superficie_terrain_m2 = models.PositiveIntegerField("Superficie terrain (m²)", null=True, blank=True)
    duree_mois = models.PositiveSmallIntegerField("Durée du chantier (mois)")
    annee_livraison = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    image_principale = models.ImageField(upload_to='realisations/principales/')
    en_avant = models.BooleanField("Mise en avant sur l'accueil", default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"
        ordering = ['-annee_livraison', '-date_creation']

    def __str__(self):
        return f"{self.titre} — {self.ville} ({self.annee_livraison})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_fr(self.titre)[:170]
        super().save(*args, **kwargs)


class EtapeChantier(models.Model):
    """Étape du déroulé de chantier affichée sur la fiche projet."""

    realisation = models.ForeignKey(Realisation, on_delete=models.CASCADE, related_name='etapes')
    titre = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    duree = models.CharField(max_length=50, blank=True, help_text="Ex. « 3 semaines »")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Étape de chantier"
        verbose_name_plural = "Étapes de chantier"
        ordering = ['realisation', 'ordre']

    def __str__(self):
        return f"{self.realisation.titre} — {self.titre}"


class GalerieImage(models.Model):
    """Photo de galerie associée à une réalisation."""

    realisation = models.ForeignKey(Realisation, on_delete=models.CASCADE, related_name='galerie')
    image = models.ImageField(upload_to='realisations/galerie/')
    legende = models.CharField(max_length=200, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"
        ordering = ['realisation', 'ordre']

    def __str__(self):
        return f"{self.realisation.titre} — image {self.ordre}"
