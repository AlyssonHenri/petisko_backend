from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from core.models import User
from core.serializers import UserSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @permission_classes([IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)