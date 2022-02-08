from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import RegexValidator


class Contacts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False,)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message=("Phone number must be entered in the format:'+99999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], max_length=100)
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
    tagsString = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.title}'


# class FileTypes(models.Model):
#     file_type = models.CharField(max_length=20, unique=True)
#     file_extention = models.CharField(max_length=5)


# class Files(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=False, blank=False)
#     file_name = models.CharField(max_length=100)
#     file_type = models.ForeignKey(
#         FileTypes, to_field='file_type', on_delete=models.CASCADE, null=False, blank=False, )
#     file_date = models.DateField()
#     file_path = models.CharField(max_length=300)

#     def __str__(self):
#         return f'{self.file_name} {self.file_type} {self.file_date}'

class Files(models.Model):
    user = User
    file_name = models.CharField(max_length=100)
    file_ext = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    file_date = models.DateField()
    file_path = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.file_name} {self.file_type} {self.file_date}'
