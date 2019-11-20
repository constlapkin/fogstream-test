# from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from .forms import MailForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from .tasks import send_email
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# class AjaxableResponseMixin(object):
#     def form_invalid(self, form):
#         response = super(AjaxableResponseMixin, self).form_invalid(form)
#         if self.request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#         else:
#             return response

#     def form_valid(self, form):
#         if self.request.is_ajax():
#             email = self.request.POST.get('email', None)
#             text = self.request.POST.get('text', None)
#             title = self.request.POST.get('title', None)
#             author = self.request.user

#             send_email.delay(title, text, email, author.pk)
#             status = {}
#             status['status'] = 1
#         else:
#             status = {}
#             status['status'] = 0
#         return JsonResponse(status)


# @method_decorator(login_required, name='dispatch')
# class MailListView(AjaxableResponseMixin, CreateView):
#     form_class = MailForm
#     template_name = 'mail/create_mail.html'


class GeneralView(FormView):
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
                email = request.POST.get('email', None)
                text = request.POST.get('text', None)
                title = request.POST.get('title', None)
                author = request.user
                send_email.delay(title, text, email, author.pk)
                status['status'] = 1
            elif request.POST.get('type', None) == 'auth':
                username = request.POST.get('username', None)
                password = request.POST.get('password', None)
                user = authenticate(request=request,
                                    username=username,
                                    password=password)
                if user is not None:
                    login(request, user)
                    status['status'] = 2
                else:
                    status['status'] = 12
            elif request.POST.get('type', None) == 'reg':
                password = request.POST.get('password1')
                username = request.POST.get('username')
                user = User.objects.create_user(username=username,
                                                password=password)
                status['status'] = 3
            else:
                status['status'] = 13
        return JsonResponse(status)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
