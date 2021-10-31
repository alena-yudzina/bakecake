from django import forms
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect

from shop.models import Berry, Decor, Topping, CakeLevel, CakeForm


class CakeConstructorChoiceField(ModelChoiceField):
    def __init__(self, model, multiple=False, **kwargs):
        kwargs['queryset'] = model.objects.all()
        kwargs['initial'] = model.objects.first() if not multiple else None
        self.widget = CheckboxSelectMultiple() if multiple else RadioSelect()
        super().__init__(**kwargs)

    def clean(self, value):
        return value

    def __new__(cls, *args, **kwargs):
        if kwargs.get('multiple'):
            cls.__bases__ = (ModelMultipleChoiceField, )
        return super().__new__(cls)


class CakeConstructorForm(forms.Form):
    cake_level = CakeConstructorChoiceField(CakeLevel, multiple=False)
    cake_form = CakeConstructorChoiceField(CakeForm, multiple=False)
    topping = CakeConstructorChoiceField(Topping, multiple=False)
    berry = CakeConstructorChoiceField(Berry, multiple=True)
    decor = CakeConstructorChoiceField(Decor, multiple=True)
    caption_on_cake = forms.CharField(
        max_length=45,
        label='Надпись',
        widget=forms.TextInput(attrs={'class': "form-control border border-secondary"}),
        required=False,
        help_text=('Можно сделать надпись, например: «С днем рождения!». '
                   'Но, пожалуйста, уложитесь в 45 символов. Мы надеемся, что торт будут есть, а не читать :)')
    )


def initial_datetime():
    import datetime
    initial = datetime.datetime.today() + datetime.timedelta(hours=5)
    initial = initial.strftime("%Y-%m-%dT%H:%M")
    return initial


class OrderDetailsForm(forms.Form):
    destination = forms.CharField(
        max_length=200,
        initial=1000,
        label='Куда доставить',
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )
    comments = forms.CharField(
        label='Комментарий к заказу',
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, 'class': "form-control-sm col-12 mt-0 pt-0 mb-3 border border-2"})
    )
    order_datetime = forms.DateTimeField(
        label='Когда',
        # initial=initial_datetime,
        widget=forms.TextInput(
            attrs={
                'class': "form-control-sm border border-2",
                'type': "datetime-local",
                'min': initial_datetime()
            }
        ),
        help_text = 'Минимальное время доставки 5 часов.'
    )
