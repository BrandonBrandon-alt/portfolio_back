# Portafolio/urls.py

from django.contrib import admin
from django.urls import path, include # <-- ¿Está 'include' importado?

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # <-- ¿Está esta línea escrita correctamente?
]