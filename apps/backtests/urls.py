from django.urls import path
from . import views

app_name = "backtests"

urlpatterns = [
    path("", views.backtests_home, name="index"),
    path("my-backtests/<int:backtest_id>/", views.backtest_detail, name="detail"),
    path("my-backtests", views.my_backtests, name="my-backtests"),
]
