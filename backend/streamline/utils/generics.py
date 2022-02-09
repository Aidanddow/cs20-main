import os
import pandas as pd
import mimetypes
from zipfile import ZipFile
from django.http import HttpResponse
from streamline.models import Url_table, Tables

def create_context(file, table_count, options):
    #inforamtion to pass to the webpage
    Web_Page_Url = Url_table.objects.filter(id = file.id)
    Web_Page_Tables = Tables.objects.filter(Url_Id = file.id)

    context_dict = {}
    context_dict["id"] = file.id
    context_dict["Web_Page_Url"] = Web_Page_Url
    context_dict["table_count"] = table_count
    
    tables_html = []

    #if preview is enabled
    if options[0]:
        for table in Web_Page_Tables:
            try:
                df_csv = pd.read_csv(table.csv_path)
                csv_html = df_csv.to_html()
                
            except:
                # Pandas cannot open the saved HTML to CSV due to the following:
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
                csv_html = "<p>Preview not available</p>"

            tables_html.append((table, csv_html))

    context_dict["Web_Page_Tables"] = tables_html

    return context_dict

'''
Will create and return the path to a zip file of all csv files in folder
'''
def create_zip(folder, url_id=0, table_id=0):
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

    # Create zip file
    with ZipFile(zipPath, 'w') as zipFile:
        for table in tables:
            zipFile.write(os.path.basename(table.csv_path))
    
    return os.path.abspath(zipPath)


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
Deletes all files in folder
'''
def clear_folder(folder):
    
    os.chdir(folder)
    for file in os.listdir(folder):
        os.remove(file)