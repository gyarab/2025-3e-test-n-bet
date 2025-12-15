from django.http import JsonResponse
from django.db import connection

def get_trades(request):
    # Tady můžeš brát request.body nebo GET parametry, pokud budeš chtít filtrování
    req_json = '{}'  # placeholder, nebo request.body
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM vrat_trade(%s::json, %s::json, NOW());",
            [req_json, '{}']
        )
        result = cursor.fetchone()

    if result:
        stav, odpoved, headers = result
        return JsonResponse({
            'stav': stav,
            'data': odpoved,
            'headers': headers
        })
    else:
        return JsonResponse({
            'stav': 1,
            'data': [],
            'headers': {}
        })
