from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from knox.models import AuthToken


from django.contrib.auth.hashers import make_password


from .serializers import UserSerializer, LoginSerializer


@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        serializer.validated_data['password'] = make_password(password)
        serializer.validated_data['username'] = serializer.validated_data.get('name')
        serializer.save()
        

        response_with_message = {
            "message":"Signup successful!",
            "data" : serializer.data
        }

        return Response(response_with_message, status=status.HTTP_201_CREATED)


    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login_user(request):
    
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    

    return Response({"message": "Login successful!",
    "data":{"token": AuthToken.objects.create(user)[1]}
    })




