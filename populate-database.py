import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','miniproject.settings')

import django
django.setup()

from blog.models import Post, Comment
from django.contrib.auth import get_user_model

import random

User = get_user_model()

def create_users(num):
    for x in range(1,num+1):
        User1 = User.objects.create_user('User'+str(x),password='admin123')
        User1.email = 'User' + str(x) +"@example.com"
        User1.name = 'User' + str(x)
        User1.username = 'User' + str(x)
        User1.save()
        create_post(2,User1,x)

def create_post(num, User, start):
    for x in range(start,start+num+1):
        random_number = str(random.randint(1,1000))
        post = Post(title = "Sample title"+random_number,content = "Sample content"+random_number, User_Id = User)
        post.save()


def create_comments_post():
    post_list = list(Post.objects.all())
    for x in post_list:
        create_comment(2,x)

def create_comment(num, post):
    user_list = list(User.objects.all())
    
    for x in range(1,num+1):
        random_number = str(random.randint(1,1000))
        user = user_list[random.randint(1,len(user_list)-1)]
        comment = Comment(content = "Comment content" + random_number, Post_Id = post, User_Id = user)
        comment.save()

def populate():
    # data is a list of lists
    create_users(5)
    create_comments_post()

if __name__ == "__main__":
    populate()