from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CategorieProduit, Produit, DemandeDevis


def index(request):
    """Page principale Import-Export (Pôle D)."""
    if request.method == 'POST':
        nom_entreprise = request.POST.get('nom_entreprise', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        produits_recherches = request.POST.get('produits_recherches', '').strip()
        quantite_estimee = request.POST.get('quantite_estimee', '').strip()
        ville_livraison = request.POST.get('ville_livraison', '').strip()

        if nom_entreprise and telephone and produits_recherches and ville_livraison:
            DemandeDevis.objects.create(
                nom_entreprise=nom_entreprise,
                telephone=telephone,
                produits_recherches=produits_recherches,
                quantite_estimee=quantite_estimee,
                ville_livraison=ville_livraison,
            )
            messages.success(request, "Votre demande de devis a été enregistrée avec succès ! Notre équipe commerciale vous répondra sous 48h.")
            return redirect('materiaux:index')
        else:
            messages.error(request, "Veuillez renseigner votre entreprise/nom, téléphone, produit(s) et ville de livraison.")

    categories = CategorieProduit.objects.prefetch_related('produits').all()
    produits = Produit.objects.filter(disponible=True)

    context = {
        'active_nav': 'import-export',
        'categories': categories,
        'produits': produits,
    }
    return render(request, 'import-export.html', context)


def materiaux(request):
    """Gros œuvre & Matériaux."""
    produits = Produit.objects.filter(disponible=True)
    return render(request, 'import-export-materiaux.html', {'active_nav': 'import-export', 'produits': produits})


def equipements(request):
    """Équipements techniques."""
    produits = Produit.objects.filter(disponible=True)
    return render(request, 'import-export-equipements.html', {'active_nav': 'import-export', 'produits': produits})


def engins(request):
    """Engins de chantier & Outillage."""
    produits = Produit.objects.filter(disponible=True)
    return render(request, 'import-export-engins.html', {'active_nav': 'import-export', 'produits': produits})
