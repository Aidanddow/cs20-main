import os
import pandas as pd
import mimetypes
from zipfile import ZipFile
from django.http import HttpResponse
from streamline.models import Url_table, Tables

def get_options(options):
    """
    Receives a string of 1's and 0's corresponding to different user settings
    """
    return [int(char) if char.isdigit() else 1 for char in options]


def get_html_representations(tables):
    """
    Returns a list containing html representations of the csv tables
    """
    tables_html = []

    for table in tables:
        try:
            df_csv = pd.read_csv(table.csv_path)
            csv_html = df_csv.to_html()
                
        except UnicodeDecodeError:
            csv_html = "<p>Preview not available</p>"
        
        tables_html.append((table, csv_html))
    return tables_html


def create_context(file, table_count, options):
    """
    Returns a dictionary to provide context to the extension
    """
    #inforamtion to pass to the webpage
    webpage_tables = Tables.objects.filter(Url_Id = file.id)

    #if preview is enabled
    # if options[0]:
    tables_html = get_html_representations(webpage_tables)

    return { "id": file.id,
             "table_count": table_count,
             "Web_Page_Url": Url_table.objects.filter(id = file.id),
             "Web_Page_Tables": tables_html }


def create_zip(folder, url_id=0, table_id=0):
    '''
    Will create and return the path to a zip file of all csv files from a given url
    '''
    os.chdir(folder)

    # Query all tables of the given file_id
    tables = Tables.objects.filter(Url_Id = url_id)

    zipPath = f"tables{url_id}.zip"  

    with ZipFile(zipPath, 'w') as zipFile:
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
