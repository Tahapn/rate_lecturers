from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserTokenSerializer, UserDetailSerializer
from .forms import UserForm, UserLogInForm, UserProfileForm

#### APIs ####


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class TokenView(generics.CreateAPIView):
    serializer_class = UserTokenSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'Token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'Invalid credentials or user does not exitst'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


#### template ####

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'user/create_user.html', {'form': form})


def log_in(request):
    # redirects to home if user is already logged in
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user=user)
                return redirect('home')
    else:
        form = UserLogInForm()

    return render(request, 'user/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user/profile.html', {'form': form})
