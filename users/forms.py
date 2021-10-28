from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from shop.models import CancellationOrder

from .models import CustomUser


class CancellationOrderForm(forms.ModelForm):

    class Meta:
        model = CancellationOrder
        fields = ('comment',)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'phonenumber',
            'social_network',
            'address',
            'agreement',
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
