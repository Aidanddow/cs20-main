'''
Download tables from pdf from terminal with

% python download_pdf.py <filename>
'''
import camelot 
import sys
import os
import urllib.request
from streamline.models import Table_PDF

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def download_pdf(url, save_path=None):
    '''
    Simple script to download a pdf from url
    '''
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


def download_pdf_tables(pdf_path, pdf_obj, save_path=None, pages="all"):
    print("--- Checking for tables in page", pages)
    print("--- PDF PATH ---", pdf_path)

    new_tables = []

    try:
        tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream", edge_tol=100)
    except:
        print("--- PDF is not valid")
        return new_tables

    if len(tables) > 0:
        
        # saves files with custom name
        for i in range(len(tables)):            
            path = os.path.join(save_path, f"table{pdf_obj.id}_{tables[i].page}_{i}.csv")
            tables[i].to_csv(path)

            # store each table from page
            new_table = Table_PDF.objects.create(pdf_id=pdf_obj, page = tables[i].page, file_path = path)
            new_tables.append(new_table)
        
        print(f"--- {len(tables)} CSV files saved to {save_path}")
    else:
        print("--- No tables found")

    return new_tables


def pages_to_int(pages):
    '''
    Transform the user input (a string) into a list of integers, each representing a page
    Returns "all" if "all" is given
    '''

    if(pages=="all"):
        return pages

    page_list = []
    for page in pages.split(','):
        if '-' in page:
            page = page.split('-')

            page_range = list(range(int(page[0]), int(page[1])+1))

            page_list = page_list+page_range
        else:
            page_list.append(page)
    
    return page_list


def get_missing_pages(page_list, pdf_obj_id, tables_obj):
    '''
    Check which tables are in the DB and return them as a list
    Also, returns the missing pages
    '''

    if(page_list=="all"):
        query = Table_PDF.objects.filter(pdf_id=pdf_obj_id)
        
        print(f"--- Found {len(query)} tables")

        for table in query:
            tables_obj.append(table)

        print("--- Missing pages: None")
        
        return "", tables_obj
            

    pages = []
    for page in page_list:
        query = Table_PDF.objects.filter(pdf_id=pdf_obj_id, page=page)
        
        if not query:
            pages.append(str(page))
        else:
            for table in query:
                tables_obj.append(table)

    missing_pages = ",".join(pages)
    print("--- Missing pages:", (missing_pages if missing_pages!="" else "None"))

    return missing_pages, tables_obj

# Temporary main method to download pdf tables from terminal
if __name__ == "__main__":
    try:
        pdf = sys.argv[1]
        download_pdf_tables(pdf)
    except IndexError:
        print("No pdf file provided")
    except Exception as e:
        print("Error", e)
