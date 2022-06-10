from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from knox.auth import TokenAuthentication


from . import functions
from . import serializers
from .models import Post, Comment


# Create your views here.

#Custom Pagination Class
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'message': "Success!",
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        }, status.HTTP_200_OK)

#ErrorResponse
def ErrorResponse(message, status):
    return Response({"Error": message}, status)






class PostAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PostSerializer 

    def get(self, request, format = None): #GetAll
        posts = Post.objects.all().order_by('-updated')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(posts,request)
        serializer = self.serializer_class(instance=result_page, many = True)

        if posts:
            
            return paginator.get_paginated_response(serializer.data)
        
        

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
            return Response(response_with_message, status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors)
    

class PostDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PostDetailSerializer


    def get(self, reqeust, post_id): #Get single post
        
        post = Post.objects.get(id = post_id)
        serializer = self.serializer_class(instance = post)

        if post:
            response_with_message = {
                "message":"Success!",
                "data": serializer.data
            }
            return Response(response_with_message,status.HTTP_200_OK)
        




    def put(self, request, post_id): #Update post
        data = request.data

        try:
            post = Post.objects.get(id = post_id)
        except:
            return ErrorResponse("Post does not exist", status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance = post, data = data)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        if post.User_Id != user:
            #change to proper exceptions later
            return ErrorResponse("User does not own the post", status.HTTP_401_UNAUTHORIZED)
        
        

        if serializer.is_valid():
            serializer.save()
        
            response_with_message = {
            "message":"Post updated!",
            "data" : serializer.data
            }
            return Response(response_with_message, status.HTTP_200_OK)
    
    def delete(self,request, post_id): #Delete post
        post = Post.objects.get(id = post_id)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        if post.User_Id != user:
            #change to proper exceptions later
            return ErrorResponse("User does not own the post", status.HTTP_401_UNAUTHORIZED)
        
        elif post.User_Id == user:
            post.delete()
            return Response({"message":"Post deleted!"}, status.HTTP_200_OK)

class UserPostListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostSerializer

    def get(self, request): #Get user posts
        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        try:
            posts = Post.objects.filter(User_Id = user).order_by('-updated')
        
        except:
            return ErrorResponse("User does not have any posts", status.HTTP_404_NOT_FOUND)
        
        pagintor = CustomPagination()
        result_page = pagintor.paginate_queryset(posts,request)
        serializer = self.serializer_class(instance = result_page, many = True)
        
        return pagintor.get_paginated_response(serializer.data)


class CommentAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.CommentSerializer
    

    def get(self,request,post_id): #Get comments from post
        
        try:
            post = Post.objects.get(id=post_id)
        except:
            return ErrorResponse("Post does not exist", status.HTTP_404_NOT_FOUND)

        
        comments = Comment.objects.filter(Post_Id = post).order_by('-updated')
        if not comments:
            return ErrorResponse("No comments on post", status.HTTP_404_NOT_FOUND)

        if post and comments:
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(comments,request)
            serializer = self.serializer_class(instance=result_page,many=True)

            return paginator.get_paginated_response(serializer.data)
        
        



    def post(self,request,post_id): #Create comment
        data = request.data
        serializer = self.serializer_class(data = data)

        try:
            post = Post.objects.get(id = post_id)
        except:
            return ErrorResponse("Post does not exist", status.HTTP_404_NOT_FOUND)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        
        

        if serializer.is_valid():
            serializer.validated_data["User_Id"] = user
            serializer.validated_data["Post_Id"] = post
            serializer.save()

            response_with_message={
                "message":"Comment created!",
                "data": serializer.data
            }
            return Response(response_with_message, status.HTTP_201_CREATED)
        
        return Response(serializer.errors)
    
    def delete(self, request, post_id, comment_id): #Delete comment
        try:
            post = Post.objects.get(id = post_id)
        except:
            return ErrorResponse("Post does not exist", status.HTTP_404_NOT_FOUND)
        
        try:
            comment = Comment.objects.get(id = comment_id)
        except:
            return ErrorResponse("Comment does not exist", status.HTTP_404_NOT_FOUND)

        #get user via token
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        user = functions.get_user_from_token(token)

        if user == post.User_Id or user == comment.User_Id:
            comment.delete()
            return Response({"message":"Comment deleted!"}, status.HTTP_200_OK)
        
        else:
            return ErrorResponse("Invalid permissions", status.HTTP_401_UNAUTHORIZED)
    



