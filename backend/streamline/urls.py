from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r"get_page_data_HTML/$", views.get_tables_from_html, name="get_tables_from_html"),
    url(r"get_page_data_pdf/$", views.get_tables_from_pdf, name="get_tables_from_pdf"),
    path("download_page/<str:table_ids>/<str:table_type>", views.download_file, name="download_file"),
]
