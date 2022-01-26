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

    zipPath = create_zip(CSV_PATH)
    response = create_file_response(zipPath)
    
    print(response.content)
    return response

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

    # downloads pdf from right click
    pdf_path = download_pdf.download_pdf(url, fname=pdf_name, save_path=CSV_PATH)

    # convert its table(s) into csv(s)
    download_pdf.download_pdf_tables(pdf_path, save_path=CSV_PATH, pages=pages)
    os.remove(pdf_path)

    zipPath = create_zip(CSV_PATH)
    response = create_file_response(zipPath)

    print(response)
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


# Creates a HttpResponse with a file attatched
def create_file_response(file_path):
    print(f"--- Sending file {file_path} as HttpResponse")

    # guess_type() returns a tuple (type, encoding) we disregard the encoding
    mime_type, _ = mimetypes.guess_type(file_path)
    fname = os.path.basename(file_path)

    with open(file_path, 'r') as file:
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={fname}"
        return response


#using url /download_file will download a sample text file, fixed file right now 
def download_file(request):

    print("Download\n")
    print(settings.BASE_DIR)

    fl_path = 'streamline/files'
    filename = 'Names.txt'
    filepath = os.path.join(settings.BASE_DIR, fl_path, filename)
    print(filepath)

    fl = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response



def create_zip(folder):
    
    zipPath = os.path.join(CSV_PATH, "tables.zip")
    zipFile = ZipFile(zipPath, 'w')

    # Add multiple files to the zip
    for csv in os.listdir(folder):
        if csv.endswith(".csv"):
            zipFile.write(os.path.join(CSV_PATH, csv))

    zipFile.close()
    return zipPath
    



