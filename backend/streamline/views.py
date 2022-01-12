

# Create your views here.


from datetime import date
import json
from django.http import JsonResponse , HttpResponse ####
from . import extract, download_image, download_pdf



def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


# https://pypi.org/project/wikipedia/#description
def get_page_data_HTML(request):
    topic = request.GET.get('topic', None)

    print('topic-HTML:', topic)

    data = {}

    extract.extract(topic)


    return JsonResponse(data)

def get_page_data_image(request):
    topic = request.GET.get('topic', None)

    print('topic-Image:', topic)

    data = {}
    #downloads the image from the passed url in topic
    #download_image.download(topic)

    return JsonResponse(data)

def get_page_data_pdf(request):
    topic = request.GET.get('topic', None)

    print('topic-PDF:', topic)

    data = {}
    #downloads pdf from right click
    #download_pdf.download_file(topic)
   
    return JsonResponse(data)