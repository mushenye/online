# Generated by Django 4.2.2 on 2024-02-23 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='user',
        ),
    ]