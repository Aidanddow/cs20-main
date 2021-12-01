from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^get_page_data/$', views.get_page_data, name='get_page_data'),
]