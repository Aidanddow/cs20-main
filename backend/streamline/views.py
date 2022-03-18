from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render

from streamline.models import Table_HTML, Url_HTML, Url_PDF

from .utils import generics, html_to_csv, pdf_to_csv

# Path to which resulting csv files will be saved (will be .../cs20-main/backend/saved)
CSV_PATH = settings.CSV_DIR
PDF_PATH = settings.PDF_DIR


def get_tables_from_html(request):
    """
    Extracts table data from HTML
    """
    request_data = generics.get_data_from_request(request, get_pages=False)

    if type(request_data) == HttpResponseBadRequest:
        return request_data

    url, options, _ = request_data

    # Try to find tables in database
    html_obj = Url_HTML.objects.filter(url=url).first()

    # If not in database or reprocess is on
    if not html_obj and not "force_reprocess" in options.keys():
        # store URL
        html_obj = Url_HTML.objects.create(url=url)
        print("--- New HTML URL:", html_obj.url)

        # process page
        html_to_csv.extract(url, html_obj, options, save_path=CSV_PATH)

    # Query extracted tables

    if tables_obj := Table_HTML.objects.filter(html_id=html_obj.id):
        context_dict = generics.create_context(html_obj, tables_obj, table_type="html")
        return render(request, "streamline/preview_page.html", context=context_dict)
    else:
        return render(request, "streamline/no_tables.html", context={})


def get_tables_from_pdf(request):
    """
    Extracts table data from PDF
    """
    request_data = generics.get_data_from_request(request, get_pages=True)

    if type(request_data) == HttpResponseBadRequest:
        return request_data

    url, options, pages = request_data
    tables_obj = list()

    # Check if page input is valid
    if generics.check_valid_page_input(pages):
        page_list = pdf_to_csv.pages_to_int(pages)

        pdf_obj = Url_PDF.objects.filter(url=url).first()

        # If the pdf already exists in db or force reprocess is off
        if pdf_obj and not "force_reprocess" in options.keys():
            print("--- PDF Found ---", pdf_obj.url)
            pdf_path = pdf_obj.pdf_path

            pages, tables_obj = pdf_to_csv.get_missing_pages(
                page_list, pdf_obj.id, tables_obj
            )

        else:
            print("--- New PDF:", url)
            # downloads pdf from right click
            pdf_path = pdf_to_csv.download_pdf(url, save_path=PDF_PATH)
            # store URL
            pdf_obj = Url_PDF.objects.create(url=url, pdf_path=pdf_path)

        # convert its table(s) into csv(s) and get table count
        if pages:
            new_tables = pdf_to_csv.download_pdf_tables(
                pdf_path, pdf_obj, save_path=CSV_PATH, pages=pages
            )
            tables_obj += new_tables

    else:
        print("\n--- Invalid page input")
        return HttpResponseBadRequest("<h1>Invalid Input</h1>")

    if tables_obj:
        context_dict = generics.create_context(pdf_obj, tables_obj, table_type="pdf")
        return render(request, "streamline/preview_page.html", context=context_dict)

    else:
        return render(request, "streamline/no_tables.html", context={})


def download_file(request, table_ids, table_type):
    """
    A view to download either a zip of all tables, or a singular table
    table_id of 0 indicates the user wants all tables
    """
    if not table_ids or not table_type:
        print("\n--- Invalid Download request")
        return HttpResponseBadRequest("<h1>Invalid Request</h1>")

    # No table paths are required
    if not (table_paths := generics.get_filepaths_from_id(table_ids, table_type)):
        print("\n--- File(s) not found")
        return HttpResponseNotFound("<h1>File(s) not found</h1>")

    # Only one table path is required -> send as file
    elif len(table_paths) == 1:
        file_path = table_paths[0]

    # Multiple paths are required -> send as zip
    else:
        print("--- Sending tables as zip")
        file_path = generics.create_zip(table_paths, folder=CSV_PATH)

    return generics.create_file_response(file_path)
