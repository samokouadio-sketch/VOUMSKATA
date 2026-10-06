from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, StatutArticle


def index(request):
    """Liste des articles du blog/actualités."""
    articles_list = Article.objects.filter(statut=StatutArticle.PUBLIE)
    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'active_nav': 'actualites',
        'page_obj': page_obj,
        'articles': page_obj.object_list,
    }
    return render(request, 'actualites.html', context)


def detail(request, slug):
    """Détail d'un article."""
    article = get_object_or_404(Article, slug=slug, statut=StatutArticle.PUBLIE)
    articles_recents = Article.objects.filter(statut=StatutArticle.PUBLIE).exclude(id=article.id)[:3]

    context = {
        'active_nav': 'actualites',
        'article': article,
        'articles_recents': articles_recents,
    }
    return render(request, 'actualite-detail.html', context)
