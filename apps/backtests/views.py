from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
    
def backtests_home(request):
    return render(request, "backtests/backtests.html")
