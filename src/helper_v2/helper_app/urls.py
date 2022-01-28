from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('contacts', views.ContactsView.as_view()),
    path('notes', views.NotesView.as_view()),
    path('news', views.NewsView.as_view()),
    path('aboutUs', views.AboutView.as_view()),
]