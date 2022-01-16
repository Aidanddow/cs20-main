import urllib.request

FOLDER = "files"

#Simple script to download a pdf from a link - wont be used in project, just used 
#to make sure the pdf if got, no filename handling
def download_file(download_url, pdf_name):
    response = urllib.request.urlopen(download_url)    
    pdf_path = os.path.join(FOLDER, pdf_name) 

    print("--- Downloading pdf")
        
    file = open(pdf_path, 'wb')
    file.write(response.read())
    file.close()
 
import camelot 
import os

def get_csv_table_from_pdf(pdf_name, pages="all"):

    pdf_path = os.path.join(FOLDER, pdf_name) 
    csv_path = os.path.join(FOLDER, "table.csv") 

    print("--- Checking for tables")

    tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream", edge_tol=100)

    if(tables.n>0):
        print("--- Saving tables to CSV")
        tables.export(csv_path, f='csv', compress=False)
    else:
        print("--- No tables found")
    
    return