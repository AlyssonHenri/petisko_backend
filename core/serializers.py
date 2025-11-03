
from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "cpf", "state", "city", "img"]

