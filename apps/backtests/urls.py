from django.urls import path
from . import views

app_name = "backtests"

urlpatterns = [
    path("", views.backtests_home, name="backtests_home"),
]
