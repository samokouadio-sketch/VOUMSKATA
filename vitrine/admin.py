from django.contrib import admin
from .models import Temoignage, ValeurEntreprise, MembreEquipe, Certification, StatistiqueCle


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role_client', 'note', 'actif', 'ordre')
    list_filter = ('actif',)
    ordering = ('ordre',)


@admin.register(ValeurEntreprise)
class ValeurEntrepriseAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre')
    ordering = ('ordre',)


@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'ordre')
    ordering = ('ordre',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre')
    ordering = ('ordre',)


@admin.register(StatistiqueCle)
class StatistiqueCleAdmin(admin.ModelAdmin):
    list_display = ('cle', 'valeur', 'libelle', 'ordre')
    ordering = ('ordre',)
