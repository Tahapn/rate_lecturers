from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer, UserTokenSerializer


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
