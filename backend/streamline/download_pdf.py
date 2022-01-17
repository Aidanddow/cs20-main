'''
Download pdf tables from terminal with

% python download_pdf.py <filename>
'''

import urllib.request
import camelot 
import sys
import os

# Need to mkdir files folder in current directory to work
FOLDER = "files"

#Simple script to download a pdf from a link - wont be used in project, just used 
#to make sure the pdf is got, no filename handling
def download_file(download_url, pdf_name):
    response = urllib.request.urlopen(download_url)    
    pdf_path = os.path.join(FOLDER, pdf_name) 

    print("--- Downloading pdf")
        
    with open(pdf_path, 'wb') as file:
        file.write(response.read())
    
    return pdf_path


def download_pdf_tables(pdf_path, pages="all"):
    print("--- Checking for tables") 
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream", edge_tol=100)

    if len(tables) > 0:
        print(f"--- Saving {len(tables)} tables to CSV")
        csv_path = os.path.join(FOLDER, "table.csv")
        tables.export(csv_path, f='csv', compress=False)
        print(f"--- CSV files saved to {csv_path}")
    else:
        print("--- No tables found")



# Temporary main method to download pdf tables from terminal
if __name__ == "__main__":
    try:
        pdf = sys.argv[1]
        download_pdf_tables(pdf)
    except IndexError:
        print("No pdf file provided")
    except Exception as e:
        print("Error", e)

