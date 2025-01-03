from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import save_report, spending_by_category


@pytest.fixture
def transactions_mock() -> pd.DataFrame:
    """Пример тестового DataFrame с данными о транзакциях."""
    data = {
        'Дата операции': ['2023-01-01', '2023-02-15', '2023-03-20', '2023-01-05'],
        'Категория': ['Еда', 'Еда', 'Транспорт', 'Еда'],
        'Сумма операции': [500, 1500, 300, 200],
        'Описание': ['Покупка 1', 'Покупка 2', 'Такси', 'Покупка 3']
    }
    return pd.DataFrame(data)


@patch("src.reports.pd.DataFrame.to_csv")
@patch("src.reports.os.makedirs")
@patch("src.reports.ensure_datetime_column")
@patch("src.reports.get_last_three_months_range", autospec=True)
def test_spending_by_category(mock_get_last_three_months_range: Any, mock_ensure_datetime_column: Any,
                              mock_makedirs: Any, mock_to_csv: Any, transactions_mock: pd.DataFrame) -> None:
    """Тестирование функции spending_by_category."""

    # Мок возвращает кортеж с двумя датами
    mock_get_last_three_months_range.return_value = (pd.Timestamp("2023-01-01"), pd.Timestamp("2023-03-31"))

    # Тестовые данные
    transactions_mock = pd.DataFrame({
        'Категория': ['Еда', 'Еда', 'Транспорт'],
        'Сумма операции': [100, 200, 50],
        'Описание': ['Покупка', 'Ужин', 'Бензин'],
        'Дата операции': pd.to_datetime(['2023-01-10', '2023-02-10', '2023-03-10'])  # Преобразуем в Timestamp
    })

    # Мокаем ensure_datetime_column
    mock_ensure_datetime_column.return_value = transactions_mock

    # Вызов функции
    result = spending_by_category(transactions_mock, "Еда")

    # Проверки
    assert len(result) == 2
    assert set(result['Категория']) == {'Еда'}
    assert all(result['Дата операции'].apply(lambda x: isinstance(x, pd.Timestamp)))


@patch("src.reports.pd.DataFrame.to_csv")
@patch("src.reports.os.makedirs")
@patch("src.reports.pd.Timestamp.now")
def test_save_report_decorator(mock_now: Any, mock_makedirs: Any, mock_to_csv: Any) -> None:
    """Тестирование сохранения файла через декоратор save_report."""
    # Mock the current time
    mock_now.return_value = pd.Timestamp("2023-12-27")

    # Define a dummy function wrapped with the save_report decorator
    def dummy_function() -> pd.DataFrame:
        return pd.DataFrame({"test": [1, 2, 3]})

    wrapped_func = save_report("test.csv")(dummy_function)
    wrapped_func()

    mock_to_csv.assert_called_once_with("../data/reports\\test.csv", index=False)
