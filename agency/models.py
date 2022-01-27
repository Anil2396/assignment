from ast import mod
from email import message
from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=50,null=False)
    email = models.CharField(max_length=50,null=False,primary_key=True)
    role= models.CharField(max_length=50,null=False)
    status = models.CharField(max_length=50,default="Pending")
    resume = models.ImageField(upload_to='resume/')
    date = models.DateTimeField(auto_now_add=True)
class Interview(models.Model):
    interview_id=models.AutoField(primary_key=True)
    userid = models.ForeignKey("User",models.DO_NOTHING,db_column="email",blank=False,null=False,)
    schedule_time_from = models.DateTimeField(null=False,name="schedule_time_from",unique=True)
    schedule_time_to = models.DateTimeField(null=False,name="schedule_time_to",unique=True)
class Emails(models.Model):
    id = models.AutoField(primary_key=True) 
    userid = models.ForeignKey("User",models.DO_NOTHING,db_column="email",blank=False,null=False,)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=50)