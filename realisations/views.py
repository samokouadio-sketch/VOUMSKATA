from django.shortcuts import render, get_object_or_404
from .models import Realisation, TypeBien, EtapeChantier, GalerieImage


def index(request):
    """Portfolio des réalisations (Pôle B)."""
    type_bien_filter = request.GET.get('type')
    realisations = Realisation.objects.all()

    if type_bien_filter in [choice[0] for choice in TypeBien.choices]:
        realisations = realisations.filter(type_bien=type_bien_filter)

    context = {
        'active_nav': 'realisation',
        'realisations': realisations,
        'types_bien': TypeBien.choices,
        'current_type': type_bien_filter,
    }
    return render(request, 'realisations.html', context)


def methode(request):
    """Méthode et déroulé de chantier."""
    return render(request, 'realisation-methode.html', {'active_nav': 'realisation'})


def detail(request, slug):
    """Fiche détaillée d'une réalisation."""
    realisation = get_object_or_404(Realisation, slug=slug)
    etapes = realisation.etapes.all()
    galerie = realisation.galerie.all()
    autres_realisations = Realisation.objects.exclude(id=realisation.id)[:3]

    context = {
        'active_nav': 'realisation',
        'realisation': realisation,
        'etapes': etapes,
        'galerie': galerie,
        'autres_realisations': autres_realisations,
    }
    return render(request, 'realisation-detail.html', context)
