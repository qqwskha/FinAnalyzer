import datetime
import logging
from typing import Any, Dict, List, Optional

import pandas as pd

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#  Анализ выгодных категорий повышенного кешбэка
def analyze_cashback_categories(data: pd.DataFrame, year: Optional[int] = None,
                                month: Optional[int] = None) -> Dict[str, float]:
    """
    Анализ выгодных категорий повышенного кешбэка.
    """
    # Указать формат и установить dayfirst=True, если даты в формате дд.мм.гггг
    data['Дата операции'] = pd.to_datetime(data['Дата операции'],
                                           format='%d.%m.%Y %H:%M:%S', errors='coerce', dayfirst=True)

    if year and month:
        # Анализ за месяц и год
        filtered_data = data[
            (data['Дата операции'].dt.year == year) &
            (data['Дата операции'].dt.month == month)
        ]
    else:
        # Анализ за предоставленный диапазон дат (если фильтрация уже сделана)
        filtered_data = data

    if filtered_data.empty:
        return {}

    cashback_by_category = (
        filtered_data.groupby('Категория')['Кэшбэк']
        .sum()
        .sort_values(ascending=False)
    ).to_dict()

    return cashback_by_category


# Инвесткопилка
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно было бы отложить в «Инвесткопилку».
    """
    # Преобразуем строку месяца в datetime
    month_date = datetime.datetime.strptime(month, "%Y-%m")

    # Преобразуем даты операций в транзакциях в datetime
    for txn in transactions:
        txn['Дата операции'] = pd.to_datetime(txn['Дата операции'], errors='coerce')

    # Фильтруем транзакции по месяцу
    filtered_transactions = [
        txn for txn in transactions
        if txn['Дата операции'].year == month_date.year and
        txn['Дата операции'].month == month_date.month
    ]

    # Логирование для отладки
    logger.info(f"Month: {month_date}")
    logger.info(f"Filtered Transactions: {filtered_transactions}")

    # Рассчитываем общую сумму, которую можно отложить
    total_saved = sum(
        (limit - (txn['Сумма операции'] % limit)) % limit
        for txn in filtered_transactions
    )

    return float(total_saved)  # Убедитесь, что возвращаете float


# Простой поиск
def simple_search(transactions: pd.DataFrame, query: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по описанию или категории.
    """
    filtered_transactions = transactions[
        transactions['Описание'].str.contains(query, case=False, na=False) |
        transactions['Категория'].str.contains(query, case=False, na=False)
    ]

    return [
        {str(key): value for key, value in txn.items()}
        for txn in filtered_transactions.to_dict('records')
    ]


# Поиск по телефонным номерам
def search_phone_numbers(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Ищет транзакции с мобильными номерами в описании.
    """
    phone_pattern = r'\+7 \d{3} \d{2}-\d{2}-\d{2}|\+7 \d{3} \d{3}-\d{2}-\d{2}'
    filtered_transactions = transactions[
        transactions['Описание'].str.contains(phone_pattern, regex=True, na=False)
    ]

    return [
        {str(key): value for key, value in txn.items()}
        for txn in filtered_transactions.to_dict('records')
    ]


# Поиск переводов физическим лицам
def search_personal_transfers(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, относящиеся к переводам физическим лицам.
    """
    filtered_transactions = transactions[
        (transactions['Категория'] == "Переводы") &
        transactions['Описание'].str.contains(r'\b[A-ЯЁ][а-яё]+\s[A-ЯЁ]\.', regex=True, na=False)
    ]

    return [
        {str(key): value for key, value in txn.items()}
        for txn in filtered_transactions.to_dict('records')
    ]
