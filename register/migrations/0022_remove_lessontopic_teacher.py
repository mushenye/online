# Generated by Django 4.2.2 on 2024-03-18 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0021_alter_onlineperson_person_alter_onlineperson_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessontopic',
            name='teacher',
        ),
    ]