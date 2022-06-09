from ast import Pass, Raise
from email import message
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import CONSTANTS

from . import functions
from . import serializers
from .exceptions import NoPermission
from .models import Post, Comment
# Create your views here.

class PostAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PostSerializer 

    def get(self, request, format = None): #GetAll
        posts = Post.objects.all()
        serializer = self.serializer_class(instance=posts, many = True)

        if posts:
            response_with_message = {
                "message":"Success!",
                "data": serializer.data
            }
            return Response(response_with_message)
        
        

    def post(self, request, format=None): #Create
        data = request.data
        serializer = self.serializer_class(data = data)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)
        
        if serializer.is_valid():
            serializer.validated_data["User_Id"] = user
            serializer.save()
            
            response_with_message = {
            "message":"Post created!",
            "data" : serializer.data
            }
            return Response(response_with_message)
        
        return Response(data=serializer.errors)
    

class PostDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PostDetailSerializer


    def get(self, reqeust, post_id):
        
        post = Post.objects.get(id = post_id)
        serializer = self.serializer_class(instance = post)

        if post:
            response_with_message = {
                "message":"Success!",
                "data": serializer.data
            }
            return Response(response_with_message)
        




    def put(self, request, post_id):
        data = request.data

        try:
            post = Post.objects.get(id = post_id)
        except:
            return Response({"Error":"Post does not exist"})

        serializer = self.serializer_class(instance = post, data = data)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        if post.User_Id != user:
            #change to proper exceptions later
            return Response({"Invalid Permissions":"User does not own the post"})
        
        

        if serializer.is_valid():
            serializer.save()
        
            response_with_message = {
            "message":"Post updated!",
            "data" : serializer.data
            }
            return Response(response_with_message)
    
    def delete(self,request, post_id):
        post = Post.objects.get(id = post_id)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        if post.User_Id != user:
            #change to proper exceptions later
            return Response({"Invalid Permissions":"User does not own the post"})
        
        elif post.User_Id == user:
            post.delete()
            return Response({"message":"Post deleted!"})

class UserPostListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostSerializer

    def get(self, request):
        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        try:
            posts = Post.objects.filter(User_Id = user)
        
        except:
            return Response({"Error":"User does not have posts"})
        
        serializer = self.serializer_class(instance = posts, many = True)
        response_with_message = {
            "message":"Success!",
            "data": serializer.data
        }
        return Response(response_with_message)
