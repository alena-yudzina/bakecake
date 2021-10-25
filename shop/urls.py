from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.show_main_page, name='main_page'),
]
