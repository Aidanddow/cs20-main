from distutils.command.upload import upload
from pyexpat import model
from tkinter import CASCADE
from django.db import models

class Url_table(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=200)



class Tables(models.Model):
    
    Table_Id = models.IntegerField()
    Url_Id = models.ForeignKey(Url_table, on_delete=models.CASCADE)
    