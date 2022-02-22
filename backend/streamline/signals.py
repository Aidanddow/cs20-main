# code
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Table_HTML, Url_PDF, Table_PDF

import os
from django.conf import settings

PDF_PATH = settings.PDF_DIR
CSV_PATH = settings.CSV_DIR

 
@receiver(post_delete, sender=Url_PDF)
def delete_pdf(sender, instance, **kwargs):

    if(os.path.isfile(instance.pdf_path)):

        os.chdir(PDF_PATH)
        print("--- PDF",instance.pdf_path,"DELETED --- ")
        os.remove(instance.pdf_path)

@receiver(post_delete, sender=Table_PDF)
def delete_pdf_csv(sender, instance, **kwargs):
    
    if(os.path.isfile(instance.file_path)):

        os.chdir(CSV_PATH)
        print("--- CSV",instance.file_path,"DELETED --- ")
        os.remove(instance.file_path)

@receiver(post_delete, sender=Table_HTML)
def delete_html_csv(sender, instance, **kwargs):

    if(os.path.isfile(instance.file_path)):

        os.chdir(CSV_PATH)
        print("--- CSV",instance.file_path,"DELETED --- ")
        os.remove(instance.file_path)