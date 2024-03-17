from django.db import models
from django.contrib.auth.models import User

from register.choices import CATEGORY, CHURCH



class Tracer(models.Model):
    category =models.CharField(max_length=100, blank=True, null=True)
    mode=models.CharField(max_length=100, blank=True, null=True)
    level=models.CharField(max_length=100, blank=True, null=True)


class Joining(models.Model):
    first_name =models.CharField(max_length=100)
    other_name =models.CharField(max_length=100)
    Local_church=models.CharField(choices=CHURCH, max_length=100 )
    category=models.CharField(choices=CATEGORY, max_length=100)