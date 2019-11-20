from celery import shared_task
from django.core.mail import send_mail
import json
from urllib.request import urlopen
from .models import Mail
from django.contrib.auth import get_user_model


@shared_task
def send_email(title, text, email, pk_author):
    json_url = urlopen('http://jsonplaceholder.typicode.com/users')
    data = json.loads(json_url.read())
    new_data = {}
    str_data = '\n ======== founded ======== \n'
    for el in data:
        if el['email'] == email:
            new_data = el
            for elnd in new_data:
                str_data = str_data + elnd + ': ' + str(new_data[elnd]).\
                    replace("'", "").replace('{', '\n').\
                    replace('}', '').replace(', ', '\n') + '\n'
            break

    if text and new_data:
        text = text + str(str_data)
    else:
        text = text + email

    status = send_mail(title,
                       text,
                       'fogs-test@yandex.ru',
                       ['fogs-test@yandex.ru'],
                       fail_silently=False)

    if status == 1:
        status = True
    else:
        status = False

    User = get_user_model()
    if email and text and title:
        mail_m = Mail(author=User.objects.get(pk=pk_author),
                      title=title,
                      email=email,
                      text=text,
                      status=status,)
        mail_m.save()

    return 'Subject: {} - sended, object saved'.format(title)
