from django.test import TransactionTestCase
from .views import GeneralView
from django.core.mail import send_mail
import json
from urllib.request import urlopen


class YourTestClass(TransactionTestCase):

    def setUp(self):
        print('initialize')
        pass

    def test_task(self):
        print('test_task')
        founded = 0
        emails = ['Sincere@april.biz', 'privet@hello.ru',
                  'Shanna@melissa.tv', 'poka@goodbye.ru',
                  'Nathan@yesenia.net', 'Julianne.OConner@kory.org',
                  'Lucio_Hettinger@annie.ca', 'hello@example.com',
                  'Karley_Dach@jasper.info', 'test@test.ru',
                  'Telly.Hoeger@billy.biz', 'Sherwood@rosamond.me',
                  'Chaim_McDermott@dana.io', 'Rey.Padberg@karina.biz']

        json_url = urlopen('http://jsonplaceholder.typicode.com/users')
        data = json.loads(json_url.read())
        for email in emails:
            for el in data:
                if el['email'] == email:
                    founded = founded + 1
                    break
        self.assertEquals(founded, 10)

    def test_send(self):
        print('test_task')
        title = 'Test Title'
        text = 'Message'
        status = send_mail(title,
                           text,
                           'fogs-test@yandex.ru',
                           ['fogs-test@yandex.ru'],
                           fail_silently=False)
        self.assertEquals(status, 1)

    def test_validate_email(self):
        print('test_validate_email')
        emails = ['', 'a', 'a@', 'a@a.r', '@a',
                  '@a.r', 'a@.', '@a.ru', 'saasa@adfsd.ru']
        title = 'ss'
        text = 'cc'
        check_e = 0
        for email in emails:
            error = GeneralView.validate_mail(self, title, text, email)
            if error['email'] != '':
                check_e = check_e + 1
            else:
                if error['email_is_not_valid'] != '':
                    check_e = check_e + 1
        self.assertEquals(check_e, 8)

    def tearDown(self):
        print('tearDown')
        pass
