from django.shortcuts import render
from django.views.generic import TemplateView


def show_main_page(request):
    return render(request, 'main_page.html')


class HomePageView(TemplateView):
    template_name = 'home.html'
