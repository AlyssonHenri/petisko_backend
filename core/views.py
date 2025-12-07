from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import User, Pet, Vacina, Match
from core.serializers import UserSerializer, UserPublicSerializer, PetSerializer, MatchSerializer, UnmatchSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q 
import json

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

        vacinas_json = data.pop('vacinas', '[]')

        serializer = PetSerializer(data=data)
        if serializer.is_valid():
          pet = serializer.save()
          try:
                # Parse do JSON (pode vir como lista ou string)
                if isinstance(vacinas_json, list):
                    vacinas_nomes = json.loads(vacinas_json[0])
                else:
                    vacinas_nomes = json.loads(vacinas_json)
                
                for v in vacinas_nomes:
                    nome_vacina = v.get("nome")
                    if not nome_vacina:
                        continue
                    vacina, created = Vacina.objects.get_or_create(nome=nome_vacina)
                    pet.vacinas.add(vacina)
                    
          except Exception as e:
                print(f"⚠️ Erro ao processar vacinas: {e}")
            
          return Response(PetSerializer(pet).data, status=201)

        return Response(serializer.errors, status=400)
    

    @action(detail=True, methods=['get', 'patch', 'delete'], url_path='pets/(?P<pet_id>[^/.]+)')
    def pet_detail(self, request, pk=None, pet_id=None):
        try:
            pet = Pet.objects.get(id=pet_id, tutor_id=pk)
        except Pet.DoesNotExist:
            return Response({'detail': 'Pet não encontrado'}, status=404)
        
        if request.method == 'GET':
            serializer = PetSerializer(pet)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            print('oi')
            data = request.data.copy()
            vacinas_json = data.pop('vacinas', None)
            
            serializer = PetSerializer(pet, data=data, partial=True)
            
            if serializer.is_valid():
                pet = serializer.save()
                
                # Só processa vacinas se foram enviadas
                if vacinas_json is not None:
                    try:
                        # Parse do JSON string
                        if isinstance(vacinas_json, str):
                            vacinas_nomes = json.loads(vacinas_json)
                        elif isinstance(vacinas_json, list) and len(vacinas_json) > 0:
                            # Se vier como lista com string JSON dentro
                            vacinas_nomes = json.loads(vacinas_json[0]) if isinstance(vacinas_json[0], str) else vacinas_json
                        else:
                            vacinas_nomes = vacinas_json


                        pet.vacinas.clear()
                        
                        for v in vacinas_nomes:
                            if isinstance(v, dict):
                                nome_vacina = v.get("nome")
                            else:
                                nome_vacina = str(v)
                                
                            if not nome_vacina:
                                continue
                            
                            vacina, created = Vacina.objects.get_or_create(nome=nome_vacina)
                            pet.vacinas.add(vacina)
                            
                    except Exception as e:
                        print(f"⚠️ Erro ao processar vacinas: {e}")
                        import traceback
                        traceback.print_exc()
                
                return Response(PetSerializer(pet).data)
            return Response(serializer.errors, status=400)

        elif request.method == 'DELETE':
            pet.delete()
            return Response(status=204)


    @action(detail=True, methods=['get', 'post'], url_path='pets/(?P<pet_id>[^/.]+)/matches')
    def match_pets(self, request, pk=None, pet_id=None):
        try:
            pet = Pet.objects.get(id=pet_id, tutor_id=pk)
        except Pet.DoesNotExist:
            return Response({'detail': 'Pet não encontrado'}, status=404)
        
        if request.method == 'GET':
            # Pega todos os matches (iniciados e recebidos)
            matches = Match.objects.filter(
                Q(petPrincipal=pet) | Q(petMatch=pet)
            )
            serializer = MatchSerializer(matches, many=True) 
            return Response(serializer.data)
            
        elif request.method == 'POST':
            data = request.data.copy()
            data['petPrincipal'] = pet_id  

            serializer = MatchSerializer(data=data)
            if serializer.is_valid():
                match = serializer.save()
                return Response(MatchSerializer(match).data, status=201)

            return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get', 'post'], url_path='pets/(?P<pet_id>[^/.]+)/unmatches')
    def unmatch_pets(self, request, pk=None, pet_id=None):
        try:
            pet = Pet.objects.get(id=pet_id, tutor_id=pk)
        except Pet.DoesNotExist:
            return Response({'detail': 'Pet não encontrado'}, status=404)
        
        if request.method == 'GET':
            matches = Match.objects.filter(
                Q(petPrincipal=pet) | Q(petBlock=pet)
            )
            serializer = MatchSerializer(matches, many=True) 
            return Response(serializer.data)
            
        elif request.method == 'POST':
            data = request.data.copy()
            data['petPrincipal'] = pet_id  

            serializer = UnmatchSerializer(data=data)
            if serializer.is_valid():
                match = serializer.save()
                return Response(UnmatchSerializer(match).data, status=201)

            return Response(serializer.errors, status=400)
    

class PetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
                    
class MatchView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

  