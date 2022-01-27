from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services', views.services, name='services'),
    path('news', views.news, name='news'),
    path('contacts', views.contacts, name='contacts'),
]