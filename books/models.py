from django.db import models


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
