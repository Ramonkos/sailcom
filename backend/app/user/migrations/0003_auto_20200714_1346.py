# Generated by Django 3.0.7 on 2020-07-14 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='title',
            new_name='titel',
        ),
    ]
