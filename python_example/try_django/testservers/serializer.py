from rest_framework import serializers
from users.serializer import UserSerializer
from .models import *

class TestServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestServers
        fields = '__all__'
