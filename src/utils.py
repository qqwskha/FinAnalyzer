import requests
import pandas as pd
from datetime import datetime

def get_greeting(date: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if 5 <= date.hour < 12:
        return "Доброе утро"
    elif 12 <= date.hour < 18:
        return "Добрый день"
    elif 18 <= date.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def fetch_currency_rates() -> list:
    """Получает текущие курсы валют с API."""
    try:
        response = requests.get("https://api.exchangeratesapi.io/latest")
        response.raise_for_status()
        data = response.json()
        return [{"currency": key, "rate": value} for key, value in data['rates'].items()]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return []

def fetch_stock_prices() -> list:
    """Возвращает фиктивные цены акций."""
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08}
    ]

def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    return pd.read_excel(file_path)
