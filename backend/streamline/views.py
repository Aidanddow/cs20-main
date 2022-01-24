from asyncio import base_events
import json
import os
import urllib.parse
import mimetypes
from pathlib import Path
from django.http import JsonResponse , HttpResponse
from . import extract, download_image, download_pdf
from django.conf import settings

# Path to which resulting csv files will be saved 
CSV_PATH = os.path.join(Path.home(), "Desktop", "files")
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
    first_file = os.listdir(CSV_PATH)[0]
    first_file_path = os.path.join(CSV_PATH, first_file)

    response = create_file_response(first_file_path)
    print(response.content)
    return response

'''
Extracts table data from PDF
'''
def get_page_data_pdf(request):
    url = request.GET.get('topic', None)
    print('topic-PDF:', url)

    # Gets name of pdf file currently being viewed, decodes it
    pdf_name = os.path.basename(url)
    pdf_name = urllib.parse.unquote(pdf_name)

    # downloads pdf from right click
    pdf_path = download_pdf.download_pdf(url, fname=pdf_name, save_path=CSV_PATH)

    # convert its table(s) into csv(s)
    download_pdf.download_pdf_tables(pdf_path, save_path=CSV_PATH)
    os.remove(pdf_path)

    first_file = os.listdir(CSV_PATH)[0]
    response = create_file_response(first_file)
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

def get_fname(path):
    return path.split("/")[-1]
