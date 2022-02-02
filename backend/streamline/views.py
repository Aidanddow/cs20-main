from asyncio import base_events
import csv
from difflib import context_diff
import json
import os
import urllib.parse
import mimetypes
from zipfile import ZipFile
from pathlib import Path
from django.http import JsonResponse , HttpResponse, HttpResponseRedirect
from django.template import context
import re
from . import extract, download_image, download_pdf
from django.conf import settings

from django.shortcuts import render

from streamline.models import Url_table, Tables
from streamline.forms import *

import pandas as pd

import re 

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
    web_page = Url_table.objects.create(url=url)
    #process page
    table_count = extract.extract(url, web_page, save_path=CSV_PATH)
    
    #inforamtion to pass to the webpage
    Web_Page_Url = Url_table.objects.filter(id = web_page.id)
    Web_Page_Tables = Tables.objects.filter(Url_Id = web_page.id)

    context_dict = {}
    context_dict["id"] = web_page.id
    context_dict["Web_Page_Url"] = Web_Page_Url
    context_dict["table_count"] = table_count

    tables_html = []

    for table in Web_Page_Tables:
        # Pandas cannot open the saved csv due to the following:
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
        # Hence, I am inserting dummy html code

        # df_csv = pd.read_csv(table.csv_path, engine='python')
        tables_html.append((table, "<p>Preview not available<p>"))

    context_dict["Web_Page_Tables"] = tables_html

    return render(request, 'streamline/preview_page.html', context=context_dict)

'''
Extracts table data from PDF
'''
def get_page_data_pdf(request):
    url = request.GET.get('topic', None)
    pages = request.GET.get('pages', None)

    print('topic-PDF:', url)
    print('pages-PDF:', pages)

    #store URL
    file = Url_table.objects.create(url=url)
    table_count = 0

    regex = "^all$|^\s*[0-9]+\s*((\,|\-)\s*[0-9]+)*\s*$"

    # Check if page input is valid
    if (re.search(regex, pages)):

        print("Valid input")

        #downloads pdf from right click
        pdf_path = download_pdf.download_pdf(url, save_path=CSV_PATH)
        #convert its table(s) into csv(s) and get table count
        table_count = download_pdf.download_pdf_tables(pdf_path, file, save_path=CSV_PATH, pages=pages)
    
    else:
         print("Invalid input")

    #inforamtion to pass to the webpage
    Web_Page_Url = Url_table.objects.filter(id = file.id)
    Web_Page_Tables = Tables.objects.filter(Url_Id = file.id)

    context_dict = {}
    context_dict["id"] = file.id
    context_dict["Web_Page_Url"] = Web_Page_Url
    context_dict["table_count"] = table_count
    
    tables_html = []

    for table in Web_Page_Tables:
        df_csv = pd.read_csv(table.csv_path)
        tables_html.append((table, df_csv.to_html()))

    context_dict["Web_Page_Tables"] = tables_html

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

    #download table pk2 
    filePath = create_zip(CSV_PATH, pk1, pk2)
    response = create_file_response(filePath)
    return response


def create_zip(folder, url_id=0, table_id=0):
    '''
    Will create and return the path to a zip file of all csv files in folder
    '''
    try:
        os.chdir(folder)
    except:
        pass
    
    if table_id == 0:
        #download all
        zipPath = f"tables{url_id}.zip"  

        # query all tables of the given file_id
        tables = Tables.objects.filter(Url_Id = url_id)
    else:
        # download only table with id table_id
        zipPath = f"table{url_id}_{table_id}.zip"

        # query the table with table_id
        tables = Tables.objects.filter(Url_Id = url_id, Table_Id=table_id)

    #download only table with id table_id
    with ZipFile(zipPath, 'w') as zipFile:
        # Add multiple files to the zip
        for table in tables:
            zipFile.write(os.path.basename(table.csv_path))

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



    



