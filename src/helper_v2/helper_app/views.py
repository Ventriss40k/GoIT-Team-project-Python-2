from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
# import json
# from .models import Project, Category, Expense
# from .forms import ExpenseForm, FilterForm

def home(request):
    return render(request, 'assistant/home.html')


def services(request):
    return render(request, 'assistant/services.html')


def news(request):
    return render(request, 'assistant/news.html')


def contacts(request):
    return render(request, 'assistant/contacts.html')