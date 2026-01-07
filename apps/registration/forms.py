from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")
        #fields = ("username", "password1", "password2")


class CustomUserLoginForm(AuthenticationForm):
    pass