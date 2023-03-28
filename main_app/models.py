from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.title

class List(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateField()
    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # M:M relationship
    game = models.ManyToManyField(Game)
