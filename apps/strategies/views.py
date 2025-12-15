from django.shortcuts import render
import os
import json

def strategy(request):
    json_path = os.path.join('apps', 'strategies', 'static', 'strategies', 'strategy_builder', 'indicators.json')
    with open(json_path, 'r') as f:
        indicators = json.load(f)

    return render(request, "strategies/strategy.html", {
        'indicators_json': json.dumps(indicators)
    })

# TODO: Implement views for getting strategy results (get_sma_list and get_sma_result in strategies/sma.py).