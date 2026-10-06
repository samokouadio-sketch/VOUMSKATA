from django.conf import settings
from django.db import models


class SujetContact(models.TextChoices):
    CONCEPTION = 'conception', 'A — Conception (étude, plans, devis)'
    REALISATION = 'realisation', 'B — Réalisation (construction)'
    GESTION = 'gestion', 'C — Gestion immobilière'
    IMPORT_EXPORT = 'import_export', 'D — Import-export de matériaux'
    AUTRE = 'autre', 'Autre demande'


class MessageContact(models.Model):
    """Formulaire de contact général, routé par pôle."""

    nom_complet = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30)
    email = models.EmailField()
    sujet = models.CharField(max_length=20, choices=SujetContact.choices, default=SujetContact.AUTRE)
    message = models.TextField()
    traite = models.BooleanField(default=False)
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages_traites'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom_complet} — {self.get_sujet_display()}"
