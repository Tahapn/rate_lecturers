from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class UserForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UserLogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
