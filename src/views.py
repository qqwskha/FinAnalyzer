# src/views.py
from utils import fetch_currency_rates, fetch_stock_prices, get_greeting, load_transactions
import json
import pandas as pd
from datetime import datetime


def main_page_view(date_str: str) -> str:
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(date)
    transactions = load_transactions("data/operations.xlsx")

    cards_summary = transactions.groupby('Номер карты').agg(
        total_spent=('Сумма операции', 'sum'),
        cashback=('Сумма операции', lambda x: x.sum() * 0.01)
    ).reset_index()

    top_transactions = transactions.nlargest(5, 'Сумма операции')[
        ['Дата операции', 'Сумма операции', 'Категория', 'Описание']]

    data = {
        "greeting": greeting,
        "cards": cards_summary.to_dict(orient='records'),
        "top_transactions": top_transactions.to_dict(orient='records'),
        "currency_rates": fetch_currency_rates(),
        "stock_prices": fetch_stock_prices()
    }
    return json.dumps(data, ensure_ascii=False, indent=2)
