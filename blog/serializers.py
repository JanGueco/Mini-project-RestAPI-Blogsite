from rest_framework import serializers

from .models import Post, Comment



class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Post
        fields = ["id","title", "content","author"]
        
    def get_author(self,obj):
        name = obj.User_Id.name
        return name

class PostDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Post
        fields = ["id","title", "content","author"]
        
    def get_author(self,obj):
        name = obj.User_Id.name
        return name
    
class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField
    author = serializers.SerializerMethodField('get_author')
    post_id = serializers.SerializerMethodField('get_postid')

    class Meta:
        model = Comment
        fields = ["id", "post_id", "content", "author"]


    def get_author(self,obj):
        name = obj.User_Id.name
        return name
    
    def get_postid(self,obj):
        id = obj.Post_Id.id
        return id
    