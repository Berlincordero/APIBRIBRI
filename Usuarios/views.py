# api/views.py
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer
from Usuarios.models import Profile

# 4.1 Ejemplo: ViewSet para listar y actualizar usuarios
class UserViewSet(viewsets.ModelViewSet):
    """
    Permite CRUD de User + Profile anidado.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Si deseas que solo usuarios autenticados puedan acceder
    # permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Sobrescribimos update si queremos manejar también el profile anidado.
        """
        partial = kwargs.pop('partial', False)  # Permite PATCH
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4.2 Endpoint personalizado para registrar usuarios (en lugar de un formulario)
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir que usuarios no autenticados se registren
def register_api(request):
    """
    Espera un JSON con campos: first_name, last_name, email, password,
    birth_date (YYYY-MM-DD), gender, etc.
    """
    data = request.data
    required_fields = ['first_name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return Response({'error': f'El campo {field} es requerido.'}, status=400)

    # Validar si email ya existe
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'El correo ya está registrado.'}, status=400)

    # Crear username automático
    base_username = f"{data['first_name'].lower()}.{data['last_name'].lower()}"
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    user = User.objects.create_user(
        username=username,
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    user.save()

    # Actualizar perfil con los datos que vengan
    profile = user.profile  # Gracias a la señal en Profile
    # birth_date, gender, etc.
    if 'birth_date' in data:
        profile.birth_date = data['birth_date']  # Asegúrate que venga con formato YYYY-MM-DD
    if 'gender' in data:
        profile.gender = data['gender']
    profile.save()

    # Devuelves info del usuario creado
    return Response(UserSerializer(user).data, status=201)
# api/views.py
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import Profile

# ViewSet CRUD de usuarios (requiere autenticación)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite registro sin loguearse
def register_api(request):
    """
    JSON de ejemplo:
    {
      "first_name": "Pedro",
      "last_name": "Perez",
      "email": "perez@gmail.com",
      "password": "12345678",
      "birth_date": "1980-01-01",
      "gender": "male"
    }
    """
    data = request.data
    required_fields = ['first_name', 'last_name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return Response({"error": f"Falta {field}"}, status=400)

    if User.objects.filter(email=data['email']).exists():
        return Response({"error": "El correo ya está registrado."}, status=400)

    # Generar username único
    base_username = f"{data['first_name'].lower()}.{data['last_name'].lower()}"
    username = base_username
    count = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{count}"
        count += 1

    user = User.objects.create_user(
        username=username,
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    user.save()

    # Actualizar perfil
    if 'birth_date' in data:
        user.profile.birth_date = data['birth_date']
    if 'gender' in data:
        user.profile.gender = data['gender']
    user.profile.save()

    # Retornar info serializada
    serializer = UserSerializer(user)
    return Response(serializer.data, status=201)
