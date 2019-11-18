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


@method_decorator(login_required, name='dispatch')
class MailListView(CreateView):
    form_class = MailForm
    template_name = 'mail/create_mail.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get(self, request):
        return super().get(request)

    def post(self, request):
        if request.is_ajax():
            email = request.POST.get('email', '')
            text = request.POST.get('text', '')
            title = request.POST.get('title', '')
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
            if email and text and title:
                mail_m = Mail(title=title, email=email, text=text)
                mail_m.save()

            send_mail(title,
                      text,
                      'fogs-test@yandex.ru',
                      ['fogs-test@yandex.ru'])
            return JsonResponse(new_data)
        else:
            return HttpResponse(False)
