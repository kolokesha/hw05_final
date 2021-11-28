from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ChangePasswordForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/password_change_form.html'
