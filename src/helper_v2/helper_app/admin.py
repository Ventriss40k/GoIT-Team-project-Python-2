from django.contrib import admin
from .models import Contacts, Note, Files, FileTypes

admin.site.register(Contacts)
admin.site.register(Note)
admin.site.register(Files)
admin.site.register(FileTypes)
