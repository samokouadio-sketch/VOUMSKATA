from django.contrib import admin
from .models import MessageContact


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'sujet', 'email', 'traite', 'traite_par', 'date_creation')
    list_filter = ('sujet', 'traite')
    search_fields = ('nom_complet', 'telephone', 'email', 'message')
    date_hierarchy = 'date_creation'
