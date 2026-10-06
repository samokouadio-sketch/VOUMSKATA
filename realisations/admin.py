from django.contrib import admin
from .models import Realisation, EtapeChantier, GalerieImage


class EtapeChantierInline(admin.TabularInline):
    model = EtapeChantier
    extra = 1


class GalerieImageInline(admin.TabularInline):
    model = GalerieImage
    extra = 1


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_bien', 'ville', 'annee_livraison', 'superficie_m2', 'en_avant')
    list_filter = ('type_bien', 'ville', 'annee_livraison', 'en_avant')
    search_fields = ('titre', 'ville', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    inlines = [EtapeChantierInline, GalerieImageInline]
