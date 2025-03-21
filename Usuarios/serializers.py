# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['birth_date', 'gender']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializa al usuario con los campos básicos,
    e incluye el Profile anidado.
    """
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        # Actualiza campos de User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Actualiza profile
        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        return instance
