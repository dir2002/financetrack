# Generated by Django 5.1.7 on 2025-04-14 14:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OpenningBalance',
            new_name='OpeningBalance',
        ),
    ]
