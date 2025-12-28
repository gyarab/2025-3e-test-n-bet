
from django.urls import path
from .views import get_indicator_list, get_strategy_view

urlpatterns = [
    path("get/", get_strategy_view, name="get_strategies"),
    path("indicators/", get_indicator_list, name="get_indicators"),
]
