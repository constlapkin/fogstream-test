from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from .forms import MailForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .tasks import send_email
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class GeneralView(FormView):

    def validate_mail(self, title, text, email):
        errors = {'title': '',
                  'text': '',
                  'email': '',
                  'email_is_not_valid': ''}
        if title == '':
            errors['title'] = "You didn't enter a title"
        if text == '':
            errors['text'] = "You didn't enter a text"
        if email == '':
            errors['email'] = "You didn't enter a email"
        try:
            validate_email(email)
        except ValidationError:
            errors['email_is_not_valid'] = "You're email is wrong"
        return errors

    def validate_auth(self, username, password):
        errors = {'username': '', 'password': ''}
        if username == '':
            errors['username'] = "You didn't enter a username"
        if password == '':
            errors['password'] = "You didn't enter a password"
        return errors

    def validate_reg(self, username, password1, password2):
        errors = {'username': '', 'password': '', 'password_is_wrong': ''}
        min_length = 8
        if username == '':
            errors['username'] = "You didn't enter a username"
        try:
            expect = User.objects.get(username=username)
        except User.DoesNotExist:
            expect = None
        if expect is not None:
            errors['username'] = "This username is busy"
        if password1 == '' or password2 == '':
            errors['password'] = "You didn't enter a password \
                                  or repeat password"
        else:
            if password1 != password2:
                errors['password_is_wrong'] = "You're password doesn't match"
            if len(password1) < min_length:
                errors['password_is_wrong'] = "You're password too small"
            if sum(c.isdigit() for c in password1) < 1:
                errors['password_is_wrong'] = "Password must contain \
                                              at least 1 number"
            if not any(c.isupper() for c in password1):
                errors['password_is_wrong'] = "Password must contain \
                                              at least 1 uppercase letter"
            if not any(c.islower() for c in password1):
                errors['password_is_wrong'] = "Password must contain \
                                               at least 1 lowercase letter"
        return errors

    def mail_form(self, request, status):
        email = request.POST.get('email', '')
        text = request.POST.get('text', '')
        title = request.POST.get('title', '')
        author = request.user
        validate = self.validate_mail(title, text, email)
        flag = 0
        for el in validate:
            if len(validate[el]) > 0:
                flag = flag + 1
            status[el] = validate[el]
        if author is not None and flag == 0:
            send_email.delay(title, text, email, author.pk)
            status['status'] = 1
        return status

    def auth_form(self, request, status):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        validate = self.validate_auth(username, password)
        flag = 0
        for el in validate:
            if len(validate[el]) > 0:
                flag = flag + 1
            status[el] = validate[el]
        if flag == 0:
            user = authenticate(request=request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                status['status'] = 1
            else:
                status['status'] = 12
        return status

    def reg_form(self, request, status):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        validate = self.validate_reg(username, password1, password2)
        flag = 0
        for el in validate:
            if len(validate[el]) > 0:
                flag = flag + 1
            status[el] = validate[el]
        if flag == 0:
            User.objects.create_user(username=username,
                                     password=password1)
            status['status'] = 1
        return status

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = MailForm
            return render(request,
                          template_name='mail/create_mail.html',
                          context={'form': form})
        else:
            form1 = UserCreationForm
            form2 = AuthenticationForm
            return render(request,
                          template_name='mail/reg.html',
                          context={'form1': form1, 'form2': form2})

    def post(self, request, *args, **kwargs):
        status = {'status': 10}
        if request.is_ajax():
            if request.POST.get('type', None) == 'mail':
                status = self.mail_form(request, status)
            elif request.POST.get('type', None) == 'auth':
                status = self.auth_form(request, status)
            elif request.POST.get('type', None) == 'reg':
                status = self.reg_form(request, status)
            else:
                status['status'] = 13
        return JsonResponse(status)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
