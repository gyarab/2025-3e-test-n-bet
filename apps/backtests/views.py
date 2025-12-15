from django.shortcuts import render

    
def backtests_home(request):
    return render(request, "backtests/backtests.html")
