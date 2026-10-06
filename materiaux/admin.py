from django.contrib import admin
from .models import CategorieProduit, Produit, DemandeDevis


@admin.register(CategorieProduit)
class CategorieProduitAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'type_offre', 'prix_indicatif', 'disponible')
    list_filter = ('categorie', 'type_offre', 'disponible')
    search_fields = ('nom', 'description')


@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):
    list_display = ('nom_entreprise', 'ville_livraison', 'statut', 'date_creation')
    list_filter = ('statut',)
    search_fields = ('nom_entreprise', 'telephone', 'produits_recherches')
    date_hierarchy = 'date_creation'
