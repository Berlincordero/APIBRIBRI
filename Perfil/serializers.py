# perfiles_api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
    """
    Serializa los campos del modelo Perfil.
    """
    class Meta:
        model = Perfil
        fields = [
            'id',
            'foto_perfil',
            'banner',
            'fecha_nacimiento',
            'biografia',
            'direccion',
            'nombre_empresa',
            'anio_fundacion',
            'actividad_economica',
            'preferencias_agropecuarias',
            'preferencias_comerciales',
            'youtube_link',
            'instagram_link',
            'whatsapp_link',
            'followers',  # si quieres exponer o permitir actualizar seguidores
        ]
        # Si solo deseas exponer seguidores, pero no que se actualicen directamente,
        # podrías excluirlos de 'fields' o poner read_only=True.

class UserSerializer(serializers.ModelSerializer):
    """
    Si quieres exponer datos básicos del User junto al Perfil.
    """
    perfil = PerfilSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'perfil']

    def update(self, instance, validated_data):
        # Maneja el perfil anidado
        perfil_data = validated_data.pop('perfil', None)
        # Actualiza campos del User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualiza perfil
        if perfil_data:
            perfil_instance = instance.perfil
            for attr, value in perfil_data.items():
                setattr(perfil_instance, attr, value)
            perfil_instance.save()

        return instance
