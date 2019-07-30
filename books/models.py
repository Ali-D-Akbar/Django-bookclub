from django.db import models

from userauth.models import Profile


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default='1')
