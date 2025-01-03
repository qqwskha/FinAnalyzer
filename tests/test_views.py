from unittest.mock import MagicMock, patch

import pandas as pd

from src.views import (generate_main_page_response, get_card_summary, get_currency_rates, get_greeting,
                       get_stock_prices, get_top_transactions)


# Тестирование функции get_greeting
def test_get_greeting() -> None:
    """Тестирование функции get_greeting."""
    assert get_greeting("2023-12-27 08:00:00") == "Доброе утро"
    assert get_greeting("2023-12-27 14:00:00") == "Добрый день"
    assert get_greeting("2023-12-27 19:00:00") == "Добрый вечер"
    assert get_greeting("2023-12-27 23:00:00") == "Доброй ночи"


# Тестирование функции get_card_summary
def test_get_card_summary() -> None:
    """Тестирование функции get_card_summary."""
    transactions = pd.DataFrame({
        'Номер карты': [1234567890123456, 1234567890123456, 9876543210987654],
        'Сумма платежа': [500, 300, 700]
    })

    # Ожидаемый результат с округлением и приведением типов к float
    expected_result = [
        {"last_digits": "3456", "total_spent": 800.0, "cashback": 8.0},
        {"last_digits": "7654", "total_spent": 700.0, "cashback": 7.0}
    ]

    result = get_card_summary(transactions)

    # Приводим все числовые значения к типу float
    result = [
        {
            "last_digits": card["last_digits"],
            "total_spent": float(round(card["total_spent"], 2)),
            "cashback": float(round(card["cashback"], 2))
        }
        for card in result
    ]

    assert result == expected_result


# Тестирование функции get_top_transactions
def test_get_top_transactions() -> None:
    """Тестирование функции get_top_transactions."""
    transactions = pd.DataFrame({
        'Дата операции': ['2023-12-25 12:00:00', '2023-12-26 12:00:00', '2023-12-27 12:00:00'],
        'Сумма платежа': [500, 1000, 200],
        'Категория': ['Еда', 'Техника', 'Одежда'],
        'Описание': ['Покупка', 'Покупка', 'Покупка']
    })
    expected_result = [
        {"date": '2023-12-26 12:00:00', "amount": 1000, "category": 'Техника', "description": 'Покупка'},
        {"date": '2023-12-25 12:00:00', "amount": 500, "category": 'Еда', "description": 'Покупка'},
        {"date": '2023-12-27 12:00:00', "amount": 200, "category": 'Одежда', "description": 'Покупка'}
    ]

    result = get_top_transactions(transactions)
    assert result == expected_result


# Тестирование функции get_currency_rates с использованием mock
@patch('requests.get')
def test_get_currency_rates(mock_get: MagicMock) -> None:
    """Тестирование функции get_currency_rates с использованием mock."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'rates': {'USD': 74.3, 'EUR': 88.7}
    }
    mock_get.return_value = mock_response

    result = get_currency_rates()
    expected_result = [
        {"currency": "USD", "rate": 74.3},
        {"currency": "EUR", "rate": 88.7}
    ]

    assert result == expected_result


# Тестирование функции get_stock_prices с использованием mock
@patch('requests.get')
def test_get_stock_prices(mock_get: MagicMock) -> None:
    """Тестирование функции get_stock_prices с использованием mock."""
    stock_list = ["AAPL", "GOOGL"]

    # Mocking response for AAPL
    mock_response_aapl = MagicMock()
    mock_response_aapl.status_code = 200
    mock_response_aapl.json.return_value = {'price': 150}

    # Mocking response for GOOGL
    mock_response_googl = MagicMock()
    mock_response_googl.status_code = 200
    mock_response_googl.json.return_value = {'price': 2800}

    mock_get.side_effect = [mock_response_aapl, mock_response_googl]

    result = get_stock_prices(stock_list)
    expected_result = [
        {"stock": "AAPL", "price": 150},
        {"stock": "GOOGL", "price": 2800}
    ]

    assert result == expected_result


# Тестирование функции generate_main_page_response
@patch('requests.get')
def test_generate_main_page_response(mock_get: MagicMock) -> None:
    """Тестирование функции generate_main_page_response с использованием mock."""
    # Mock responses for currency rates and stock prices
    mock_response_currency = MagicMock()
    mock_response_currency.status_code = 200
    mock_response_currency.json.return_value = {
        'rates': {'USD': 74.3, 'EUR': 88.7}
    }

    mock_response_stock = MagicMock()
    mock_response_stock.status_code = 200
    mock_response_stock.json.return_value = {'price': 150}

    mock_get.side_effect = [mock_response_currency, mock_response_stock]

    transactions = pd.DataFrame({
        'Номер карты': [1234567890123456, 9876543210987654],
        'Сумма платежа': [500, 700],
        'Категория': ['Еда', 'Техника'],
        'Описание': ['Покупка', 'Покупка'],
        'Дата операции': ['2023-12-25 12:00:00', '2023-12-26 12:00:00']
    })

    user_settings = {"user_stocks": ["AAPL"]}
    current_time = "2023-12-27 08:00:00"

    # Ожидаемый результат с округленными значениями для корректного сравнения
    expected_result = {
        "greeting": "Доброе утро",
        "cards": [
            {"last_digits": "3456", "total_spent": 500.0, "cashback": 5.0},
            {"last_digits": "7654", "total_spent": 700.0, "cashback": 7.0}
        ],
        "top_transactions": [
            {"date": '2023-12-26 12:00:00', "amount": 700, "category": 'Техника', "description": 'Покупка'},
            {"date": '2023-12-25 12:00:00', "amount": 500, "category": 'Еда', "description": 'Покупка'}
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 74.3},
            {"currency": "EUR", "rate": 88.7}
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": 150}
        ]
    }

    result = generate_main_page_response(transactions, current_time, user_settings)

    # Приводим все числовые значения к типу float
    result["cards"] = [
        {
            "last_digits": card["last_digits"],
            "total_spent": float(round(card["total_spent"], 2)),
            "cashback": float(round(card["cashback"], 2))
        }
        for card in result["cards"]
    ]

    assert result == expected_result
