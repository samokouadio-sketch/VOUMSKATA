from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'statut', 'date_publication')
    list_filter = ('statut',)
    search_fields = ('titre', 'extrait', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
