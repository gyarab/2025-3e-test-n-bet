
from django.urls import path
from .views import get_strategy_view

urlpatterns = [
    path("get/", get_strategy_view, name="get_strategies"),
]
