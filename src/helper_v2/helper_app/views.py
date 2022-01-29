from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from .models import Contacts, Notes, NoteTags, Files, FileTypes
from django.urls import reverse_lazy
# import json

# from .forms import ExpenseForm, FilterForm

from django.db import transaction


class HomeView(TemplateView):
    template_name = "assistant/home.html"


class ContactsView(ListView):
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


class AddContact(CreateView):
    model = Contacts
    fields = ['first_name', 'last_name',
              'phone_number', 'email', 'b_day', 'is_favorite']
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        # form.instance.user = self.request.user
        return super(AddContacts, self).form_valid(form)


class NotesView(TemplateView):
    template_name = "assistant/notes.html"


class NewsView(TemplateView):
    template_name = "assistant/news.html"


class AboutView(TemplateView):
    template_name = "assistant/about_us.html"
