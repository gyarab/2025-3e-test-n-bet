from django.shortcuts import render
import os
import json
from .models import Strategy

def strategy(request):
    return render(request, "strategies/strategy.html", {
        'strategies': Strategy.objects.all()
    })



# TODO: Implement views for getting strategy results (get_sma_list and get_sma_result in strategies/sma.py).