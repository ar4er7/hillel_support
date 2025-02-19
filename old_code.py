import json
import random
import string
from datetime import datetime, timedelta

import httpx
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import path

last_answer_time = None
total_price = 0


def create_random_string(size: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(size))


def generate_article_idea(request: HttpRequest) -> HttpResponse:
    content = {
        "title": create_random_string(size=10),
        "description": create_random_string(size=20),
    }
    return JsonResponse(content)


async def get_current_market_state(request: HttpRequest) -> JsonResponse:
    global last_answer_time, total_price

    if request.method == "POST":
        data = json.loads(request.body)
        source: str = data.get("src_currency", "no_currency")
        destination: str = data.get("dest_currency", "no currency")

        current_time = datetime.now()
        url = (
            "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
            f"from_currency={source}&"
            f"to_currency={destination}&"
            "apikey=MO31CNEF7DLKTRW1"
        )

        if last_answer_time:
            if current_time - last_answer_time < timedelta(seconds=10):
                return JsonResponse(
                    {
                        "Source": source,
                        "Destination": destination,
                        "CACHED_rate": total_price,
                        "CACHED_time": last_answer_time.strftime("%X"),
                    }
                )

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(url)
        # response: requests.Response = requests.get(url)
        rate: str = response.json()["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
        ]
        total_price = rate
        last_answer_time = current_time

        return JsonResponse(
            {
                "Source": source,
                "Destination": destination,
                "rate": total_price,
            }
        )
    return JsonResponse({"error": "Invalid request method"}, status=400)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path(route="generate-article", view=generate_article_idea),
    path(route="rate-check", view=get_current_market_state),
]
