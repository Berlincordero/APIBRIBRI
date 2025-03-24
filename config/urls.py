# config/urls.py (archivo de configuración de URLs principal del proyecto)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Usuarios/', include('Usuarios.urls')),

]
