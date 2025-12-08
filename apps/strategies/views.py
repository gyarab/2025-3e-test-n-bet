from django.shortcuts import render

def strategy(request):
    return render(request, "strategies/strategy.html")

# TODO: Implement views for getting strategy results (get_sma_list and get_sma_result in strategies/sma.py).