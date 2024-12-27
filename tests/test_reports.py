from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def transactions_mock():
    """Пример тестового DataFrame с данными о транзакциях."""
    data = {
        'Дата операции': ['2023-01-01', '2023-02-15', '2023-03-20', '2023-01-05'],
        'Категория': ['Еда', 'Еда', 'Транспорт', 'Еда'],
        'Сумма операции': [500, 1500, 300, 200],
        'Описание': ['Покупка 1', 'Покупка 2', 'Такси', 'Покупка 3']
    }
    return pd.DataFrame(data)


@patch("src.reports.get_last_three_months_range")
@patch("src.reports.ensure_datetime_column")
@patch("src.reports.os.makedirs")
@patch("src.reports.pd.DataFrame.to_csv")
def test_spending_by_category(mock_to_csv, mock_makedirs, mock_ensure_datetime_column, mock_get_last_three_months_range, transactions_mock):
    """Тестирование функции spending_by_category."""
    mock_get_last_three_months_range.return_value = ("2023-01-01", "2023-03-31")
    mock_ensure_datetime_column.return_value = transactions_mock

    result = spending_by_category(transactions_mock, "Еда")

    assert not result.empty
    assert list(result.columns) == ['Дата операции', 'Сумма операции', 'Описание']
    mock_to_csv.assert_called_once()


@patch("src.reports.pd.Timestamp.now")
@patch("src.reports.os.makedirs")
@patch("src.reports.pd.DataFrame.to_csv")
def test_spending_by_weekday(mock_to_csv, mock_makedirs, mock_now, transactions_mock):
    """Тестирование функции spending_by_weekday."""
    mock_now.return_value = pd.Timestamp("2023-03-31")

    result = spending_by_weekday(transactions_mock)

    assert not result.empty
    assert 'День недели' in result.columns
    mock_to_csv.assert_called_once()


@patch("src.reports.pd.Timestamp.now")
@patch("src.reports.os.makedirs")
@patch("src.reports.pd.DataFrame.to_csv")
def test_spending_by_workday(mock_to_csv, mock_makedirs, mock_now, transactions_mock):
    """Тестирование функции spending_by_workday."""
    mock_now.return_value = pd.Timestamp("2023-03-31")

    result = spending_by_workday(transactions_mock)

    assert not result.empty
    assert 'Тип дня' in result.columns
    mock_to_csv.assert_called_once()


@patch("src.reports.os.makedirs")
@patch("src.reports.pd.DataFrame.to_csv")
def test_save_report_decorator(mock_to_csv, mock_makedirs):
    """Тестирование сохранения файла через декоратор save_report."""
    @patch("src.reports.logger.info")
    def mock_func(logger_mock):
        def dummy_function():
            return pd.DataFrame({"test": [1, 2, 3]})
        wrapped_func = save_report("test.csv")(dummy_function)
        wrapped_func()
        mock_to_csv.assert_called_once_with("../data/reports/test.csv", index=False)
