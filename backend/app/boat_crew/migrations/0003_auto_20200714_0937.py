# Generated by Django 3.0.7 on 2020-07-14 09:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boat_crew', '0002_boatcrew_crew_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boatcrew',
            name='crew_member',
        ),
        migrations.AddField(
            model_name='boatcrew',
            name='crew_member',
            field=models.ManyToManyField(blank=True, null=True, related_name='boat', to=settings.AUTH_USER_MODEL),
        ),
    ]