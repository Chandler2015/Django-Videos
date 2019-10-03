from django.db import models


class Videos(models.Model):
    title = models.CharField(max_length=200)


class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    youtube_id = models.CharField(max_length=100)
    videos = models.ForeignKey(Videos, on_delete=models.CASCADE)
