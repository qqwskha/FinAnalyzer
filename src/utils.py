import pandas as pd
import datetime
import os
import logging
from typing import Union, Optional

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 📆 Функция для получения диапазона дат за последние 3 месяца
def get_last_three_months_range(date: Optional[str] = None) -> tuple:
    """
    Возвращает диапазон дат за последние 3 месяца от переданной даты или текущей даты.

    :param date: Строка с датой в формате 'YYYY-MM-DD'. Если None, берется текущая дата.
    :return: Кортеж с начальной и конечной датами.
    """
    if date:
        current_date = pd.to_datetime(date)
    else:
        current_date = pd.Timestamp.now()

    start_date = current_date - pd.DateOffset(months=3)
    return start_date, current_date


# 🛡️ Функция для проверки и преобразования столбца с датами
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


# 📁 Функция для создания папки, если её нет
def ensure_directory_exists(path: str):
    """
    Проверяет, существует ли папка, и создает её, если она отсутствует.

    :param path: Путь к папке.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Папка создана: {path}")
    else:
        logger.info(f"Папка уже существует: {path}")


# 📊 Функция для вычисления кешбэка по сумме операций
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


# 🔍 Функция для фильтрации транзакций по категории
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


def save_json():
    pass


def configure_logging():
    pass