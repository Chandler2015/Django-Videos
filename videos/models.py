from django.db import models
from django.contrib.auth.models import User


class Videos(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    youtube_id = models.CharField(max_length=100)
    videos = models.ForeignKey(Videos, on_delete=models.CASCADE)
