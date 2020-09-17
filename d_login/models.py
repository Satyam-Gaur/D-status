from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class UserData(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    updated_on = models.DateTimeField(default = datetime.now)
    t_factor = models.DecimalField(max_digits=3, decimal_places=2,default = 0.00)
    trainings = models.TextField(default = "")
    projects = models.TextField(default = "")
    status = models.CharField(max_length=250,default = "")
    leaves = models.CharField(max_length=100,default = "")

    def is_next_day(self, other):
        if self.updated_on.day>other.day and self.updated_on.month >= other.month and self.updated_on.year >= other.year:
            return True
        else:
            return False

class UserDataHistory(models.Model):
    class Meta:
        unique_together = (('updated_on','user'))
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(default = datetime.now)
    t_factor = models.DecimalField(max_digits=3, decimal_places=2,default = 0.00)
    trainings = models.TextField(default = "")
    projects = models.TextField(default = "")
    status = models.CharField(max_length=250,default = "")
    leaves = models.CharField(max_length=100,default = "")


class UserProjectData(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.TextField(default = "")
    project1 = models.TextField(default = "")
    project2 = models.TextField(default = "")
    project3 = models.TextField(default = "")
    project4 = models.TextField(default = "")
    project5 = models.TextField(default = "")
    project6 = models.TextField(default = "")
    project7 = models.TextField(default = "")
    project8 = models.TextField(default = "")
    project9 = models.TextField(default = "")
    project10 = models.TextField(default = "")
