from django import urls

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from shop.models import Berry, CakeLevel, CakeForm, Decor, Topping

from .forms import CakeConstructorForm, OrderDetailsForm


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


def order_details(request):
    cake_params = CakeConstructorForm(request.POST)
    cake_params.is_valid()
    cake_level_price = CakeLevel.objects.get(pk=cake_params.cleaned_data['cake_level']).price
    cake_form_price = CakeForm.objects.get(pk=cake_params.cleaned_data['cake_form']).price
    topping_price = Topping.objects.filter(pk__in=cake_params.cleaned_data['topping']).values_list('price', flat=True)
    berry_price = Berry.objects.filter(pk__in=cake_params.cleaned_data['berry']).values_list('price', flat=True)
    decor_price = Decor.objects.filter(pk__in=cake_params.cleaned_data['decor']).values_list('price', flat=True)
    total_price = sum([cake_level_price, cake_form_price, *topping_price, *berry_price, *decor_price])
    form = OrderDetailsForm(initial={'price': total_price})
    return render(request, 'order_details.html', {'form': form})


def make_order(request):
    if request.method == 'GET':
        return redirect(urls.reverse('make_cake_page'))
    return render(request, 'order_details.html', {})


class HomePageView(TemplateView):
    template_name = 'home.html'
