from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  
def backtests_home(request):
    print("Rendering backtests home page for user:", request.user)
    return render(request, "backtests/backtests.html")
