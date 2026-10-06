from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Bien, DemandeGestion, TypeBienGestion, Transaction, ObjectifGestion


def index(request):
    """Page principale Gestion immobilière (Pôle C)."""
    if request.method == 'POST':
        nom_complet = request.POST.get('nom_complet', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        type_bien = request.POST.get('type_bien', TypeBienGestion.VILLA)
        objectif = request.POST.get('objectif', ObjectifGestion.LOUER)
        adresse_bien = request.POST.get('adresse_bien', '').strip()
        message = request.POST.get('message', '').strip()

        if nom_complet and telephone and adresse_bien:
            DemandeGestion.objects.create(
                nom_complet=nom_complet,
                telephone=telephone,
                email=email,
                type_bien=type_bien,
                objectif=objectif,
                adresse_bien=adresse_bien,
                message=message,
            )
            messages.success(request, "Votre demande de gestion a été bien enregistrée ! Notre gestionnaire vous recontactera sous peu.")
            return redirect('gestion:index')
        else:
            messages.error(request, "Veuillez renseigner votre nom, votre téléphone et l'adresse de votre bien.")

    biens = Bien.objects.filter(statut='disponible')
    context = {
        'active_nav': 'gestion',
        'biens': biens,
        'types_bien': TypeBienGestion.choices,
        'objectifs': ObjectifGestion.choices,
    }
    return render(request, 'gestion.html', context)


def acd(request):
    """Accompagnement ACD / Foncier."""
    return render(request, 'gestion-acd.html', {'active_nav': 'gestion'})


def locative(request):
    """Gestion locative sur-mesure."""
    return render(request, 'gestion-locative.html', {'active_nav': 'gestion'})


def louer(request):
    """Biens à louer."""
    type_filter = request.GET.get('type')
    biens = Bien.objects.filter(transaction=Transaction.LOUER)
    if type_filter:
        biens = biens.filter(type_bien=type_filter)
    return render(request, 'gestion-louer.html', {
        'active_nav': 'gestion',
        'biens': biens,
        'types_bien': TypeBienGestion.choices,
        'current_type': type_filter,
    })


def vendre(request):
    """Biens à vendre."""
    type_filter = request.GET.get('type')
    biens = Bien.objects.filter(transaction=Transaction.VENDRE)
    if type_filter:
        biens = biens.filter(type_bien=type_filter)
    return render(request, 'gestion-vendre.html', {
        'active_nav': 'gestion',
        'biens': biens,
        'types_bien': TypeBienGestion.choices,
        'current_type': type_filter,
    })


def detail_bien(request, pk):
    """Fiche d'un bien en gestion."""
    bien = get_object_or_404(Bien, pk=pk)
    biens_similaires = Bien.objects.filter(transaction=bien.transaction).exclude(id=bien.id)[:3]
    return render(request, 'gestion-bien-detail.html', {
        'active_nav': 'gestion',
        'bien': bien,
        'biens_similaires': biens_similaires,
    })
