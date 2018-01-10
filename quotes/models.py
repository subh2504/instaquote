from django.db import models

from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    activated = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    