from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializers, UserSerializers
from rest_framework import status
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import datetime, timedelta
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


def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    print("this is protocol",protocol)
    host = request.get_host()
    return f"{protocol}://{host}"

@api_view(['POST'])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    print('this is host ',host)
    link = f"http://127.0.0.1:8000/api/reset_password/{token}"
    body = f"You can reset your Password Here {link}"
    send_mail(
        "Password Reset From E-Market",
        body,
        'emarket@staff.com',
        [data['email']]
    )

    return Response({'details': f'Password reset sent to {data["email"]}'})


@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'Error': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
         return Response({'Error': 'password Not Equal'}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])

    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()


    return Response({'details': 'Password Changed Succesfully!!'})