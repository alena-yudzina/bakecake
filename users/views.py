from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def show_orders(request):
	return render(request=request, template_name='user.html', context={'user': request.user})
