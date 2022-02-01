from asyncio import base_events
from difflib import context_diff
import json
import os
import urllib.parse
import mimetypes
from zipfile import ZipFile
from pathlib import Path
from django.http import JsonResponse , HttpResponse, HttpResponseRedirect
from django.template import context
from markupsafe import re
from . import extract, download_image, download_pdf
from django.conf import settings
from django.shortcuts import render

from streamline.models import Url_table, Tables
from streamline.forms import *

# Path to which resulting csv files will be saved (will be .../cs20-main/backend/saved)
CSV_PATH = settings.CSV_DIR



def index(request):
    return render(request, 'streamline/index.html')


'''
 Extracts table data from HTML
'''
def get_page_data_HTML(request):
    
    #Get Url
    url = request.GET.get('topic', None)
    print('topic-HTML:', url)

    #store URL
    page = Url_table.objects.create(url=url)
    page_id = page.id
    #process page
    table_count = extract.extract(url, page_id, save_path=CSV_PATH, )
    
    #store each table from page
    for i in range(table_count):
        Tables.objects.create(Url_Id=page, Table_Id=(i + 1))

    
    #inforamtion to pass to the webpage
    Web_Page_Url = Url_table.objects.filter(id = page_id)
    Web_Page_Tables = Tables.objects.filter(Url_Id = page_id)

    context_dict = {}
    context_dict["id"] = page_id
    context_dict["Web_Page_Url"] = Web_Page_Url
    context_dict["Web_Page_Tables"] = Web_Page_Tables
    context_dict["table_count"] = table_count

    return render(request, 'streamline/preview_page.html', context=context_dict)

'''
Extracts table data from PDF
'''
def get_page_data_pdf(request):
    url = request.GET.get('topic', None)
    pages = request.GET.get('pages', None)

    print('topic-PDF:', url)
    print('pages-PDF:', pages)

    # Gets name of pdf file currently being viewed, decodes it
    pdf_name = os.path.basename(url)
    pdf_name = urllib.parse.unquote(pdf_name)

    #store URL
    page = Url_table.objects.create(url=url)
    page_id = page.id
    
    # downloads pdf from right click
    pdf_path = download_pdf.download_pdf(url, fname=pdf_name, save_path=CSV_PATH)
    # convert its table(s) into csv(s) and get table count
    table_count = download_pdf.download_pdf_tables(pdf_path, page_id, save_path=CSV_PATH, pages=pages)
    
    #store each table from page
    for i in range(table_count):
        Tables.objects.create(Url_Id=page, Table_Id=(i + 1))
   
   
   #inforamtion to pass to the webpage
    Web_Page_Url = Url_table.objects.filter(id = page_id)
    Web_Page_Tables = Tables.objects.filter(Url_Id = page_id)

    context_dict = {}
    context_dict["id"] = page_id
    context_dict["Web_Page_Url"] = Web_Page_Url
    context_dict["Web_Page_Tables"] = Web_Page_Tables
    context_dict["table_count"] = table_count

    return render(request, 'streamline/preview_page.html', context=context_dict)

'''
 Extracts table data from images 
 (NOT WORKING) - No table extraction
 '''
def get_page_data_image(request):
    topic = request.GET.get('topic', None)
    print('topic-Image:', topic)

    # downloads the image from the passed url in topic
    # download_image.download(topic)

    data = {}
    return JsonResponse(data)



def preview_page(request, pk=1): 
    context = {"id" : pk}
    return render(request, 'streamline/preview_page.html', context=context)

def download_page(request, pk1=0, pk2=0):
    #pk1 is Url_table.id --- p2k is Tables.Table_Id
    #if pk2 == 0 then download all

    if pk2 == 0:
        #download all
        #filepath = location of created zip file
        filePath = zip_or_csv(folder=CSV_PATH, url_id=pk1, table_id=0)
        response = create_file_response(filePath)
        return response
    else:
        #download table pk2 
        filePath = zip_or_csv(folder=CSV_PATH, url_id=pk1, table_id=pk2)
        response = create_file_response(filePath)
        return response
    
    return response


def zip_or_csv(folder, url_id=0, table_id=0):
    '''
    zip_or_csv() returns a filepath which can be one of two cases
        1. There is only one csv file in folder -> Return the path of the file
        2. There are multiple csv files in folder -> Create a zip archive of files and return that
    '''

    csv_files = [file for file in os.listdir(folder) if file.startswith("table" + str(url_id))]
    if len(csv_files) == 0:
        #there are no tables
        pass
    
    if table_id == 0:
        #download all
        return create_zip(CSV_PATH, url_id)

    else:
        #download only table with id table_id
         return create_zip(CSV_PATH, url_id, table_id)
    

    # if len(csv_files) == 1:
    #     return os.path.join(CSV_PATH, csv_files[0])
    # else:


def create_zip(folder, url_id=0, table_id=0):
    '''
    Will create and return the path to a zip file of all csv files in folder
    '''

    if table_id == 0:
        #download all
        os.chdir(folder)
        zipPath = f"tables{url_id}.zip"   

        with ZipFile(zipPath, 'w') as zipFile:
            # Add multiple files to the zip
            csv_files = [file for file in os.listdir(folder) if (file.startswith("table" + str(url_id)) and file.endswith(".csv"))]
            
            for file in csv_files:
                zipFile.write(file)

    else:
        #download only table with id table_id
        os.chdir(folder)
        zipPath = f"table{url_id}_{table_id}.zip"

        with ZipFile(zipPath, 'w') as zipFile:
            # Add multiple files to the zip
            csv_files = [file for file in os.listdir(folder) if (file.startswith("table" + str(url_id) + "_" + str(table_id)) and file.endswith(".csv"))]
            
            for file in csv_files:
                zipFile.write(file)

    return os.path.abspath(zipPath)
        


def create_file_response(file_path):
    '''
    Creates a HttpResponse with a file attatched, and returns the response
    '''
    print(f"--- Sending file {file_path} as HttpResponse")

    # guess_type() returns a tuple (type, encoding) we disregard the encoding
    mime_type, _ = mimetypes.guess_type(file_path)
    fname = os.path.basename(file_path)

    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={fname}'
        return response


'''
Deletes all files in folder
'''
def clear_folder(folder):
    os.chdir(folder)
    for file in os.listdir(folder):
        os.remove(file)



    



