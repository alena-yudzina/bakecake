from django.urls import path
from .views import SignUpView, show_orders


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('account/', show_orders, name='account'),
]
