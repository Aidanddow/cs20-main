

# Create your views here.


import json
from django.http import JsonResponse , HttpResponse ####
from . import Extract_HTML



def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


# https://pypi.org/project/wikipedia/#description
def get_page_data(request):
    topic = request.GET.get('topic', None)

    print('topic:', topic)

    data = {}

    Extract_HTML.readURL(topic)


    return JsonResponse(data)