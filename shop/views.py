from django.contrib.auth.decorators import login_required

from django import urls
from django.http import JsonResponse

from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from shop.models import Berry, Cake, CakeLevel, CakeForm, Decor, Order, Topping, PromoCode

from .forms import CakeConstructorForm, OrderDetailsForm


def get_and_check_promo_code(request):
    actualPromoCode = PromoCode.objects.first().code
    code_is_used = request.user.orders.filter(
        promo_code__code=actualPromoCode
    ).exists()
    return JsonResponse(
        {'actualCode': actualPromoCode, 'thisClientUsed': code_is_used}
    )


def show_main_page(request):
    return render(request, 'main_page.html')


@login_required
def make_cake_page(request):
    form = CakeConstructorForm()
    context = {'form': form}
    return render(
        request,
        'cake_constructor.html',
        context=context
    )


@login_required
def order_details(request):
    if request.method == 'GET':
        return redirect(urls.reverse('make_cake_page'))
    cake_params = CakeConstructorForm(request.POST)
    cake_params.is_valid()
    total_price = sum([
        CakeLevel.objects.get(pk=cake_params.cleaned_data['cake_level']).price,
        CakeForm.objects.get(pk=cake_params.cleaned_data['cake_form']).price,
        Topping.objects.get(pk__in=cake_params.cleaned_data['topping']).price,
        *Decor.objects.filter(pk__in=cake_params.cleaned_data['decor']).values_list('price', flat=True),
        *Berry.objects.filter(pk__in=cake_params.cleaned_data['berry']).values_list('price', flat=True)
    ])
    form = OrderDetailsForm(initial={'price': total_price, 'destination': request.user.address})
    return render(
        request,
        'order_details.html',
        {'form': form, 'cake_params': cake_params, 'price': total_price}
    )


@login_required
def make_order(request):
    if request.method == 'GET':
        return redirect(urls.reverse('make_cake_page'))
    order_details = OrderDetailsForm(request.POST)
    order_details.is_valid()
    order_details = order_details.cleaned_data
    cake_constructor_form = CakeConstructorForm(request.POST)
    cake_constructor_form.is_valid()
    cake_params = cake_constructor_form.cleaned_data
    cake = Cake.objects.create(
        level=CakeLevel.objects.get(pk=cake_params['cake_level']),
        form=CakeForm.objects.get(pk=cake_params['cake_form']),
        topping=Topping.objects.get(pk=cake_params['topping']),
        caption_on_cake=cake_params['caption_on_cake']
    )
    cake.decor.add(*map(lambda pk: Decor.objects.get(pk=pk), cake_params['decor']))
    cake.berry.add(*map(lambda pk: Berry.objects.get(pk=pk), cake_params['berry']))
    # собираем заказ
    if request.POST.get('promo_code'):
        promo_code = PromoCode.objects.get(code=request.POST.get('promo_code'))
    else:
        promo_code = None
    Order.objects.create(
        client=request.user,
        cake=cake,
        destination=order_details['destination'],
        delivery_time=order_details['order_datetime'],
        comment=order_details['comments'],
        promo_code=promo_code,
        total_price=request.POST.get('cake_price')
    )
    return redirect(urls.reverse('account'))


class HomePageView(TemplateView):
    template_name = 'super_main.html'
