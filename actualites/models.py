from django.conf import settings
from django.db import models
from django.utils import timezone
from habitat.utils import slugify_fr


class StatutArticle(models.TextChoices):
    BROUILLON = 'brouillon', 'Brouillon'
    PUBLIE = 'publie', 'Publié'


class Article(models.Model):
    """Article du blog / actualités."""

    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    extrait = models.CharField(max_length=255, help_text="Résumé affiché dans la liste des actualités")
    contenu = models.TextField()
    image = models.ImageField(upload_to='actualites/', blank=True, null=True)
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles'
    )
    statut = models.CharField(max_length=10, choices=StatutArticle.choices, default=StatutArticle.BROUILLON)
    date_publication = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_fr(self.titre)[:220]
        super().save(*args, **kwargs)
