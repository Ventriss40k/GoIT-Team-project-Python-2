from datetime import datetime
from multiprocessing import context
from django import conf
from django.utils.decorators import classonlymethod
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction

from django.http import HttpResponseRedirect, HttpResponse
from dotenv import load_dotenv
import asyncio
import aiohttp
import os

from .models import Contacts, Notes, NoteTags, Files, FileTypes

from google.oauth2 import service_account # for authorization
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload # for downloading| uploading files
from googleapiclient.discovery import build # allows creating a resorce for easy acess to API
import io
from django.core.files.storage import FileSystemStorage
from helper_v2.settings import MEDIA_ROOT 
from django.contrib.auth.models import User

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
    # AUTHORIZATION GOOGLE API
    SCOPES = ['https://www.googleapis.com/auth/drive'] # is a list of features for this exact service. can get one from Google drive docs
    SERVICE_ACCOUNT_FILE = r'C:\Users\1\Downloads\goit-python-2-3532a63ebc79.json' # This is path to json file vith keys from service account
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES) # credentials is user data, to grant him permission of doing smth
    service = build('drive', 'v3', credentials=credentials) # creating a service, which use 3rd version REST API Google Drive, using acount (credentials)

    #GET LIST OF ALL FILES 
    results = service.files().list(pageSize=10,
                                fields="nextPageToken, files(id, name, mimeType)").execute()
    nextPageToken = results.get('nextPageToken')
    while nextPageToken:
            nextPage = service.files().list(pageSize=10,
                                            fields="nextPageToken, files(id, name, mimeType, parents)",
                                            pageToken=nextPageToken).execute()
            nextPageToken = nextPage.get('nextPageToken')
            results['files'] = results['files'] + nextPage['files']
    list_of_files = results['files']
    
    template_name = "assistant/files.html"

    def get_context_data(self, list_of_files= list_of_files, **kwargs):
        context = super(FilesView, self).get_context_data(**kwargs)
        context['list_of_files'] = list_of_files
        return context
    def post(self, request, service= service, *args, **kwargs ):
        # DELETE
        if request.POST["operation"] == 'delete':
            service.files().delete(fileId= request.POST['file_id']).execute()

            return HttpResponse("deleted file") 
        # DOWNLOAD
        elif request.POST["operation"] == 'download':
            file_id = request.POST['file_id']
            googleapirequest = service.files().get_media(fileId=file_id)
            filepath = f'C:\\Users\\1\\Desktop\\googleapi-files\\downloaded\\'+  request.POST['file_name'] # warning
            fh = io.FileIO(filepath, 'wb')
            downloader = MediaIoBaseDownload(fh, googleapirequest)
            done = False
            while done is False:
                done = downloader.next_chunk()
            return HttpResponse("downloaded file")
            # UPLOAD
        elif request.POST["operation"] == 'upload':
            uploaded_file = request.FILES['file']
            filename= uploaded_file.name
            fileextension = filename.split('.')[1].lower()
            fs = FileSystemStorage()
            fs.save(filename,uploaded_file)
            filepath = os.path.join(MEDIA_ROOT,filename) # creating filepath to local saved file

            folder_id = '1B-2uKukREH15gK5sHqW0Iif5lT_zRqiq' # folder id, can be acuired from url or from "list" method 
            file_metadata = {
                            'name': filename,
                            'parents': [folder_id]
                        }
            media = MediaFileUpload(filepath, resumable=True)
            googlefile = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            # ADD RECORD TO DATABASE
            # record = Files.objects.create(user= User, file_name= filename,file_type= fileextension, file_date= datetime.now(),file_path = googlefile  ) # CHANGE USER LATER









            return HttpResponse("upload file")


        else:
            return HttpResponse('invalid operation')

        
    


