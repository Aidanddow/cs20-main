from asyncio import base_events
import json
import os
import urllib.parse
import mimetypes
from zipfile import ZipFile
from pathlib import Path
from django.http import JsonResponse , HttpResponse
from . import extract, download_image, download_pdf
from django.conf import settings
import re 

# Path to which resulting csv files will be saved (will be .../cs20-main/backend/saved)
CSV_PATH = settings.CSV_DIR

def index(request):
    return HttpResponse("Hello World! Server is up and running")

'''
 Extracts table data from HTML
'''
def get_page_data_HTML(request):
    url = request.GET.get('topic', None)
    print('topic-HTML:', url)
    extract.extract(url, save_path=CSV_PATH)
    filePath = zip_or_csv(folder=CSV_PATH)
    response = create_file_response(filePath)
    
    print(response)
    clear_folder(CSV_PATH)
    return response

'''
Extracts table data from PDF
'''
def get_page_data_pdf(request):
    url = request.GET.get('topic', None)
    pages = request.GET.get('pages', None)

    print('topic-PDF:', url)
    print('pages-PDF:', pages)

    regex = "^\s*[0-9]+\s*((\,|\-)\s*[0-9]+)*\s*$|^all$/g"

    # Check if page input is valid
    if (re.search(regex, pages)):

        print("Valid input")

        # Gets name of pdf file currently being viewed, decodes it
        pdf_name = os.path.basename(url)
        pdf_name = urllib.parse.unquote(pdf_name)

        # downloads pdf from right click
        pdf_path = download_pdf.download_pdf(url, fname=pdf_name, save_path=CSV_PATH)

        # convert its table(s) into csv(s)
        download_pdf.download_pdf_tables(pdf_path, save_path=CSV_PATH, pages=pages)

    filePath = zip_or_csv(CSV_PATH)
    response = create_file_response(filePath)

    print(response)
    clear_folder(CSV_PATH)

    return response

'''
 Extracts table data from images 
 (NOT WORKING)
 '''
def get_page_data_image(request):
    topic = request.GET.get('topic', None)
    print('topic-Image:', topic)

    # downloads the image from the passed url in topic
    # download_image.download(topic)

    data = {}
    return JsonResponse(data)


'''
Creates a HttpResponse with a file attatched, and returns the response
'''
def create_file_response(file_path):
    print(f"--- Sending file {file_path} as HttpResponse")

    # guess_type() returns a tuple (type, encoding) we disregard the encoding
    mime_type, _ = mimetypes.guess_type(file_path)
    fname = os.path.basename(file_path)

    with open(file_path, 'rb') as file:
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={fname}'
        return response


'''
Will create and return the path to a zip file of all csv files in folder
'''
def create_zip(folder):
    os.chdir(folder)
    zipPath = "tables.zip"

    with ZipFile(zipPath, 'w') as zipFile:

        # Add multiple files to the zip
        csv_files = (file for file in os.listdir(folder) if file.endswith('.csv'))
        
        for file in csv_files:
            zipFile.write(file)

    return os.path.abspath(zipPath)

'''
zip_or_csv() returns a filepath which can be one of two cases
    1. There is only one csv file in folder -> Return the path of the file
    2. There are multiple csv files in folder -> Create a zip archive of files and return that
'''
def zip_or_csv(folder):
    csv_files = [file for file in os.listdir(folder) if file.endswith(".csv")]

    if len(csv_files) == 1:
        return os.path.join(CSV_PATH, csv_files[0])
    else:
        return create_zip(CSV_PATH)

'''
Deletes all files in folder
'''
def clear_folder(folder):
    os.chdir(folder)
    for file in os.listdir(folder):
        os.remove(file)


def download_file(request):
    pass
    



