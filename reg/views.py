from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout


class RegistrationView(FormView):
    form_class = UserCreationForm
    success_url = '/enter/login/'
    template_name = 'reg/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'reg/login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
