from django.urls import path
from .views import RegistrationView, LoginView, LogoutView
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', TemplateView.as_view(template_name="reg/enter.html")),
]
