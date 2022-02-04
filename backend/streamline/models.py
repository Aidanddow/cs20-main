from tkinter import CASCADE
from django.db import models

class Url_PDF(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    # title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    # doi = models.CharField(max_length=200)
    pdf_path = models.FilePathField(null=True, default=None)

class Url_HTML(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)

class Table_HTML(models.Model):
    id = models.AutoField(primary_key=True)
    html_id = models.ForeignKey(Url_HTML, on_delete=models.CASCADE)
    file_path = models.FilePathField(default=None)

class Table_PDF(models.Model):
    id = models.AutoField(primary_key=True)
    pdf_id = models.ForeignKey(Url_PDF, on_delete=models.CASCADE)
    page = models.IntegerField()
    file_path = models.FilePathField(default=None)
    