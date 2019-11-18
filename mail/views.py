from django.views.generic.edit import CreateView
from .forms import MailForm
from django.http import JsonResponse
from django.http import HttpResponse
import json
from urllib.request import urlopen
from .models import Mail
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        if self.request.is_ajax():
            email = self.request.POST.get('email', None)
            text = self.request.POST.get('text', None)
            title = self.request.POST.get('title', None)
            json_url = urlopen('http://jsonplaceholder.typicode.com/users')
            data = json.loads(json_url.read())
            new_data = {}
            str_data = '\n ======== founded ======== \n'
            for el in data:
                if el['email'] == email:
                    new_data = el
                    for elnd in new_data:
                        str_data = str_data + elnd + ': ' + str(new_data[elnd]).\
                            replace("'", "").replace('{', '\n').replace('}', '').\
                            replace(', ', '\n') + '\n'
                    break

            if text and new_data:
                text = text + str(str_data)
            else:
                text = text + email

            status = send_mail(title,
                               text,
                               'fogs-test@yandex.ru',
                               ['fogs-test@yandex.ru'])
            if status:
                new_data['status'] = True
            else:
                new_data['status'] = False

            if email and text and title:
                mail_m = Mail(author=self.request.user,
                              title=title,
                              email=email,
                              text=text,
                              status=new_data['status'])
                mail_m.save()

            return JsonResponse(new_data)
        else:
            return HttpResponse(False)


@method_decorator(login_required, name='dispatch')
class MailListView(AjaxableResponseMixin, CreateView):
    form_class = MailForm
    template_name = 'mail/create_mail.html'
