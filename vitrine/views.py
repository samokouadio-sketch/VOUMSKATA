from django.shortcuts import render
from realisations.models import Realisation
from gestion.models import Bien
from vitrine.models import Temoignage, ValeurEntreprise, MembreEquipe, Certification, StatistiqueCle
from actualites.models import Article


def index(request):
    """Page d'accueil."""
    realisations = Realisation.objects.filter(en_avant=True)[:3]
    if not realisations.exists():
        realisations = Realisation.objects.all()[:3]

    biens = Bien.objects.filter(statut='disponible')[:3]
    if not biens.exists():
        biens = Bien.objects.all()[:3]

    temoignages = Temoignage.objects.filter(actif=True)
    stats = StatistiqueCle.objects.all()
    valeurs = ValeurEntreprise.objects.all()
    articles = Article.objects.filter(statut='publie')[:3]

    context = {
        'active_nav': 'index',
        'realisations': realisations,
        'biens': biens,
        'temoignages': temoignages,
        'stats': stats,
        'valeurs': valeurs,
        'articles': articles,
    }
    return render(request, 'index.html', context)


def a_propos(request):
    """Page À propos."""
    context = {
        'active_nav': 'apropos',
        'equipe': MembreEquipe.objects.all(),
        'certifications': Certification.objects.all(),
        'valeurs': ValeurEntreprise.objects.all(),
        'stats': StatistiqueCle.objects.all(),
    }
    return render(request, 'a-propos.html', context)


def mentions_legales(request):
    """Page Mentions légales."""
    return render(request, 'mentions-legales.html', {'active_nav': 'mentions'})
