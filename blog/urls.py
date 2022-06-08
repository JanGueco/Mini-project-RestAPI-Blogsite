from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.PostAPIView.as_view()),
    path('posts/<str:post_id>', views.PostDetailAPIView.as_view())
]