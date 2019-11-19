from django.views.generic.edit import CreateView
from .forms import MailForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .tasks import send_email


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
            author = self.request.user

            send_email.delay(title, text, email, author.pk)
            status = {}
            status['status'] = 1
        else:
            status = {}
            status['status'] = 0
        return JsonResponse(status)


@method_decorator(login_required, name='dispatch')
class MailListView(AjaxableResponseMixin, CreateView):
    form_class = MailForm
    template_name = 'mail/create_mail.html'
