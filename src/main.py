import logging

import pandas as pd

from src.services import analyze_cashback_categories
from src.utils import load_transactions

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Основная функция приложения для анализа кешбэка."""
    logger.info("Запуск приложения...")

    try:
        # Загрузка данных
        transactions = load_transactions('../data/operations.xlsx')
        logger.info("Транзакции успешно загружены.")
    except FileNotFoundError as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        return

    # Выбор периода анализа
    print("\nВыберите период для анализа кешбэка:")
    print("1. Анализ за конкретный месяц и год")
    print("2. Анализ за диапазон дат")

    choice = input("Введите ваш выбор (1/2): ").strip()

    if choice == '1':
        year = int(input("Введите год (например, 2024): ").strip())
        month = int(input("Введите месяц (1-12): ").strip())

        cashback_result = analyze_cashback_categories(transactions, year=year, month=month)
        if cashback_result:
            print("Анализ кешбэка за выбранный месяц:")
            print(cashback_result)
        else:
            logger.warning("Нет данных для анализа кешбэка за указанный месяц и год.")

    elif choice == '2':
        start_date = input("Введите начальную дату (YYYY-MM-DD): ").strip()
        end_date = input("Введите конечную дату (YYYY-MM-DD): ").strip()

        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], errors='coerce')
        filtered_data = transactions[(
            transactions['Дата операции'] >= pd.to_datetime(start_date)) &
            (transactions['Дата операции'] <= pd.to_datetime(end_date))
        ]

        cashback_result = analyze_cashback_categories(filtered_data, year=None, month=None)
        if cashback_result:
            print("Анализ кешбэка за выбранный диапазон:")
            print(cashback_result)
        else:
            logger.warning("Нет данных для анализа кешбэка за указанный диапазон дат.")
    else:
        print("Некорректный ввод. Попробуйте снова.")

    logger.info("Завершение работы приложения.")


if __name__ == '__main__':
    main()
