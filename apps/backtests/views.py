from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  
def backtests_home(request):
    return render(request, "backtests/backtests.html")
