from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.models import User
from core.serializers import UserSerializer, UserPublicSerializer

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

    #patch
    def partial_update(self, request, *args, **kwargs):
        if str(request.user.id) == kwargs['pk']:
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({"detail": "Not authorized."}, status=403)