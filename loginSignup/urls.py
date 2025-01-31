from django.contrib import admin
from django.urls import path, include

from loginSignup import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/login', views.login, name='login'),
    path('signup/index', views.index, name='index'),
    path('signup/signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
