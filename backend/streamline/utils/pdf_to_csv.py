'''
Download tables from pdf from terminal with

% python download_pdf.py <filename>
'''

import camelot 
import sys
import os
import urllib.request
from streamline.models import Tables

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

# Simple script to download a pdf from a link - wont be used in project, just used 
# to make sure the pdf is got, no filename handling
def download_pdf(url, save_path=None):

    req = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(req)

    # Gets name of pdf file currently being viewed, decodes it
    pdf_name = os.path.basename(url)
    pdf_name = urllib.parse.unquote(pdf_name)

    path = os.path.join(save_path, pdf_name)   

    print("--- Downloading pdf")
        
    with open(path, 'wb') as file:
        file.write(response.read())

    return path


def download_pdf_tables(pdf_path, file, save_path=None, pages="all"):
    print("--- Checking for tables in page", pages)

    tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream", edge_tol=100)

    if len(tables) > 0:
        print(f"--- Saving {len(tables)} tables to CSV")
        
        #saves files with custom name
        for i in range(len(tables)):
            table_id = i + 1
            
            path = os.path.join(save_path, f"table{file.id}_{table_id}.csv")
            tables[i].to_csv(path)

            #store each table from page
            Tables.objects.create(Url_Id=file, Table_Id=(i + 1), csv_path = path)
        
        print(f"--- {len(tables)} CSV files saved to {save_path}")
    else:
        print("--- No tables found")

    number_of_tables = len(tables)
    return number_of_tables


# Temporary main method to download pdf tables from terminal
if __name__ == "__main__":
    try:
        pdf = sys.argv[1]
        download_pdf_tables(pdf)
    except IndexError:
        print("No pdf file provided")
    except Exception as e:
        print("Error", e)

