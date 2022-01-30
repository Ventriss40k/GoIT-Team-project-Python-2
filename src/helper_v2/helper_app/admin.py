from django.contrib import admin
from .models import Contacts, Notes, NoteTags, Files, FileTypes

admin.site.register(Contacts)
admin.site.register(Notes)
admin.site.register(NoteTags)
admin.site.register(Files)
admin.site.register(FileTypes)
