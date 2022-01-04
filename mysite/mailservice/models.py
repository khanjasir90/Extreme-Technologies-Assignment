from django.db import models
from django.utils import timezone
# Create your models here.

class MailService(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    time=models.TimeField(default=timezone.now())
