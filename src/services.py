import pandas as pd
from typing import Dict, List, Any
import datetime
import logging
import re

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#  Анализ выгодных категорий повышенного кешбэка
def analyze_cashback_categories(data: pd.DataFrame, year: int, month: int) -> Dict[str, float]:
    """
    Анализ выгодных категорий повышенного кешбэка.
    """
    # Преобразование строковых дат в datetime с учетом формата
    try:
        data['Дата операции'] = pd.to_datetime(
            data['Дата операции'],
            format='%d.%m.%Y %H:%M:%S',
            errors='coerce',
            dayfirst=True
        )
    except Exception as e:
        logger.error(f"Ошибка при преобразовании дат: {e}")
        return {}

    # Проверка наличия корректных дат
    if data['Дата операции'].isnull().all():
        logger.warning("Все даты некорректны после преобразования.")
        return {}

    # Фильтрация данных по году и месяцу
    filtered_data = data[
        (data['Дата операции'].dt.year == year) &
        (data['Дата операции'].dt.month == month)
    ]

    # Проверка на пустой результат
    if filtered_data.empty:
        logger.warning(f"Нет транзакций за {year}-{month} для анализа кешбэка.")
        return {}

    # Группировка по категориям и расчет кешбэка
    cashback_by_category = (
        filtered_data.groupby('Категория')['Кэшбэк']
        .sum()
        .sort_values(ascending=False)
    )

    return cashback_by_category.to_dict()

# 🏦 Инвесткопилка
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно было бы отложить в «Инвесткопилку».
    """
    month_date = datetime.datetime.strptime(month, "%Y-%m")  # Преобразуем месяц в datetime

    # Фильтрация транзакций по месяцу
    filtered_transactions = [
        txn for txn in transactions
        if pd.to_datetime(txn['Дата операции']).year == month_date.year and  # Используем pd.to_datetime
           pd.to_datetime(txn['Дата операции']).month == month_date.month  # Для извлечения года и месяца
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
