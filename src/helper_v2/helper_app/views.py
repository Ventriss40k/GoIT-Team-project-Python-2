from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
# import json
# from .models import Project, Category, Expense
# from .forms import ExpenseForm, FilterForm



class HomeView(TemplateView):
    template_name = "assistant/home.html"  


class ContactsView(TemplateView):
    template_name = "assistant/contacts.html"    
    

class NotesView(TemplateView):
    template_name = "assistant/notes.html" 


class NewsView(TemplateView):
    template_name = "assistant/news.html" 


class AboutView(TemplateView):
    template_name = "assistant/about_us.html"

  
