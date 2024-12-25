# src/reports.py
import pandas as pd
from datetime import datetime, timedelta


def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    if not date:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    start_date = date - timedelta(days=90)
    filtered = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= date)
        ]
    return filtered
