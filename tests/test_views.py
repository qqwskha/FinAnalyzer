import json

from src.views import main_page_view


def test_main_page_view():
    response = main_page_view("2024-06-25 12:00:00")
    data = json.loads(response)
    assert "greeting" in data
    assert "cards" in data
    assert "top_transactions" in data
    assert "currency_rates" in data
    assert "stock_prices" in data
