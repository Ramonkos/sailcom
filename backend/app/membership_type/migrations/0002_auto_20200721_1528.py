# Generated by Django 3.0.7 on 2020-07-21 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership_type', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membershiptype',
            old_name='membershipFee',
            new_name='membership_fee',
        ),
    ]
