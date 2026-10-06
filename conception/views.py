from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PlanType, DemandeEtude, TypeProjet


def index(request):
    """Page principale Conception (Pôle A)."""
    if request.method == 'POST':
        nom_complet = request.POST.get('nom_complet', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        ville_terrain = request.POST.get('ville_terrain', '').strip()
        superficie_terrain = request.POST.get('superficie_terrain', '').strip()
        type_projet = request.POST.get('type_projet', TypeProjet.VILLA)
        message = request.POST.get('message', '').strip()

        if nom_complet and telephone and ville_terrain:
            DemandeEtude.objects.create(
                nom_complet=nom_complet,
                telephone=telephone,
                email=email,
                ville_terrain=ville_terrain,
                superficie_terrain=superficie_terrain,
                type_projet=type_projet,
                message=message,
            )
            messages.success(request, "Votre demande d'étude a été transmise avec succès ! Notre équipe vous contactera sous 48h.")
            return redirect('conception:index')
        else:
            messages.error(request, "Veuillez remplir au moins votre nom, téléphone et la localisation de votre terrain.")

    plans_types = PlanType.objects.all()
    context = {
        'active_nav': 'conception',
        'plans_types': plans_types,
        'type_projets': TypeProjet.choices,
    }
    return render(request, 'conception.html', context)


def plans_3d(request):
    """Page Plans 2D et Rendus 3D."""
    plans_types = PlanType.objects.all()
    return render(request, 'conception-plans-3d.html', {'active_nav': 'conception', 'plans_types': plans_types})


def etude_conseil(request):
    """Page Étude & Conseil."""
    return render(request, 'conception-etude-conseil.html', {'active_nav': 'conception'})


def devis(request):
    """Page Devis Conception."""
    return render(request, 'conception-devis.html', {'active_nav': 'conception'})
