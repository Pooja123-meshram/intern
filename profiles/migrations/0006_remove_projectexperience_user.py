# Generated by Django 5.0.6 on 2024-06-01 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_projectexperience_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectexperience',
            name='user',
        ),
    ]
