from django.urls import path
from .views import UserCreateView, TokenView, UserDetailView, create_user, log_in, log_out, profile

urlpatterns = [
    # APIs views
    path('api/create/', UserCreateView.as_view()),
    path('api/token', TokenView.as_view()),
    path('api/me', UserDetailView.as_view()),

    # template views
    path('sign-up/', create_user, name='sign-up'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/', profile, name='profile')
]
