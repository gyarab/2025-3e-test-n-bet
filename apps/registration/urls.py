from django.urls import path
from . import views
from .views import login_view, logout_view, register  # relativní import

urlpatterns = [
    path('', login_view, name="login"),
    path('register/', register, name='register'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
