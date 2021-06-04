from django.db import models
# from datetime import datetime

# Create your models here.
class Contact(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=13)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.fname
