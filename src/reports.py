import pandas as pd
import datetime
import logging
from typing import Optional, Callable
import os

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 📁 Декоратор для сохранения отчетов в файл
def save_report(file_name: Optional[str] = None):
    """
    Декоратор для сохранения отчета в файл.
    Если имя файла не указано, используется имя по умолчанию.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
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


# 📊 Траты по категории
@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по указанной категории за последние 3 месяца.
    """
    if date:
        current_date = pd.to_datetime(date)
    else:
        current_date = pd.Timestamp.now()

    start_date = current_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    filtered_data = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= current_date)
        ]

    report = filtered_data[['Дата операции', 'Сумма операции', 'Описание']]
    return report


# 📅 Траты по дням недели
@save_report()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
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


# 📆 Траты в рабочий/выходной день
@save_report()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
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
