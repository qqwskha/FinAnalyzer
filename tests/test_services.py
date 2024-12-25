from src.services import cashback_categories

def test_cashback_categories():
    transactions = [
        {"Дата операции": "2024-06-01", "Категория": "Супермаркеты", "Сумма операции": 1000},
        {"Дата операции": "2024-06-02", "Категория": "Топливо", "Сумма операции": 500}
    ]
    result = cashback_categories(2024, 6, transactions)
    assert result == {"Супермаркеты": 10.0, "Топливо": 5.0}
