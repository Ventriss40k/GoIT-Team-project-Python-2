# Generated by Django 4.0 on 2022-02-01 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper_app', '0006_remove_note_tag_note_tag_list_notestag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='user',
        ),
    ]
