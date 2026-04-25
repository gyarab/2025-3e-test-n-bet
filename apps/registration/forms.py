from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean(self):
        username_input = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_input and password:
            # Gets username if the input is email (contains "@")
            if "@" in username_input:
                try:
                    user_obj = User.objects.get(email__iexact=username_input)
                    username = user_obj.username
                except User.DoesNotExist:
                    raise forms.ValidationError("Invalid email or password")
            else:
                username = username_input

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError("Invalid username/email or password")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data