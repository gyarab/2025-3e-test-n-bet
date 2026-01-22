
from django.urls import path
from .views import delete_strategy_view, get_indicator_list, get_strategy_view, save_strategy_view

urlpatterns = [
    path("get/", get_strategy_view, name="get_strategies"),
    path("indicators/", get_indicator_list, name="get_indicators"),
    path("save/", save_strategy_view, name="save_strategy"),
    path("delete/", delete_strategy_view, name="delete_strategy"),
]
