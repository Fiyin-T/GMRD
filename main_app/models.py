from django.db import models

# Create your models here.
class Video_Game(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class List(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateField()
    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # M:M relationship
    video_game = models.ManyToManyField(Video_Game)
