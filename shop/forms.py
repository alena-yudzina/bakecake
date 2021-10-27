from django import forms
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.utils.html import format_html

from shop.models import Berry, Decor, Topping, CakeLevel, CakeForm


def label_for_cake_options(obj, option_name):
    return format_html(
        '{} <span class="mark small">+{}&#8381;</span>',
        getattr(obj, option_name), obj.price
    )


class CakeConstructorChoiceField(ModelChoiceField):
    def __init__(self, model, option_name, multiple=False, **kwargs):
        self.option_name = option_name
        kwargs['queryset'] = model.objects.all()
        kwargs['to_field_name'] = option_name
        kwargs['initial'] = model.objects.first() if not multiple else None
        self.widget = CheckboxSelectMultiple() if multiple else RadioSelect()
        super().__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        if kwargs.get('multiple'):
            cls.__bases__ = (ModelMultipleChoiceField, )
        return super().__new__(cls)

    def label_from_instance(self, obj):
        return label_for_cake_options(obj, self.option_name)


class CakeConstructorForm(forms.Form):
    cake_level = CakeConstructorChoiceField(CakeLevel, 'level_num', multiple=False)
    cake_form = CakeConstructorChoiceField(CakeForm, 'type', multiple=False)
    topping = CakeConstructorChoiceField(Topping, 'name', multiple=False)
    berry = CakeConstructorChoiceField(Berry, 'name', multiple=True)
    decor = CakeConstructorChoiceField(Decor, 'name', multiple=True)
    caption_on_cake = forms.CharField(
        max_length=45,
        label='Надпись',
        widget=forms.TextInput(attrs={'class': "form-control border border-primary"}),
        required=False,
        help_text=('Можно сделать надпись, например: «С днем рождения!». '
                   'Но, пожалуйста, уложитесь в 45 символов. Мы надеемся, что торт будут есть :)')
    )
