# Generated by Django 3.0.7 on 2020-07-14 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(max_length=200)),
                ('sender', models.CharField(default='students@propulsionacademy.com', max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=2000)),
                ('sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
