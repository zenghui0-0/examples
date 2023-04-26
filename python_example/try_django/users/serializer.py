from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        # fields = ["id", "username", "date_joined", "is_active"]
        ordering = ['id']

