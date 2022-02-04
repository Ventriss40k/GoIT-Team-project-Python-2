from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Contacts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    b_day = models.DateField(default=now().date(), null=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone_number}'


class Note(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, )
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=300)
    tagsString = models.CharField(max_length=300, default='null')

    def __str__(self):
        return f'{self.title}'


# class NotesTag(models.Model):
#     note_tag = models.CharField(
#         max_length=20, default='just note', null=False, blank=False,)
#     notes = models.ManyToManyField(Note, related_name="tags_list", blank=True)            


class FileTypes(models.Model):
    file_type = models.CharField(max_length=20, unique=True)
    file_extention = models.CharField(max_length=5)


class Files(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    file_name = models.CharField(max_length=100)
    file_type = models.ForeignKey(
        FileTypes, to_field='file_type', on_delete=models.CASCADE, null=False, blank=False, )
    file_date = models.DateField()
    file_path = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.file_name} {self.file_type} {self.file_date}'
