import pandas as pd
from src.reports import spending_by_category

def test_spending_by_category():
    data = {
        "Дата операции": ["2024-06-01", "2024-06-15"],
        "Категория": ["Супермаркеты", "Супермаркеты"],
        "Сумма операции": [100, 200]
    }
    df = pd.DataFrame(data)
    result = spending_by_category(df, "Супермаркеты", "2024-06-30")
    assert len(result) == 2
