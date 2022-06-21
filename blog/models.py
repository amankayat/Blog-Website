from django.db import models

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    desc = models.TextField()