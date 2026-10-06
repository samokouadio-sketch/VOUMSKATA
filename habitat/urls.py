from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('vitrine.urls', 'vitrine'), namespace='vitrine')),
    path('conception/', include(('conception.urls', 'conception'), namespace='conception')),
    path('realisations/', include(('realisations.urls', 'realisations'), namespace='realisations')),
    path('gestion/', include(('gestion.urls', 'gestion'), namespace='gestion')),
    path('import-export/', include(('materiaux.urls', 'materiaux'), namespace='materiaux')),
    path('actualites/', include(('actualites.urls', 'actualites'), namespace='actualites')),
    path('contact/', include(('contact.urls', 'contact'), namespace='contact')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
