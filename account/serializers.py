from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

        extra_kwargs = {
            'first_name': {'required': True}, 
            'last_name': {'required': True},
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'min_length': 8}
        }

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
