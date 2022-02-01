# Generated by Django 4.0 on 2022-02-01 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='note_path',
            new_name='note_disc',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='note_tags',
        ),
        migrations.AddField(
            model_name='notetags',
            name='notes',
            field=models.ManyToManyField(to='helper_app.Notes'),
        ),
    ]
