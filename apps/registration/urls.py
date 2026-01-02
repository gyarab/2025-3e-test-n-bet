from django.urls import path
from . import views
from .api.views import register  # relativní import

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
]
