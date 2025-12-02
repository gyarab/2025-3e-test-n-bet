from django.urls import path
from . import views

app_name = "strategies"

urlpatterns = [
    path("", views.strategies_comparison, name="strategies_comparison"),
]
