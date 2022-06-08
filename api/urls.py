from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup', views.add_user),
    path('auth/login', views.login_user),
]