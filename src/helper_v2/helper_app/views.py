from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.utils import timezone, dateformat
from dotenv import load_dotenv
import requests
import os
from .models import Contacts, Note, Files, FileTypes


load_dotenv()
API_KEY = os.getenv("API_KEY")


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, **kwargs)


class HomeView(TemplateView):
    template_name = "assistant/home.html"


class ContactsView(LoginRequiredMixin, ListView):
    template_name = "assistant/contacts_list.html"
    model = Contacts
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = context['contacts'].filter(
            user=self.request.user)
        context['count'] = context['contacts'].count()

        context['b_days'] = context['contacts'].filter(
            b_day__month=timezone.datetime.now().month)

        first_name_input = self.request.GET.get('search-by-name') or ''
        if first_name_input:
            context['contacts'] = context['contacts'].filter(
                first_name__istartswith=first_name_input)

        last_name_input = self.request.GET.get('search-by-last-name') or ''
        if last_name_input:
            context['contacts'] = context['contacts'].filter(
                last_name=last_name_input)

        phone_input = self.request.GET.get('search-by-phone-number') or ''
        if phone_input:
            context['contacts'] = context['contacts'].filter(
                phone_number=phone_input)

        email_input = self.request.GET.get('search-by-email') or ''
        if email_input:
            context['contacts'] = context['contacts'].filter(
                email=email_input)
        return context


class AddContact(LoginRequiredMixin, CreateView):
    model = Contacts
    fields = ['first_name', 'last_name',
              'phone_number', 'email', 'b_day', 'is_favorite']
    success_url = reverse_lazy('contacts_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddContact, self).form_valid(form)


class UpdateContact(LoginRequiredMixin, UpdateView):
    model = Contacts
    fields = ['first_name', 'last_name',
              'phone_number', 'email', 'b_day', 'is_favorite']
    success_url = reverse_lazy('contacts_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateContact, self).form_valid(form)


class DeleteContact(LoginRequiredMixin, DeleteView):
    model = Contacts
    context_object_name = 'contacts'
    success_url = reverse_lazy('contacts_list')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = "notes"
    template_name = 'assistant/notes_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        
        search_input_title = self.request.GET.get('search_title') or ''
        if search_input_title:
            context['notes'] = context['notes'].filter(
                title__istartswith=search_input_title)

        context['search_input_title'] = search_input_title 
        return context  



class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note 
    context_object_name = "note"
    template_name = 'assistant/note.html'




class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'description', 'tagsString']
    success_url = reverse_lazy('notes')
    template_name = 'assistant/note_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NoteCreateView, self).form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['title', 'description', 'tagsString']
    success_url = reverse_lazy('notes')
    template_name = 'assistant/note_form.html'


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    context_object_name = "note"
    template_name = 'assistant/note_confirm_delete.html'
    success_url = reverse_lazy('notes')
    

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)



class NewsView(ListView):
    template_name = "assistant/news.html"

    @classmethod
    def fetch_news(cls):
        url = f'https://newsapi.org/v2/everything?q=finance&apiKey={API_KEY}'
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        result = response.json()
        return result['articles']

    def get(self, request, *args, **kwargs):
        context = {
            "data": self.fetch_news()
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "assistant/about_us.html"


class FilesView(TemplateView):
    template_name = "assistant/files.html"
