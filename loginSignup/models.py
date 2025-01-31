from django.db import models

# Create your models here.
class register(models.Model):
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    mobile=models.IntegerField()