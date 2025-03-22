# perfiles_api/models.py (o Perfiles/models.py si lo prefieres)
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    nombre_empresa = models.CharField(max_length=255, blank=True, null=True)
    anio_fundacion = models.DateField(blank=True, null=True)
    actividad_economica = models.CharField(max_length=255, blank=True, null=True)
    preferencias_agropecuarias = models.CharField(max_length=255, blank=True, null=True)
    preferencias_comerciales = models.CharField(max_length=255, blank=True, null=True)
    youtube_link = models.URLField(max_length=500, blank=True, null=True)
    instagram_link = models.URLField(max_length=500, blank=True, null=True)
    whatsapp_link = models.URLField(max_length=500, blank=True, null=True)
    # Campo ManyToMany para seguidores:
    followers = models.ManyToManyField(User, related_name='siguiendo', blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    @property
    def cantidad_suscriptores(self):
        return self.followers.count()

    @property
    def cantidad_foros_publicados(self):
        """
        Ejemplo: si existe un modelo Foro con una ForeignKey:
            class Foro(models.Model):
                autor = models.ForeignKey(User, related_name='foros', ...)
        """
        return self.user.foros.count()
