# Generated by Django 4.0 on 2022-02-01 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helper_app', '0007_remove_note_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='tag_list',
            new_name='tags',
        ),
        migrations.DeleteModel(
            name='NotesTag',
        ),
    ]
