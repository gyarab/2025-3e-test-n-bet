from django.shortcuts import render, redirect
from django.contrib import messages
from requests import request
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
        #    return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request,username=username,password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
        login(request, user)
        return redirect("home")
    return render(request, "registration/login.html")
    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
    return render(request, "registration/login.html")