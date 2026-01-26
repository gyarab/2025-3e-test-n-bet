from django.shortcuts import render
import os
import json
from .models import Strategy

def strategy(request):
    for s in Strategy.objects.all():
        print(f"Strategy: {s.name}, Parameters: {json.dumps(s.parameters, indent=2)}")
    return render(request, "strategies/pages/strategy.html", {
        'strategies': Strategy.objects.all()
    })



# TODO: Implement views for getting strategy results (get_sma_list and get_sma_result in strategies/sma.py).