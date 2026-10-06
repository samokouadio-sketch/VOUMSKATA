from django.db import models


class Temoignage(models.Model):
    """Avis client affiché sur l'accueil (section « La parole à nos clients »)."""

    nom = models.CharField(max_length=100)
    role_client = models.CharField("Rôle / qualité", max_length=150, help_text="Ex. « Propriétaire, Cocody »")
    texte = models.TextField()
    note = models.PositiveSmallIntegerField(default=5, help_text="Note sur 5")
    actif = models.BooleanField(default=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} — {self.role_client}"


class ValeurEntreprise(models.Model):
    """Carte « Nos valeurs » de la page À propos."""

    titre = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Valeur d'entreprise"
        verbose_name_plural = "Valeurs d'entreprise"
        ordering = ['ordre']

    def __str__(self):
        return self.titre


class MembreEquipe(models.Model):
    """Membre affiché sur la page À propos."""

    nom = models.CharField(max_length=150)
    poste = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='vitrine/equipe/', blank=True, null=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Équipe"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} — {self.poste}"


class Certification(models.Model):
    """Agrément / certification affiché(e) sur la page À propos."""

    nom = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='vitrine/certifications/', blank=True, null=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['ordre']

    def __str__(self):
        return self.nom


class StatistiqueCle(models.Model):
    """Chiffre clé affiché dans les bandeaux stats (accueil + pages pôles).
    Ex. clé=chantiers_livres, valeur=120+, libelle=Chantiers livrés."""

    cle = models.SlugField(max_length=50, unique=True)
    valeur = models.CharField(max_length=20, help_text="Ex. « 120+ », « 48 000 m² », « 9 »")
    libelle = models.CharField(max_length=100, help_text="Ex. « Chantiers livrés »")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Statistique clé"
        verbose_name_plural = "Statistiques clés"
        ordering = ['ordre']

    def __str__(self):
        return f"{self.libelle} : {self.valeur}"
