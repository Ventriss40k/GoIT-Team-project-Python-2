# Generated by Django 4.0 on 2022-02-01 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper_app', '0004_rename_note_disc_note_note_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='tag',
            field=models.CharField(default='default tag', max_length=300),
        ),
        migrations.DeleteModel(
            name='NotesTag',
        ),
    ]
