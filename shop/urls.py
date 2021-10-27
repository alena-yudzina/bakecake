from django.urls import path
from . import views
from .views import HomePageView


# app_name = 'shop'

urlpatterns = [
    # path('', views.show_main_page, name='main_page'),
    path('', HomePageView.as_view(), name='home'),
    path('cake', views.make_cake_page, name='make_cake_page')
]
