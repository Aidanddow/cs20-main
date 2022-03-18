from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Url_PDF(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    pdf_path = models.FilePathField(null=True, default=None)
    created = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if Url_PDF.objects.count() >= settings.MAX_ENTRIES:
            Url_PDF.objects.earliest("id").delete()
            print("--- PDF_TUPLE DELETED --- ")

        super(Url_PDF, self).save(*args, **kwargs)


class Url_HTML(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    doi = models.CharField(max_length=200, default="")
    created = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if Url_HTML.objects.count() >= settings.MAX_ENTRIES:
            Url_HTML.objects.earliest("id").delete()
            print("--- HTML_TUPLE DELETED --- ")

        super(Url_HTML, self).save(*args, **kwargs)


class Table_HTML(models.Model):
    id = models.AutoField(primary_key=True)
    html_id = models.ForeignKey(Url_HTML, on_delete=models.CASCADE)
    file_path = models.FilePathField(default=None)


class Table_PDF(models.Model):
    id = models.AutoField(primary_key=True)
    pdf_id = models.ForeignKey(Url_PDF, on_delete=models.CASCADE)
    page = models.IntegerField()
    file_path = models.FilePathField(default=None)
