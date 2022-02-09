import os
import pandas as pd
import mimetypes
from zipfile import ZipFile
from django.http import HttpResponse

from streamline.models import Table_PDF, Table_HTML

def create_context(url_obj, tables_obj, table_type="pdf"):
    #inforamtion to pass to the webpage

    context_dict = {}
    context_dict["url_id"] = url_obj.id
    context_dict["table_count"] = len(tables_obj)
    context_dict["table_type"] = table_type
    
    tables_html = []
    table_ids = ""

    for table in tables_obj:
        table_id = str(table.id)
        table_ids = table_ids + "," + table_id
        try:
            df_csv = pd.read_csv(table.file_path, index_col=False)
            df_csv.fillna('', inplace=True)
            df_csv.set_index(df_csv.columns[0], inplace=True)
            # df_csv.reset_index(drop=True, inplace=True)
            csv_html = df_csv.to_html()
        except:
            # Pandas cannot open the saved HTML to CSV due to the following:
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
            csv_html = "<p>Preview not available</p>"
        
        tables_html.append((table_id, csv_html))

    if(table_ids!=""):
        table_ids = table_ids[1:]

    context_dict["Web_Page_Tables"] = tables_html
    context_dict["table_ids"] = table_ids

    return context_dict

'''
Will create and return the path to a zip file of all csv files in folder
'''
def create_zip(folder, table_ids="", table_type="pdf"):
    try:
        os.chdir(folder)
    except:
        pass

    zipPath = f"tables.zip" 

    table_paths = []

    if(table_type=="pdf"):
        for table_id in table_ids.split(","):
            table_paths.append(Table_PDF.objects.filter(id = int(table_id)).first().file_path)
    else:
        for table_id in table_ids.split(","):
            table_paths.append(Table_HTML.objects.filter(id = int(table_id)).first().file_path)
        
    # Create zip file
    with ZipFile(zipPath, 'w') as zipFile:
        for path in table_paths:
            zipFile.write(os.path.basename(path))
    
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
    
    # Remove created zip file from server
    os.remove(file_path)

    return response

'''
Deletes all files in folder
'''
def clear_folder(folder):
    os.chdir(folder)
    for file in os.listdir(folder):
        os.remove(file)