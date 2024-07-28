from django.urls import path
from .views import UserCreateView, TokenView, UserDetailView, create_user, log_in

urlpatterns = [
    path('api/create/', UserCreateView.as_view()),
    path('api/token', TokenView.as_view()),
    path('api/me', UserDetailView.as_view()),
    path('sign-up/', create_user, name='sign-up'),
    path('login/', log_in, name='login')
]
