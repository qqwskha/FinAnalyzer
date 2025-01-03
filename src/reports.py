import datetime
import logging
import os
from typing import Callable, Optional

import pandas as pd

from src.utils import ensure_datetime_column, get_last_three_months_range

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Декоратор для сохранения отчетов в файл
def save_report(file_name: Optional[str] = None) -> Callable[[Callable[..., pd.DataFrame]], Callable[..., pd.DataFrame]]:
    """
    Декоратор для сохранения отчета в файл.
    Если имя файла не указано, используется имя по умолчанию.
    """

    def decorator(func: Callable[..., pd.DataFrame]) -> Callable[..., pd.DataFrame]:
        def wrapper(*args: tuple, **kwargs: dict) -> pd.DataFrame:
            result = func(*args, **kwargs)
            nonlocal file_name
            if not file_name:
                file_name = f"{func.__name__}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            output_path = os.path.join("../data/reports", file_name)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            if isinstance(result, pd.DataFrame):
                result.to_csv(output_path, index=False)
                logger.info(f"Отчет сохранен в файл: {output_path}")
            else:
                logger.error("Функция должна возвращать DataFrame для сохранения отчета.")
            return result

        return wrapper

    return decorator


# Траты по категории
@save_report()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает отчет о тратах по категории за последние 3 месяца.
    """
    start_date, current_date = get_last_three_months_range(date)
    transactions = ensure_datetime_column(transactions, 'Дата операции')
    filtered_transactions = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= current_date)
    ]
    return filtered_transactions


# Траты по дням недели
@save_report()
def spending_by_weekday(
    transactions: pd.DataFrame,
    date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.
    """
    if date:
        current_date = pd.to_datetime(date)
    else:
        current_date = pd.Timestamp.now()

    start_date = current_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    filtered_data = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= current_date)
    ]

    filtered_data['День недели'] = filtered_data['Дата операции'].dt.day_name()
    report = (
        filtered_data.groupby('День недели')['Сумма операции']
        .mean()
        .reset_index()
        .sort_values(by='Сумма операции', ascending=False)
    )
    return report


# Траты в рабочий/выходной день
@save_report()
def spending_by_workday(
    transactions: pd.DataFrame,
    date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочие и выходные дни за последние 3 месяца.
    """
    if date:
        current_date = pd.to_datetime(date)
    else:
        current_date = pd.Timestamp.now()

    start_date = current_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    filtered_data = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= current_date)
    ]

    filtered_data['Тип дня'] = filtered_data['Дата операции'].dt.dayofweek.apply(
        lambda x: 'Рабочий день' if x < 5 else 'Выходной день'
    )

    report = (
        filtered_data.groupby('Тип дня')['Сумма операции']
        .mean()
        .reset_index()
    )
    return report
