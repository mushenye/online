from django.db import models
from django.contrib.auth.models import User



class Tracer(models.Model):
    category =models.CharField(max_length=100, blank=True, null=True)
    mode=models.CharField(max_length=100, blank=True, null=True)
    level=models.CharField(max_length=100, blank=True, null=True)
