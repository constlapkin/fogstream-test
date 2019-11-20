from django.urls import path
from .views import GeneralView, LogoutView


urlpatterns = [
    path('', GeneralView.as_view()),
    path('logout/', LogoutView.as_view()),
]
