# perfiles_api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .models import Perfil
from .serializers import PerfilSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



class PerfilViewSet(viewsets.ModelViewSet):
    """
    Permite listar, crear, ver, actualizar, eliminar perfiles.
    """
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]
    # Para manejar subida de archivos (foto_perfil), config:
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Si deseas que al crear un perfil se asocie al usuario logueado
        serializer.save(user=self.request.user)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def mi_perfil_view(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        ser = PerfilSerializer(perfil)
        return Response(ser.data)
    elif request.method in ['PUT', 'PATCH']:
        ser = PerfilSerializer(perfil, data=request.data, partial=(request.method=='PATCH'))
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors, status=400)

