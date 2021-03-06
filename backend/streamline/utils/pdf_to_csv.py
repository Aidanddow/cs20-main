import os
import urllib.request
import uuid

import camelot
from streamline.models import Table_PDF

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


def download_pdf(url, save_path=None):
    """
    Simple script to download a pdf from url
    """
    req = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(req)

    # Generates name of pdf file
    pdf_name = str(uuid.uuid4()) + ".pdf"

    path = os.path.join(save_path, pdf_name)

    print("--- Downloading pdf")

    with open(path, "wb") as file:
        file.write(response.read())

    return path


def download_pdf_tables(pdf_path, pdf_obj, save_path=None, pages="all"):
    print("--- Checking for tables in page", pages)
    print("--- PDF PATH ---", pdf_path)

    new_tables = []

    try:
        tables = camelot.read_pdf(pdf_path, pages=pages, flavor="stream", edge_tol=100)
    except Exception as e:

        print(e, "--- PDF is not valid")
        return new_tables

    if len(tables) > 0:

        # saves files with custom name
        for i in range(len(tables)):
            path = os.path.join(
                save_path, f"table{pdf_obj.id}_{tables[i].page}_{i}.csv"
            )
            tables[i].to_csv(path)

            # store each table from page
            new_table = Table_PDF.objects.create(
                pdf_id=pdf_obj, page=tables[i].page, file_path=path
            )
            new_tables.append(new_table)

        print(f"--- {len(tables)} CSV files saved to {save_path}")
    else:
        print("--- No tables found")

    return new_tables


def pages_to_int(pages):
    """
    Transform the user input (a string) into a list of integers, each representing a page
    Returns "all" if "all" is given
    """
    if pages == "all":
        return pages

    page_list = []
    for page in pages.split(","):
        if "-" in page:
            page = page.split("-")
            page_range = list(range(int(page[0]), int(page[1]) + 1))
            page_list += page_range
        else:
            page_list.append(page)

    return page_list


def get_missing_pages(page_list, pdf_obj_id, tables_obj):
    """
    Check which tables are in the DB and return them as a list
    Also, returns the missing pages
    """
    if page_list == "all":
        query = Table_PDF.objects.filter(pdf_id=pdf_obj_id)

        print(f"--- Found {len(query)} tables")

        for table in query:
            tables_obj.append(table)

        print("--- Missing pages: None")

        return "", tables_obj

    pages = []

    for page in page_list:

        if not (query := Table_PDF.objects.filter(pdf_id=pdf_obj_id, page=page)):
            pages.append(str(page))
        else:
            tables_obj += [table for table in query]

    missing_pages = ",".join(pages)
    print("--- Missing pages:", missing_pages or "None")

    return missing_pages, tables_obj
