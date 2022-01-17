import json
import os
import urllib.parse
from pathlib import Path
from django.http import JsonResponse , HttpResponse
from . import extract, download_image, download_pdf

# Path to which resulting csv files will be saved 
CSV_PATH = os.path.join(Path.home(), "Desktop")

def index(request):
    return HttpResponse("Hello World! Server is up and running")

'''
 Extracts table data from HTML
'''
def get_page_data_HTML(request):
    url = request.GET.get('topic', None)
    print('topic-HTML:', url)
    extract.extract(url, save_path=CSV_PATH)

    data = {}
    return JsonResponse(data)

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

    data = {}
    return JsonResponse(data)

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