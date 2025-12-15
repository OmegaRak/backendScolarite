from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/', include('auth_users.urls')),

    # Inscription / Concours
    path('api/inscription/', include('inscription.urls')),

    # Réinscription
    path('api/reinscription/', include('reinscription.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
