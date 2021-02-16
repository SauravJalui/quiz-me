from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm


class HomePageView(TemplateView):
    template_name = 'account/home.html'

# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('account_login')
#     template_name = 'account/signup.html'
