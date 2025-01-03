import logging
import os
from typing import Optional

import pandas as pd

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция для получения диапазона дат за последние 3 месяца
def get_last_three_months_range(date: Optional[str] = None) -> tuple[pd.Timestamp, pd.Timestamp]:
    if date:
        end_date = pd.Timestamp(date)
    else:
        end_date = pd.Timestamp.now().normalize()
    start_date = end_date - pd.DateOffset(months=3)
    return start_date, end_date


# Функция для проверки и преобразования столбца с датами
def ensure_datetime_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Проверяет и преобразует указанный столбец в datetime.

    :param df: DataFrame с данными.
    :param column: Название столбца для преобразования.
    :return: DataFrame с преобразованным столбцом.
    """
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
        logger.info(f"Столбец '{column}' преобразован в datetime.")
    else:
        logger.error(f"Столбец '{column}' не найден в DataFrame.")
        raise KeyError(f"Столбец '{column}' не найден.")
    return df


# Функция для создания папки, если её нет
def ensure_directory_exists(path: str) -> None:
    """
    Проверяет, существует ли папка, и создает её, если она отсутствует.

    :param path: Путь к папке.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Папка создана: {path}")
    else:
        logger.info(f"Папка уже существует: {path}")


# Функция для вычисления кешбэка по сумме операций
def calculate_cashback(amount: float, rate: float = 0.01) -> float:
    """
    Рассчитывает кешбэк по сумме операции.

    :param amount: Сумма операции.
    :param rate: Процент кешбэка (по умолчанию 1%).
    :return: Сумма кешбэка.
    """
    cashback = round(amount * rate, 2)
    logger.info(f"Рассчитан кешбэк: {cashback} для суммы: {amount}")
    return cashback


# Функция для фильтрации транзакций по категории
def filter_transactions_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Фильтрует транзакции по указанной категории.

    :param df: DataFrame с транзакциями.
    :param category: Категория для фильтрации.
    :return: Отфильтрованный DataFrame.
    """
    filtered_df = df[df['Категория'] == category]
    logger.info(f"Отфильтровано {len(filtered_df)} транзакций по категории: {category}")
    return filtered_df


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает данные о транзакциях из Excel-файла.
    """
    return pd.read_excel(file_path)
