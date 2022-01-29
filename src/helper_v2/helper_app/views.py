from django.shortcuts import render, get_object_or_404


from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from .models import Contacts, Notes, NoteTags, Files, FileTypes
from django.urls import reverse_lazy
# import json

# from .forms import ExpenseForm, FilterForm


class CustomLoginView(LoginView):
    template_name = 'helper_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'helper_app/register.html'
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
    template_name = "assistant/contacts.html"
    model = Contacts
    context_object_name = 'contacts'

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        context['contacts'] = context['contacts']
        context['count'] = context['contacts'].count()

        first_name_input = self.request.GET.get('serch-by-name') or ''
        if first_name_input:
            context['contacts'] = context['contacts'].filter(
                first_name=first_name_input)

        last_name_input = self.request.GET.get('serch-by-last-name') or ''
        if last_name_input:
            context['contacts'] = context['contacts'].filter(
                last_name=last_name_input)

        phone_input = self.request.GET.get('serch-by-phone-number') or ''
        if phone_input:
            context['contacts'] = context['contacts'].filter(
                phone_number=phone_input)

        email_input = self.request.GET.get('serch-by-email') or ''
        if email_input:
            context['contacts'] = context['contacts'].filter(
                email=email_input)


class AddContact(LoginRequiredMixin, CreateView):
    model = Contacts
    fields = ['first_name', 'last_name',
              'phone_number', 'email', 'b_day', 'is_favorite']
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        # form.instance.user = self.request.user
        return super(AddContacts, self).form_valid(form)


class UpdateContact(LoginRequiredMixin, UpdateView):
    model = Contacts
    fields = ['first_name', 'last_name',
              'phone_number', 'email', 'b_day', 'is_favorite']
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateContact, self).form_valid(form)


class DeleteContact(LoginRequiredMixin, DeleteView):
    model = Contacts
    context_object_name = 'contacts'
    success_url = reverse_lazy('contacts')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class NotesView(TemplateView):
    template_name = "assistant/notes.html"


class NewsView(TemplateView):
    template_name = "assistant/news.html"


class AboutView(TemplateView):
    template_name = "assistant/about_us.html"
