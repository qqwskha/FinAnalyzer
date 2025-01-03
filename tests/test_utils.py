from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import (calculate_cashback, ensure_datetime_column, ensure_directory_exists,
                       filter_transactions_by_category, get_last_three_months_range)


# Тест для функции get_last_three_months_range
def test_get_last_three_months_range() -> None:
    """Тестирование функции получения диапазона дат за последние 3 месяца."""

    # Тест с переданной датой
    date = "2023-12-01"
    start_date, end_date = get_last_three_months_range(date)
    assert start_date == pd.Timestamp("2023-09-01")
    assert end_date == pd.Timestamp("2023-12-01")

    # Тест без передачи даты (по умолчанию текущая дата)
    end_date = pd.Timestamp.now().normalize()  # Нормализуем дату, устанавливая время на 00:00:00
    start_date = end_date - pd.DateOffset(months=3)
    start_date_func, end_date_func = get_last_three_months_range()

    # Сравниваем нормализованные значения
    assert start_date_func == start_date
    assert end_date_func == end_date


# Тест для функции ensure_datetime_column
def test_ensure_datetime_column() -> None:
    """Тестирование преобразования столбца в datetime."""

    # Создаем тестовый DataFrame
    data = {'Дата операции': ['2023-01-01', '2023-01-15', '2023-02-01']}
    df = pd.DataFrame(data)

    # Преобразуем столбец 'Дата операции' в datetime
    result_df = ensure_datetime_column(df, 'Дата операции')

    # Проверяем, что столбец стал datetime
    assert result_df['Дата операции'].dtype == 'datetime64[ns]'

    # Тестируем случай, когда столбец не существует
    with pytest.raises(KeyError):
        ensure_datetime_column(df, 'Не существующий столбец')


# Тест для функции ensure_directory_exists
@patch("os.makedirs")
def test_ensure_directory_exists(mock_makedirs: MagicMock) -> None:
    """Тестирование создания папки, если её нет."""

    path = 'test_folder'

    # Проверяем, что папка не существует, и создаем её
    mock_makedirs.reset_mock()  # Сбросим количество вызовов mock
    ensure_directory_exists(path)

    # Проверяем, что os.makedirs был вызван только 1 раз
    mock_makedirs.assert_called_once_with(path)


# Тест для функции calculate_cashback
def test_calculate_cashback() -> None:
    """Тестирование расчета кешбэка."""

    # Простой тест с обычной суммой
    cashback = calculate_cashback(1000, 0.05)  # 5% кешбэк
    assert cashback == 50.00

    # Тест с дефолтным значением процента кешбэка (1%)
    cashback = calculate_cashback(1000)
    assert cashback == 10.00

    # Тест с суммой, равной 0
    cashback = calculate_cashback(0)
    assert cashback == 0.00


# Тест для функции filter_transactions_by_category
def test_filter_transactions_by_category() -> None:
    """Тестирование фильтрации транзакций по категории."""

    # Создаем тестовый DataFrame
    data = {
        'Дата операции': ['2023-01-01', '2023-01-15', '2023-02-01'],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Сумма операции': [500, 300, 1500],
        'Кэшбэк': [50, 20, 100],
        'Описание': ['Ресторан', 'Такси', 'Супермаркет']
    }
    df = pd.DataFrame(data)

    # Фильтруем по категории "Еда"
    result_df = filter_transactions_by_category(df, "Еда")

    # Проверяем, что в результате остались только транзакции категории "Еда"
    assert len(result_df) == 2
    assert all(result_df['Категория'] == "Еда")
