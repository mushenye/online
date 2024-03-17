# Generated by Django 4.2.2 on 2024-03-15 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Joining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('other_name', models.CharField(max_length=100)),
                ('Local_church', models.CharField(choices=[('South B', 'South B'), ('Kiambiu', 'Kiambiu'), ('Kitengela', 'Kitengela'), ('Waudo', 'Waudo'), ('Eastleigh', 'Eastleigh'), ('Umoja', 'Umoja'), ('Muthaiga', 'Muthaiga'), ('Runda', 'Runda'), ('Kariokor', 'Kariokor')], max_length=100)),
                ('category', models.CharField(choices=[('L', 'Learner'), ('T', 'Teacher'), ('P', 'Leader'), ('M', 'Member')], max_length=100)),
            ],
        ),
    ]
