# Generated by Django 4.2.2 on 2024-02-25 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_rename_taught_on_date_lessontopic_taught_on_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('number_of_students', models.IntegerField()),
                ('comment', models.TextField(max_length=200)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.lessontopic')),
            ],
        ),
    ]
