"""
URL configuration for prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.market.views import BtcPricesView
from apps.backtests.views import RunBacktestView
from django.urls import path, include

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apps/registration/', include('apps.registration.urls')),
    path('home/', include('core.urls')),
    path('', include('core.urls')),
    path('api/', include('api.urls')),  # všechny endpointy z api
    path('backtests/', include('apps.backtests.urls')),
    path('strategies/', include('apps.strategies.urls')),
]
