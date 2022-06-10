from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.PostAPIView.as_view()),
    path('posts/<str:post_id>', views.PostDetailAPIView.as_view()),
    path('me/posts', views.UserPostListView.as_view()),
    path('posts/<str:post_id>/comments',views.CommentAPIView.as_view()),
    path('posts/<str:post_id>/comments/<str:comment_id>',views.CommentAPIView.as_view()),
]