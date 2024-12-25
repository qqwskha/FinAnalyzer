from typing import List, Dict

def cashback_categories(year: int, month: int, transactions: List[Dict]) -> Dict[str, float]:
    cashback_data = {}
    for txn in transactions:
        txn_date = txn['Дата операции'].split('-')
        txn_year, txn_month = int(txn_date[0]), int(txn_date[1])
        if txn_year == year and txn_month == month:
            category = txn['Категория']
            cashback = txn['Сумма операции'] * 0.01
            cashback_data[category] = cashback_data.get(category, 0) + cashback
    return cashback_data
