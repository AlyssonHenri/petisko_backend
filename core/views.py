from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.models import User, Pet
from core.serializers import UserSerializer, UserPublicSerializer, PetSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(request.user.id) == kwargs['pk']:
            serializer = UserSerializer(instance)
        else:
            serializer = UserPublicSerializer(instance)
        return Response(serializer.data)

    #put    
    def update(self, request, *args, **kwargs): 
        if str(request.user.id) == kwargs['pk']:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"detail": "Not authorized."}, status=403)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='pets')
    def pets(self, request, pk=None):
        pets = Pet.objects.filter(tutor=pk)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['post'], url_path='add')

    def create_pet(self, request, pk=None):

        data = request.data.copy()
        data['tutor'] = pk  # associa o pet ao usuário da URL

        serializer = PetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['get'], url_path='pets/(?P<pet_id>[^/.]+)')
    def pet_detail(self, request, pk=None, pet_id=None):
        try:
            pet = Pet.objects.get(id=pet_id, tutor_id=pk)
        except Pet.DoesNotExist:
            return Response({'detail': 'Pet não encontrado'}, status=404)

        serializer = PetSerializer(pet)
        return Response(serializer.data)

class PetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer