from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializers, UserSerializers
from rest_framework import status
# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializers(data=data)

    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'],
                username = data['username'], 
                password = make_password(data['password'])
            )
            return Response({"Details": 'User Created Successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({"Error": 'User Already Exist'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializers(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    print(f"First Name: {user.first_name}, Last Name: {user.last_name}, Email: {user.email}")
    data = request.data

    user.first_name = data['first_name']
    
    user.last_name = data['last_name']
    user.email = data['email']

    if data['password'] != "":
        user.password =  make_password(data['password'])

    user.save()
    serializer = UserSerializers(user,many=False)
    return Response(serializer.data)