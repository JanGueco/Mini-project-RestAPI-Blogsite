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
    
    