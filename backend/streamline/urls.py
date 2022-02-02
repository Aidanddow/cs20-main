from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'get_page_data_HTML/$', views.get_page_data_HTML, name='get_page_data_HTML'),
    url(r'get_page_data_pdf/$', views.get_page_data_pdf, name='get_page_data_pdf'),
    path('download_page/<int:url_id>/<int:table_id>', views.download_page, name='download_page'),
]