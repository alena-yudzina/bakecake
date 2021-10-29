from django.urls import path
from . import views
from .views import HomePageView


# app_name = 'shop'

urlpatterns = [
    # path('', views.show_main_page, name='main_page'),
    path('', HomePageView.as_view(), name='home'),
    path('cake', views.make_cake_page, name='make_cake_page'),
    path('order_details', views.order_details, name='order_details'),
    path('make_order', views.make_order, name='make_order'),
    path('get_code', views.get_and_check_promo_code, name='get_and_check_promo_code'),
]
