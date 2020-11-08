from django.db import models
from django.utils import timezone
# Create your models here.
class Orders(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()


