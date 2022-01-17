import json
import os
from django.http import JsonResponse , HttpResponse ####
from . import extract, download_image, download_pdf


def index(request):
    return HttpResponse("Hello World! Server is up and running")


def get_page_data_HTML(request):
    topic = request.GET.get('topic', None)
    print('topic-HTML:', topic)
    extract.extract(topic)

    data = {}
    return JsonResponse({data})


def get_page_data_image(request):
    topic = request.GET.get('topic', None)
    print('topic-Image:', topic)

    # downloads the image from the passed url in topic
    # download_image.download(topic)

    data = {}
    return JsonResponse(data)


def get_page_data_pdf(request):
    url = request.GET.get('topic', None)
    pdf_name = os.path.basename(url)

    # downloads pdf from right click
    pdf_path = download_pdf.download_file(url, pdf_name)

    # convert its table(s) into csv(s)
    csv_path = download_pdf.download_pdf_tables(pdf_path)

    data = {}
    return JsonResponse(data)