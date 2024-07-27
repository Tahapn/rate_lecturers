from django.urls import path
from .views import UserCreateView, TokenView

urlpatterns = [
    path('api/create/', UserCreateView.as_view()),
    path('api/token', TokenView.as_view()),
]
