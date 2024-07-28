from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserTokenSerializer, UserDetailSerializer
from .forms import UserForm

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
            return redirect('')
    else:
        form = UserForm()
    return render(request, 'user/create_user.html', {'form': form})
