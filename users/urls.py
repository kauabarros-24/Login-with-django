from .views import RegisterView, LoginView, UserView
from django.urls import path

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view())
]