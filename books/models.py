from django.db import models

from django.contrib.auth import get_user_model


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
