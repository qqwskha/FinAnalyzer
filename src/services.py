import pandas as pd
from typing import Dict, List, Any
import datetime
import logging

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#  Анализ выгодных категорий повышенного кешбэка
def analyze_cashback_categories(data: pd.DataFrame, year: int, month: int) -> Dict[str, float]:
    """
    Анализ выгодных категорий повышенного кешбэка.
    """
    # Фильтрация данных по году и месяцу
    data['Дата операции'] = pd.to_datetime(data['Дата операции'])
    filtered_data = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month)
        ]

    # Группировка по категориям и расчет кешбэка
    cashback_by_category = (
        filtered_data.groupby('Категория')['Кешбэк']
        .sum()
        .sort_values(ascending=False)
    ).to_dict()

    return cashback_by_category


# 🏦 Инвесткопилка
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно было бы отложить в «Инвесткопилку».
    """
    month_date = datetime.datetime.strptime(month, "%Y-%m")

    # Фильтрация транзакций по месяцу
    filtered_transactions = [
        txn for txn in transactions
        if datetime.datetime.strptime(txn['Дата операции'], "%Y-%m-%d").year == month_date.year
           and datetime.datetime.strptime(txn['Дата операции'], "%Y-%m-%d").month == month_date.month
    ]

    # Рассчет округления
    total_saved = sum(
        (limit - (txn['Сумма операции'] % limit)) % limit
        for txn in filtered_transactions
    )

    return total_saved


# 🔍 Простой поиск
def simple_search(transactions: pd.DataFrame, query: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по описанию или категории.
    """
    filtered_transactions = transactions[
        transactions['Описание'].str.contains(query, case=False, na=False) |
        transactions['Категория'].str.contains(query, case=False, na=False)
        ]

    return filtered_transactions.to_dict('records')


# 📱 Поиск по телефонным номерам
import re


def search_phone_numbers(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Ищет транзакции с мобильными номерами в описании.
    """
    phone_pattern = r'\+7 \d{3} \d{2}-\d{2}-\d{2}|\+7 \d{3} \d{3}-\d{2}-\d{2}'
    filtered_transactions = transactions[
        transactions['Описание'].str.contains(phone_pattern, regex=True, na=False)
    ]

    return filtered_transactions.to_dict('records')


# 👤 Поиск переводов физическим лицам
def search_personal_transfers(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, относящиеся к переводам физическим лицам.
    """
    filtered_transactions = transactions[
        (transactions['Категория'] == "Переводы") &
        transactions['Описание'].str.contains(r'\b[A-ЯЁ][а-яё]+\s[A-ЯЁ]\.', regex=True, na=False)
        ]

    return filtered_transactions.to_dict('records')
