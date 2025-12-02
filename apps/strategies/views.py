from django.shortcuts import render

def strategies_comparison(request):
    return render(request, "strategies/strategy_comparison.html")

# TODO: Implement views for getting strategy results (get_sma_list and get_sma_result in strategies/sma.py).