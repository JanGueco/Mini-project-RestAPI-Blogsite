from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup', views.addUser),
    path('auth/login', views.loginUser)
]