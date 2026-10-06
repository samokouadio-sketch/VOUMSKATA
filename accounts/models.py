from django.conf import settings
from django.db import models


class Profil(models.Model):
    """Rôle back-office d'un utilisateur (cf. cahier des charges §9 : admin, commercial, gestionnaire de biens)."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrateur'
        COMMERCIAL = 'commercial', 'Commercial'
        GESTIONNAIRE = 'gestionnaire', 'Gestionnaire de biens'

    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil'
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.COMMERCIAL)
    telephone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"{self.utilisateur.get_full_name() or self.utilisateur.username} ({self.get_role_display()})"
