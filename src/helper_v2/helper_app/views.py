from ast import UAdd
from django import conf
from django.utils.decorators import classonlymethod
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse
from dotenv import load_dotenv
from newsapi import NewsApiClient
import asyncio
import aiohttp
import os


load_dotenv()
API_KEY = os.getenv("API_KEY")



class HomeView(TemplateView):
    template_name = "assistant/home.html"  


class ContactsView(TemplateView):
    template_name = "assistant/contacts.html"    
    

class NotesView(TemplateView):
    template_name = "assistant/notes.html" 


class NewsView(View):
    
    template_name = "assistant/news.html" 
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


    async def get(self, request, *args, **kwargs):                                    
        url = f'https://newsapi.org/v2/everything?q=finance&apiKey={API_KEY}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                result = await response.json()
                data = result['articles']
                context = {
                        "data": data
                          }
                return render(request, self.template_name, context)                                           
        

    

    




class AboutView(TemplateView):
    template_name = "assistant/about_us.html"

  
