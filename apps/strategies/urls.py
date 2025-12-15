from django.urls import path
from . import views

app_name = "strategies"

urlpatterns = [
    path("", views.strategy, name="strategy"),
]
