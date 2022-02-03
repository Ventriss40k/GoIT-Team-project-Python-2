from django import conf
from django.utils.decorators import classonlymethod
from django.views.generic import View, TemplateView
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

from django.http import HttpResponseRedirect, HttpResponse
from dotenv import load_dotenv
import asyncio
import aiohttp
import os
from .models import Contacts, Notes, NoteTags, Files, FileTypes
from .forms import PositionForm


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
                first_name=first_name_input)

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


# visible_projects = project.expenses.filter(dateExpense__gte=dates[0]).filter(
#     dateExpense__lte=dates[1]) if dates else project.expenses.all()


# def find_birthday(colleagues):
#     next_week = []
#     current_time = datetime.datetime.now().date()
#     start_of_period = current_time - \
#         datetime.timedelta(days=current_time.weekday() - 5)
#     end_of_period = start_of_period + datetime.timedelta(days=6)
#     for item in colleagues:
#         for i, val in item.items():
#             if end_of_period.strftime('%m-%d') >= val.strftime('%m-%d') >= start_of_period.strftime('%m-%d'):
#                 next_week.append(item)
#     return next_week


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


class NotesView(TemplateView):
    template_name = "assistant/notes.html"


class NewsView(View):
    template_name = "assistant/news.html"

    @classonlymethod
    def as_view(self, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    @classmethod
    async def fetch_news(cls):
        url = f'https://newsapi.org/v2/everything?q=finance&apiKey={API_KEY}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                result = await response.json()
                return result['articles']

    async def get(self, request, *args, **kwargs):
        context = {
            "data": await self.fetch_news()
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "assistant/about_us.html"


class FilesView(TemplateView):
    template_name = "assistant/files.html"
