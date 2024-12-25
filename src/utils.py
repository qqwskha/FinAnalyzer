# src/utils.py

import pandas as pd
import datetime
import os
import logging
from typing import Union

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 📆 Функция для получения диапазона дат за последние 3 месяца
def get_last_three_months_range(date: Union[str, None] = None) -> tuple:
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
