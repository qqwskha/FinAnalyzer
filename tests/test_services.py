import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.services import (analyze_cashback_categories, investment_bank, search_personal_transfers,
                          search_phone_numbers, simple_search)


@pytest.fixture
def transactions_mock():
    """Пример тестового DataFrame с данными о транзакциях."""
    data = {
        'Дата операции': ['2023-01-01', '2023-01-15', '2023-02-10', '2023-03-01'],
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Переводы'],
        'Сумма операции': [500, 300, 1500, 1000],
        'Кэшбэк': [50, 20, 100, 0],
        'Описание': [
            'Кафе',
            'Такси',
            'Ресторан',
            'Иванов И.П. перевод средств'
        ]
    }
    return pd.DataFrame(data)


@patch("pandas.to_datetime", side_effect=pd.to_datetime)
def test_analyze_cashback_categories(mock_to_datetime):
    """Тестирование analyze_cashback_categories с mock."""
    transactions_mock = pd.DataFrame({
        'Дата операции': ['01.01.2023 12:00:00', '15.01.2023 15:30:00', '01.02.2023 18:00:00'],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Сумма операции': [500, 300, 800],
        'Кэшбэк': [50, 20, 80],
        'Описание': ['Ресторан', 'Такси', 'Супермаркет']
    })

    result = analyze_cashback_categories(transactions_mock, year=2023, month=1)
    assert result == {'Еда': 50, 'Транспорт': 20}


def test_investment_bank():
    """Тестирование investment_bank без моков."""
    transactions = [
        {'Дата операции': '2023-01-01 12:00:00', 'Сумма операции': 512},
        {'Дата операции': '2023-01-15 15:30:00', 'Сумма операции': 490},
        {'Дата операции': '2023-02-10 18:00:00', 'Сумма операции': 775}
    ]
    result = investment_bank("2023-01", transactions, limit=100)
    assert result == 98  # (100 - 12) + (100 - 90)



@patch("src.services.pd.DataFrame.to_dict")
def test_simple_search(mock_to_dict, transactions_mock):
    """Тестирование simple_search с mock."""
    mock_to_dict.return_value = [
        {'Дата операции': '2023-01-01', 'Описание': 'Кафе', 'Категория': 'Еда'}
    ]
    result = simple_search(transactions_mock, query="Кафе")
    assert len(result) == 1
    assert result[0]['Описание'] == 'Кафе'
    mock_to_dict.assert_called_once_with('records')


@patch("src.services.pd.DataFrame.to_dict")
def test_search_phone_numbers(mock_to_dict):
    """Тестирование search_phone_numbers с mock."""
    mock_to_dict.return_value = [
        {'Дата операции': '2023-01-01', 'Описание': 'Пополнение телефона +7 123 456-78-90'}
    ]
    data = {
        'Дата операции': ['2023-01-01', '2023-02-15'],
        'Категория': ['Еда', 'Связь'],
        'Описание': ['Пополнение телефона +7 123 456-78-90', 'Интернет']
    }
    transactions = pd.DataFrame(data)

    result = search_phone_numbers(transactions)
    assert len(result) == 1
    assert '+7 123 456-78-90' in result[0]['Описание']
    mock_to_dict.assert_called_once_with('records')


@patch("src.services.pd.DataFrame.to_dict")
def test_search_personal_transfers(mock_to_dict, transactions_mock):
    """Тестирование search_personal_transfers с mock."""
    mock_to_dict.return_value = [
        {'Дата операции': '2023-03-01', 'Описание': 'Иванов И.П. перевод средств'}
    ]
    result = search_personal_transfers(transactions_mock)
    assert len(result) == 1
    assert 'Иванов И.П.' in result[0]['Описание']
    mock_to_dict.assert_called_once_with('records')
