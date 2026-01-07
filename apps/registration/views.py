from django.shortcuts import render, redirect
from django.contrib import messages
from requests import request
from .forms import CustomUserRegisterForm, CustomUserLoginForm
from django.contrib.auth import authenticate, login, logout


def register(request):
    form = CustomUserRegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("login")

    return render(request, "registration/register.html", {
        "form": form
    })

def login_view(request):
    form = CustomUserLoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("login")
    
    return render(request, "registration/login.html", {
        "form": form
    })
    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
    return render(request, "registration/login.html")