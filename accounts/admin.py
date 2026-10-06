from django.contrib import admin
from .models import Profil


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'role', 'telephone')
    list_filter = ('role',)
    search_fields = ('utilisateur__username', 'utilisateur__first_name', 'utilisateur__last_name')
