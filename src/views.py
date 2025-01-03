import logging
from typing import Any, Dict, List

import pandas as pd
import requests

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Приветствие в зависимости от времени суток
def get_greeting(current_time: str) -> str:
    hour = int(current_time.split(' ')[1].split(':')[0])
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


# Суммирование трат и кешбэка по картам
def get_card_summary(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает сводку по картам: последние 4 цифры, сумма потраченных средств и кэшбэк."""
    card_summary = []
    for card in transactions['Номер карты'].unique():
        card_transactions = transactions[transactions['Номер карты'] == card]
        total_spent = card_transactions['Сумма платежа'].sum()
        cashback = total_spent * 0.01  # 1% cashback
        last_digits = str(card)[-4:]  # Extract last 4 digits as string
        card_summary.append({
            'last_digits': last_digits,
            'total_spent': total_spent,
            'cashback': cashback
        })
    return card_summary


# Топ-5 транзакций по сумме платежа
def get_top_transactions(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    top_transactions = transactions.sort_values(by='Сумма платежа', ascending=False).head(5)
    return [
        {
            "date": row['Дата операции'],
            "amount": row['Сумма платежа'],
            "category": row['Категория'],
            "description": row['Описание']
        }
        for _, row in top_transactions.iterrows()
    ]


# Получение курсов валют
def get_currency_rates() -> List[Dict[str, Any]]:
    response = requests.get('https://api.exchangerate.host/latest')
    if response.status_code == 200:
        data = response.json()
        return [
            {"currency": "USD", "rate": data['rates'].get('USD', 'N/A')},
            {"currency": "EUR", "rate": data['rates'].get('EUR', 'N/A')}
        ]
    else:
        logger.error("Не удалось получить курсы валют")
        return []


# Получение стоимости акций
def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    stock_data = []
    for stock in stocks:
        response = requests.get(f'https://api.example.com/stocks/{stock}')
        if response.status_code == 200:
            data = response.json()
            stock_data.append({"stock": stock, "price": data.get('price', 'N/A')})
        else:
            logger.error(f"Не удалось получить данные по акции {stock}")
    return stock_data


# Главная функция
def generate_main_page_response(transactions: pd.DataFrame, current_time: str,
                                user_settings: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "greeting": get_greeting(current_time),
        "cards": get_card_summary(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(user_settings.get("user_stocks", []))
    }
