from django.urls import path
from . import views

urlpatterns = [
    path('get_page_data_HTML/', views.get_tables_from_html, name='get_page_data_HTML'),
    path('get_page_data_pdf/', views.get_tables_from_pdf, name='get_page_data_pdf'),
    path('download_file/<int:url_id>/<int:table_id>', views.download_file, name='download_file'),
]