from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.backtests.backtest_runner import run_backtest

class RunBacktestView(APIView):
    def get(self, request):
        result = run_backtest()
        return Response(result)
    
def backtests_home(request):
    return render(request, "backtests/backtests.html")
