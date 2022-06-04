from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from .serializers import UserSerializer

@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        serializer.validated_data['password'] = make_password(password)
        serializer.save()
        

        response_with_message = {
            "message":"Signup successful!",
            "data" : serializer.data
        }

        return Response(response_with_message, status=status.HTTP_201_CREATED)


    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

