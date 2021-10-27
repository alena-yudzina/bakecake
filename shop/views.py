from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import CakeConstructorForm


def show_main_page(request):
    return render(request, 'main_page.html')


def make_cake_page(request):
    form = CakeConstructorForm()
    context = {'form': form}
    return render(
        request,
        'cake_constructor.html',
        context=context
    )


class HomePageView(TemplateView):
    template_name = 'home.html'
