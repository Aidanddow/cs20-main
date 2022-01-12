from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^get_page_data_HTML/$', views.get_page_data_HTML, name='get_page_data_HTML'),
    url(r'get_page_data_image/$', views.get_page_data_image, name='get_page_data_image'),
    url(r'get_page_data_pdf/$', views.get_page_data_pdf, name='get_page_data_pdf'),
]