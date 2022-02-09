import re
import pandas as pd

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from streamline.models import Url_table, Tables
from django.conf import settings

from .utils import html_to_csv, pdf_to_csv, generics

# Path to which resulting csv files will be saved (will be .../cs20-main/backend/saved)
CSV_PATH = settings.CSV_DIR

@cache_page(settings.CACHE_TIMEOUT)
def get_tables_from_html(request):
    '''
    Extracts table data from HTML
    '''
    # Get url and options
    url = request.GET.get('topic', None)
    options = request.GET.get('options', None)

    print('topic-HTML:', url)
    print('options', options)

    # Set up options list 
    options_list = generics.get_options(options)

    # Store URL
    web_page = Url_table.objects.create(url=url)
    
    # Process page
    table_count = html_to_csv.extract(url, web_page, save_path=CSV_PATH)
    
    context_dict = generics.create_context(web_page, table_count, options_list)

    return render(request, 'streamline/preview_page.html', context=context_dict)


@cache_page(settings.CACHE_TIMEOUT)
def get_tables_from_pdf(request):
    '''
    Extracts table data from PDF
    '''
    url = request.GET.get('topic', None)
    pages = request.GET.get('pages', None)
    options = request.GET.get('options', None)

    print('topic-PDF:', url)
    print('pages-PDF:', pages)
    print('options', options)
    #options - contains string of 01s to indicate true/falses 

    #store URL
    file = Url_table.objects.create(url=url)
    table_count = 0

    regex = "^all$|^\s*[0-9]+\s*((\,|\-)\s*[0-9]+)*\s*$"

    # Check if page input is valid
    if (re.search(regex, pages)):

        #downloads pdf from right click
        pdf_path = pdf_to_csv.download_pdf(url, save_path=CSV_PATH)
        #convert its table(s) into csv(s) and get table count
        table_count = pdf_to_csv.download_pdf_tables(pdf_path, file, save_path=CSV_PATH, pages=pages)

    else:
         print("Invalid input")

    options_list = generics.get_options(options)
    context_dict = generics.create_context(file, table_count, options_list)

    return render(request, 'streamline/preview_page.html', context=context_dict)


def download_file(request, url_id=0, table_id=0):
    """
    A view to download either a zip of all tables, or a singular table
    table_id of 0 indicates the user wants all tables
    """
    if table_id == 0:
        file_path = generics.create_zip(CSV_PATH, url_id, table_id)
    else:  
        table = Tables.objects.filter(Url_Id = url_id, Table_Id=table_id)
        file_path = table.get().csv_path

    return generics.create_file_response(file_path)
    